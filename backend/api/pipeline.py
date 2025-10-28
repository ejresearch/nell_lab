"""
HARV SHIPPED - Pipeline API
Complete automation pipeline endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel

from ..app.database import get_db
from ..app.models import Module, QualityReport, FeedbackAnalysis
from ..app.auth import get_current_user, require_admin, User
from ..services.integrations import (
    SteelToHarvConverter,
    DigesterToSteelExtractor,
    HarvToSteelFeedback,
    QualityAssuranceLoop
)
from ..app.config import settings

router = APIRouter()

# Initialize integration components
steel_converter = SteelToHarvConverter(settings.curriculum_path)
digester_extractor = DigesterToSteelExtractor()
harv_feedback = HarvToSteelFeedback()
qa_loop = QualityAssuranceLoop(steel_converter, digester_extractor, harv_feedback)


# ============================================================================
# Request/Response Models
# ============================================================================

class GenerateRequest(BaseModel):
    weeks: list[int]
    use_pattern_library: bool = True
    pattern_source_ids: Optional[list[str]] = None


class ImportRequest(BaseModel):
    weeks: list[int]


class ValidateRequest(BaseModel):
    week: int


class FullCycleRequest(BaseModel):
    week: int
    auto_refine: bool = True


# ============================================================================
# Pipeline Endpoints
# ============================================================================

@router.post("/generate")
async def generate_curriculum(
    request: GenerateRequest,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """
    Generate curriculum weeks using Steel2.

    Optionally uses pattern library from Doc Digester analyses.
    """
    # TODO: Call Steel2 generator with pattern library
    return {
        "status": "pending",
        "message": "Steel2 generation not yet connected",
        "weeks": request.weeks,
        "use_patterns": request.use_pattern_library
    }


@router.post("/import-to-harv")
async def import_to_harv(
    request: ImportRequest,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """
    Import Steel2 curriculum weeks to Harv as modules.

    Uses SteelToHarvConverter integration module.
    """
    imported = []
    failed = []

    for week in request.weeks:
        try:
            # Convert week to module
            module_data = steel_converter.convert_week_to_module(week)

            # Check if module already exists
            existing = db.query(Module).filter(Module.week_number == week).first()

            if existing:
                # Update existing
                for key, value in module_data.items():
                    if key != "id" and hasattr(existing, key):
                        setattr(existing, key, value)
                module = existing
            else:
                # Create new
                module = Module(**{k: v for k, v in module_data.items() if k != "id"})
                db.add(module)

            db.commit()
            db.refresh(module)
            imported.append({"week": week, "module_id": module.id})

        except Exception as e:
            failed.append({"week": week, "error": str(e)})

    return {
        "status": "completed",
        "imported": len(imported),
        "failed": len(failed),
        "details": {
            "imported": imported,
            "failed": failed
        }
    }


@router.post("/validate")
async def validate_curriculum(
    request: ValidateRequest,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """
    Validate curriculum week quality using Doc Digester.

    Returns quality metrics and recommendations.
    """
    validation = await qa_loop.validate_curriculum(request.week)

    # Save quality report
    report = QualityReport(
        week_number=request.week,
        quality_score=validation["quality_score"],
        **validation.get("metrics", {}),
        issues=validation.get("issues", []),
        recommendations=validation.get("recommendations", [])
    )
    db.add(report)
    db.commit()

    return validation


@router.post("/full-cycle")
async def run_full_cycle(
    request: FullCycleRequest,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """
    Run complete QA cycle for a week:
    1. Validate quality
    2. Import to Harv (if quality good)
    3. Collect student feedback (if available)
    4. Refine curriculum (if auto_refine enabled)
    """
    results = await qa_loop.run_complete_cycle(
        week_number=request.week,
        auto_refine=request.auto_refine
    )

    # Save results to database
    # TODO: Save to appropriate tables

    return results


@router.get("/quality-report/{week}")
async def get_quality_report(
    week: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get latest quality report for a week."""
    report = db.query(QualityReport)\
        .filter(QualityReport.week_number == week)\
        .order_by(QualityReport.validated_at.desc())\
        .first()

    if not report:
        raise HTTPException(status_code=404, detail="No quality report found for this week")

    return {
        "week_number": report.week_number,
        "quality_score": report.quality_score,
        "metrics": {
            "structural_coherence": report.structural_coherence,
            "pedagogical_soundness": report.pedagogical_soundness,
            "concept_clarity": report.concept_clarity,
            "assessment_alignment": report.assessment_alignment,
            "spiral_learning_coverage": report.spiral_learning_coverage
        },
        "issues": report.issues,
        "recommendations": report.recommendations,
        "validated_at": report.validated_at
    }


@router.get("/status")
async def get_pipeline_status(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get overall pipeline ecosystem status.

    Returns:
    - Total modules/weeks
    - Quality metrics
    - Student engagement
    - Pending improvements
    """
    total_modules = db.query(Module).count()
    published_modules = db.query(Module).filter(Module.is_published == True).count()

    # Get average quality score
    avg_quality = db.query(QualityReport).with_entities(
        db.func.avg(QualityReport.quality_score)
    ).scalar() or 0.0

    # Count pending refinements
    pending_refinements = db.query(FeedbackAnalysis)\
        .filter(FeedbackAnalysis.needs_refinement == True)\
        .count()

    return {
        "status": "operational",
        "modules": {
            "total": total_modules,
            "published": published_modules,
            "unpublished": total_modules - published_modules
        },
        "quality": {
            "average_score": round(avg_quality, 2),
            "threshold": settings.QUALITY_THRESHOLD
        },
        "improvements": {
            "pending_refinements": pending_refinements
        },
        "automation": {
            "auto_validation": settings.ENABLE_AUTO_VALIDATION,
            "auto_import": settings.ENABLE_AUTO_IMPORT,
            "feedback_loop": settings.ENABLE_FEEDBACK_LOOP
        }
    }


@router.post("/batch-validate")
async def batch_validate(
    start_week: int = 1,
    end_week: int = 35,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """
    Run batch validation for multiple weeks.

    Useful for validating entire curriculum at once.
    """
    results = await qa_loop.run_batch_validation(start_week, end_week)

    # Save all quality reports
    for week_num, validation in results.get("weeks", {}).items():
        if validation.get("quality_score"):
            report = QualityReport(
                week_number=week_num,
                quality_score=validation["quality_score"],
                **validation.get("metrics", {}),
                issues=validation.get("issues", []),
                recommendations=validation.get("recommendations", [])
            )
            db.add(report)

    db.commit()

    return results


@router.post("/extract-patterns")
async def extract_patterns(
    analysis_id: str,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """
    Extract pedagogical patterns from Doc Digester analysis.

    Args:
        analysis_id: Chapter ID from Doc Digester

    Returns:
        Extracted patterns ready for Steel2
    """
    # TODO: Load analysis from Doc Digester
    # analysis = load_analysis(analysis_id)

    # Extract patterns
    # patterns = digester_extractor.extract_patterns(analysis)

    # TODO: Save to pattern_library table

    return {
        "status": "pending",
        "message": "Doc Digester integration not yet connected",
        "analysis_id": analysis_id
    }


@router.get("/feedback/{module_id}")
async def get_module_feedback(
    module_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """
    Get student feedback analysis for a module.

    Returns aggregated performance data and improvement recommendations.
    """
    # Get latest feedback analysis
    feedback = db.query(FeedbackAnalysis)\
        .filter(FeedbackAnalysis.module_id == module_id)\
        .order_by(FeedbackAnalysis.analyzed_at.desc())\
        .first()

    if not feedback:
        raise HTTPException(status_code=404, detail="No feedback analysis found for this module")

    return {
        "module_id": feedback.module_id,
        "student_count": feedback.student_count,
        "completion_rate": feedback.completion_rate,
        "average_grade": feedback.average_grade,
        "time_to_mastery": {
            "average_minutes": feedback.average_time_minutes,
            "median_minutes": feedback.median_time_minutes
        },
        "common_misconceptions": feedback.common_misconceptions,
        "struggling_concepts": feedback.struggling_concepts,
        "successful_strategies": feedback.successful_strategies,
        "improvement_recommendations": feedback.improvement_recommendations,
        "needs_refinement": feedback.needs_refinement,
        "analyzed_at": feedback.analyzed_at
    }
