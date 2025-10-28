# HARV SHIPPED Integration Guide

Complete guide to how Steel2, Doc Digester, and Harv integrate into a unified platform.

---

## Architecture Overview

```
┌──────────────────────────────────────────────────────────────┐
│                   HARV SHIPPED ECOSYSTEM                      │
│                                                               │
│  ┌────────────┐      ┌──────────────┐      ┌─────────────┐  │
│  │ Reference  │  →   │  Steel2      │  →   │   Harv      │  │
│  │ Materials  │      │  Generator   │      │   Tutor     │  │
│  └────────────┘      └──────────────┘      └─────────────┘  │
│         ↓                    ↓                       ↓        │
│  ┌────────────┐      ┌──────────────┐      ┌─────────────┐  │
│  │ Doc        │  →   │  Pattern     │  →   │  Student    │  │
│  │ Digester   │      │  Library     │      │  Analytics  │  │
│  └────────────┘      └──────────────┘      └─────────────┘  │
│         ↑                    ↑                       │        │
│         └────────────────────┴───────────────────────┘        │
│                    Feedback Loop                              │
└──────────────────────────────────────────────────────────────┘
```

---

## Integration Modules

### 1. Steel2 → Harv Converter (`steel_to_harv.py`)

**Purpose**: Transform Steel2 curriculum weeks into Harv teaching modules

**Input Format**: Steel2 Week structure
```
Week{XX}/
├── internal_documents/
│   ├── week_spec.json       # Week specifications
│   └── week_summary.md      # Human-readable summary
└── Day{N}_{W}.{N}/           # 4 days of lessons
    ├── 01_class_name.txt
    ├── 02_summary.md
    ├── 05_guidelines_for_sparky.md
    ├── 06_document_for_sparky/  # 6 teacher support docs
    └── 07_sparkys_greeting.txt
```

**Output Format**: Harv Module structure
```json
{
  "id": 5,
  "title": "Week 5: Second Declension Masculine",
  "description": "This week focuses on 2nd declension endings",
  "system_prompt": "You are Sparky, an AI Latin tutor...",
  "module_prompt": "**Learning Sequence...",
  "system_corpus": "**Grammar Focus:**\n2nd declension...",
  "module_corpus": "### Day 1: Discovery\n...",
  "learning_objectives": ["Identify 2nd declension endings", ...],
  "metadata": {
    "source": "Steel2",
    "week_number": 5,
    "grammar_focus": "Second declension masculine"
  }
}
```

**Key Mappings**:
| Steel2 Field | Harv Field | Transformation |
|--------------|------------|----------------|
| `week_spec.title` | `module.title` | Direct mapping |
| `week_spec.grammar_focus` | `module.description` | Direct mapping |
| `guidelines_for_sparky.md` | `system_prompt` | Formatted as Socratic instructions |
| `week_spec.vocabulary` | `system_corpus` | Formatted as knowledge base |
| All 4 days' activities | `module_corpus` | Combined with structure |

**Usage Example**:
```python
from services.integrations import SteelToHarvConverter

converter = SteelToHarvConverter(curriculum_base_path="./data/curriculum")

# Convert single week
module = converter.convert_week_to_module(week_number=5)

# Convert all weeks
all_modules = converter.convert_all_weeks(start_week=1, end_week=35)
```

---

### 2. Doc Digester → Steel2 Pattern Extractor (`digester_to_steel.py`)

**Purpose**: Extract pedagogical patterns from analyzed content to inform Steel2 generation

**Input Format**: Doc Digester 5-phase analysis
```json
{
  "chapter_id": "ch-abc123",
  "comprehension_pass": {...},
  "structural_outline": {
    "outline": [
      {
        "section_title": "Introduction to Cases",
        "pedagogical_purpose": "Build foundation",
        "subtopics": [...]
      }
    ]
  },
  "propositional_extraction": {
    "propositions": [...]
  },
  "pedagogical_mapping": {
    "learning_objectives": [...],
    "student_activities": [...],
    "assessment_questions": [...]
  }
}
```

**Output Format**: Pattern Library
```json
{
  "lesson_flow_templates": [
    {
      "section_title": "Introduction to Cases",
      "pedagogical_purpose": "Build foundation",
      "steps": [
        {
          "type": "introduction",
          "title": "Case System Overview",
          "key_concepts": ["nominative", "genitive"],
          "student_actions": ["Respond to: What is a case?"]
        }
      ]
    }
  ],
  "assessment_patterns": [
    {
      "question_template": "Identify the case of...",
      "question_type": "application",
      "cognitive_level": "application"
    }
  ],
  "teaching_strategies": [...],
  "concept_progressions": [...],
  "activity_structures": [...]
}
```

**Key Extractions**:
| Doc Digester Phase | Extracted Pattern | Steel2 Use |
|--------------------|-------------------|------------|
| Structural Outline | Lesson flow templates | Day structure planning |
| Pedagogical Mapping | Assessment patterns | Day 4 quiz generation |
| Pedagogical Mapping | Teaching strategies | Activity type selection |
| Propositional Extraction | Concept progressions | Grammar sequencing |
| Structural Outline | Activity structures | Exercise design |

**Usage Example**:
```python
from services.integrations import DigesterToSteelExtractor

extractor = DigesterToSteelExtractor()

# Extract from single analysis
patterns = extractor.extract_patterns(analysis_data)

# Build library from multiple analyses
all_analyses = [analysis1, analysis2, analysis3]
pattern_library = extractor.build_pattern_library(all_analyses)

# Use in Steel2 generation
steel2_generator.load_pattern_library(pattern_library)
steel2_generator.generate_week(week=10, use_patterns=True)
```

---

### 3. Harv → Steel2 Feedback Loop (`harv_to_steel.py`)

**Purpose**: Analyze student learning data to generate curriculum improvement recommendations

**Input Format**: Harv analytics data
```json
{
  "module_id": 5,
  "conversations": [
    {
      "id": 123,
      "user_id": 1,
      "messages_json": [
        {"role": "user", "content": "What is genitive?"},
        {"role": "assistant", "content": "Actually, let's reconsider..."}
      ]
    }
  ],
  "progress_data": [
    {
      "user_id": 1,
      "completed": true,
      "grade": "B+",
      "time_spent": 45
    }
  ],
  "memory_summaries": [
    {
      "user_id": 1,
      "what_learned": "2nd declension endings",
      "understanding_level": "proficient"
    }
  ]
}
```

**Output Format**: Improvement Recommendations
```json
{
  "module_id": 5,
  "student_count": 15,
  "completion_rate": 0.867,
  "average_grade": "B+",
  "time_to_mastery": {
    "average_minutes": 47,
    "median_minutes": 42
  },
  "common_misconceptions": [
    {
      "concept": "genitive",
      "frequency": 8,
      "severity": "high"
    }
  ],
  "improvement_recommendations": [
    {
      "type": "content",
      "priority": "high",
      "issue": "Common error with genitive",
      "recommendation": "Add explicit teaching on genitive earlier in lesson",
      "steel2_action": "add_misconception_prevention",
      "target_concept": "genitive"
    }
  ]
}
```

**Analysis Methods**:
| Data Source | Analysis | Output |
|-------------|----------|--------|
| Progress data | Completion rate, grades | Overall difficulty assessment |
| Conversations | Error patterns | Common misconceptions |
| Memory summaries | Understanding levels | Concept difficulty ranking |
| Conversation turns | Interaction counts | Time-intensive topics |

**Usage Example**:
```python
from services.integrations import HarvToSteelFeedback

feedback_analyzer = HarvToSteelFeedback()

# Analyze module performance
analysis = feedback_analyzer.analyze_module_performance(
    module_id=5,
    conversations=conv_data,
    progress_data=progress_data,
    memory_summaries=memory_data
)

# Generate refinement instructions
instructions = feedback_analyzer.generate_refinement_instructions(analysis)

# Apply to Steel2
steel2_generator.refine_week(
    week=5,
    modifications=instructions["modifications"]
)
```

---

### 4. Quality Assurance Loop (`quality_loop.py`)

**Purpose**: Orchestrate the complete automated improvement cycle

**Complete Cycle Steps**:

```
1. VALIDATE CURRICULUM (Doc Digester)
   ↓
   - Structural coherence: 9.0/10
   - Pedagogical soundness: 8.5/10
   - Spiral learning: 27% ✓
   ↓
2. IMPORT TO HARV (if quality >= 7.5)
   ↓
   - Convert to module format
   - Insert into Harv database
   - Ready for students
   ↓
3. COLLECT STUDENT FEEDBACK
   ↓
   - 15 students complete module
   - Completion rate: 86.7%
   - Common error: genitive case (8 occurrences)
   ↓
4. AUTO-REFINE CURRICULUM
   ↓
   - Add genitive practice to Day 2
   - Include misconception prevention
   - Regenerate Days 2-3
   ↓
5. RE-VALIDATE & RE-IMPORT
   ↓
   Next cohort gets improved curriculum
```

**Usage Examples**:

**Single Week Cycle**:
```python
from services.integrations import QualityAssuranceLoop

qa_loop = QualityAssuranceLoop(
    steel_converter=steel_converter,
    digester_extractor=digester_extractor,
    harv_feedback=harv_feedback
)

# Run complete cycle for Week 5
results = await qa_loop.run_complete_cycle(
    week_number=5,
    auto_refine=True
)

# Generate report
report = qa_loop.generate_quality_report(results)
print(report)
```

**Batch Validation**:
```python
# Validate all 35 weeks
batch_results = await qa_loop.run_batch_validation(
    start_week=1,
    end_week=35
)

print(f"Passed: {batch_results['passed']}/35")
print(f"Average Quality: {batch_results['average_quality_score']}/10")
```

---

## Data Flow Diagrams

### Flow 1: Initial Curriculum Creation

```
Reference Latin Textbook
    ↓
[Doc Digester Analysis]
    ├─ Structural Outline
    ├─ Pedagogical Mapping
    ├─ Assessment Patterns
    └─ Teaching Strategies
    ↓
[Pattern Library]
    ↓
[Steel2 Generator]
    ├─ Uses patterns as templates
    ├─ Generates Week 1-35
    └─ Validates spiral learning
    ↓
[Steel2 Curriculum]
    ↓
[Steel→Harv Converter]
    ├─ Maps days → modules
    ├─ Formats prompts
    └─ Builds corpus
    ↓
[Harv Modules 1-35]
    ↓
Ready for Students!
```

### Flow 2: Continuous Improvement Loop

```
[Students Learn via Harv]
    ├─ Complete modules
    ├─ Chat with AI tutor
    └─ Take assessments
    ↓
[Harv Analytics]
    ├─ Completion rates
    ├─ Common errors
    ├─ Time to mastery
    └─ Misconceptions
    ↓
[Harv→Steel Feedback]
    ├─ Identify struggling concepts
    ├─ Generate recommendations
    └─ Create refinement instructions
    ↓
[Steel2 Refinement]
    ├─ Regenerate problem areas
    ├─ Add scaffolding
    └─ Fix misconceptions
    ↓
[Doc Digester Re-Validation]
    ├─ Check quality score
    ├─ Verify improvements
    └─ Approve changes
    ↓
[Updated Harv Module]
    ↓
Next Cohort Gets Better Curriculum!
```

---

## Integration API Endpoints

### Curriculum Pipeline

```bash
# Generate curriculum with patterns
POST /api/pipeline/generate
{
  "weeks": [1, 2, 3],
  "use_pattern_library": true,
  "pattern_source_ids": ["ch-abc123", "ch-def456"]
}

# Import to Harv
POST /api/pipeline/import-to-harv
{
  "weeks": [1, 2, 3]
}

# Run complete cycle
POST /api/pipeline/full-cycle
{
  "week": 5,
  "auto_refine": true
}
```

### Quality Validation

```bash
# Validate single week
POST /api/pipeline/validate
{
  "week": 5
}

# Batch validation
POST /api/pipeline/validate-batch
{
  "start_week": 1,
  "end_week": 35
}

# Get quality report
GET /api/pipeline/quality-report/5
```

### Feedback & Refinement

```bash
# Collect feedback
GET /api/pipeline/feedback/module/5

# Refine curriculum
POST /api/pipeline/refine
{
  "week": 5,
  "feedback_id": "fb-xyz789"
}
```

---

## Configuration

### Enable/Disable Features

```env
# .env file
ENABLE_AUTO_VALIDATION=true      # Auto-validate after generation
ENABLE_AUTO_IMPORT=true          # Auto-import to Harv
ENABLE_PATTERN_EXTRACTION=true   # Extract patterns from analysis
ENABLE_FEEDBACK_LOOP=true        # Collect student feedback
AUTO_REFINE_ON_LOW_QUALITY=true  # Auto-refine if quality < threshold

QUALITY_THRESHOLD=8.0            # Minimum acceptable quality score
```

---

## Best Practices

### 1. Pattern Library Management

- **Start with gold standards**: Analyze high-quality reference materials first
- **Build incrementally**: Add patterns as you analyze more materials
- **Version control**: Track pattern library versions alongside curriculum

### 2. Quality Thresholds

- **7.5-8.0**: Minimum for production deployment
- **8.0-9.0**: Good quality, minor improvements possible
- **9.0+**: Excellent quality, gold standard

### 3. Feedback Collection

- **Minimum cohort size**: Wait for 10+ students before refining
- **Review cycle**: Monthly or per-cohort refinement
- **A/B testing**: Test improvements with small groups first

### 4. Automation Levels

- **Level 1 (Manual)**: Generate → Review → Import
- **Level 2 (Semi-Auto)**: Generate → Auto-validate → Manual review → Import
- **Level 3 (Full Auto)**: Complete cycle with quality gates
- **Level 4 (Continuous)**: Feedback-driven auto-improvement

---

## Troubleshooting

### Issue: Low Quality Scores

**Symptoms**: Validation returns quality score < 7.5

**Solutions**:
1. Check pattern library quality
2. Review Steel2 generation prompts
3. Increase max_retries for generation
4. Manually review and fix specific issues

### Issue: Import Failures

**Symptoms**: Steel→Harv conversion fails

**Solutions**:
1. Verify Steel2 output structure matches expected format
2. Check for missing required files (week_spec.json, etc.)
3. Review conversion logs for specific errors

### Issue: No Student Feedback

**Symptoms**: Feedback analysis returns empty data

**Solutions**:
1. Ensure students have completed modules
2. Check Harv database connections
3. Verify module_id mappings are correct

---

## Next Steps

1. **Run Initial Pattern Extraction**:
   ```bash
   python -m scripts.extract_patterns --source wheelock_chapters/
   ```

2. **Generate First 5 Weeks**:
   ```bash
   python -m scripts.generate_curriculum --weeks 1-5 --use-patterns
   ```

3. **Import to Harv**:
   ```bash
   python -m scripts.import_to_harv --weeks 1-5
   ```

4. **Enable Auto-QA Loop**:
   ```bash
   # In .env
   ENABLE_AUTO_VALIDATION=true
   AUTO_REFINE_ON_LOW_QUALITY=true
   ```

5. **Monitor Dashboard**:
   ```
   http://localhost:8000/pipeline/dashboard
   ```

---

**For detailed API documentation, see**: [API_REFERENCE.md](API_REFERENCE.md)

**For architecture details, see**: [ARCHITECTURE.md](ARCHITECTURE.md)
