"""
Doc Digester → Steel2 Pattern Extractor
Transforms Doc Digester analysis into Steel2-compatible pedagogical patterns
"""
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)


class DigesterToSteelExtractor:
    """
    Extracts pedagogical patterns from Doc Digester analysis
    and formats them for use in Steel2 curriculum generation.

    Input: Doc Digester 5-phase analysis JSON
    Output: Pattern library for Steel2 generators
    """

    def extract_patterns(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract all patterns from a Doc Digester analysis.

        Args:
            analysis: Complete Doc Digester analysis output

        Returns:
            Pattern library dictionary with:
            - lesson_flow_templates
            - assessment_patterns
            - teaching_strategies
            - concept_progressions
            - activity_structures
        """
        logger.info("Extracting patterns from Doc Digester analysis")

        patterns = {
            "source_chapter_id": analysis.get("chapter_id", "unknown"),
            "analysis_timestamp": analysis.get("timestamp", ""),

            "lesson_flow_templates": self._extract_lesson_flow(
                analysis.get("structural_outline", {})
            ),

            "assessment_patterns": self._extract_assessment_patterns(
                analysis.get("pedagogical_mapping", {})
            ),

            "teaching_strategies": self._extract_teaching_strategies(
                analysis.get("pedagogical_mapping", {})
            ),

            "concept_progressions": self._extract_concept_progressions(
                analysis.get("propositional_extraction", {})
            ),

            "activity_structures": self._extract_activity_structures(
                analysis.get("pedagogical_mapping", {})
            ),

            "temporal_insights": self._extract_temporal_insights(
                analysis.get("pedagogical_mapping", {}).get("temporal_analysis", {})
            )
        }

        logger.info(f"✓ Extracted {sum(len(v) if isinstance(v, list) else 1 for v in patterns.values())} patterns")
        return patterns

    def _extract_lesson_flow(self, structural_outline: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extract lesson flow patterns from structural outline.

        Returns:
            List of lesson step templates
        """
        templates = []
        outline = structural_outline.get("outline", [])

        for section in outline:
            template = {
                "section_title": section.get("section_title", ""),
                "pedagogical_purpose": section.get("pedagogical_purpose", ""),
                "rhetorical_mode": section.get("rhetorical_mode", "expository"),
                "estimated_duration": 10,  # Default, adjust based on content

                "steps": []
            }

            # Extract subtopics as lesson steps
            for subtopic in section.get("subtopics", []):
                step = {
                    "type": self._infer_step_type(subtopic),
                    "title": subtopic.get("subtopic_title", ""),
                    "key_concepts": subtopic.get("key_concepts", []),
                    "student_actions": self._extract_student_actions(subtopic),
                    "teacher_notes": subtopic.get("notes_on_instructional_sequence", "")
                }
                template["steps"].append(step)

            if template["steps"]:  # Only add if has steps
                templates.append(template)

        return templates

    def _infer_step_type(self, subtopic: Dict[str, Any]) -> str:
        """Infer lesson step type from subtopic content."""
        title = subtopic.get("subtopic_title", "").lower()

        if any(word in title for word in ["introduce", "introduction", "discover"]):
            return "introduction"
        elif any(word in title for word in ["practice", "exercise", "drill"]):
            return "guided_practice"
        elif any(word in title for word in ["assess", "quiz", "test", "check"]):
            return "assessment"
        elif any(word in title for word in ["review", "recall"]):
            return "review"
        elif any(word in title for word in ["chant", "recite"]):
            return "chant"
        else:
            return "guided_practice"

    def _extract_student_actions(self, subtopic: Dict[str, Any]) -> List[str]:
        """Extract expected student actions from subtopic."""
        actions = []

        # Extract from discussion prompts
        prompts = subtopic.get("student_discussion_prompts", [])
        for prompt in prompts:
            actions.append(f"Respond to: {prompt}")

        # Extract from supporting examples
        examples = subtopic.get("supporting_examples", [])
        if examples:
            actions.append(f"Work through examples: {', '.join(examples[:2])}")

        return actions if actions else ["Participate in lesson"]

    def _extract_assessment_patterns(
        self,
        pedagogical_mapping: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Extract assessment question patterns."""
        patterns = []
        questions = pedagogical_mapping.get("assessment_questions", [])

        for q in questions:
            pattern = {
                "question_template": q.get("question", ""),
                "question_type": q.get("question_type", "recall"),
                "location_context": q.get("location", ""),
                "cognitive_level": self._infer_cognitive_level(q.get("question_type", ""))
            }
            patterns.append(pattern)

        return patterns

    def _infer_cognitive_level(self, question_type: str) -> str:
        """Map question type to Bloom's taxonomy."""
        type_lower = question_type.lower()

        if "analysis" in type_lower or "compare" in type_lower:
            return "analysis"
        elif "apply" in type_lower or "practice" in type_lower:
            return "application"
        elif "evaluate" in type_lower or "critique" in type_lower:
            return "evaluation"
        elif "create" in type_lower or "design" in type_lower:
            return "synthesis"
        elif "understand" in type_lower or "explain" in type_lower:
            return "comprehension"
        else:
            return "knowledge"

    def _extract_teaching_strategies(
        self,
        pedagogical_mapping: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Extract teaching strategies from student activities."""
        strategies = []
        activities = pedagogical_mapping.get("student_activities", [])

        for activity in activities:
            strategy = {
                "activity_type": activity.get("activity_type", ""),
                "description": activity.get("description", ""),
                "location": activity.get("location", ""),
                "teaching_mode": self._classify_teaching_mode(activity)
            }
            strategies.append(strategy)

        return strategies

    def _classify_teaching_mode(self, activity: Dict[str, Any]) -> str:
        """Classify teaching mode from activity description."""
        desc = activity.get("description", "").lower()

        if any(word in desc for word in ["socratic", "question", "discuss"]):
            return "socratic_dialogue"
        elif any(word in desc for word in ["practice", "exercise", "drill"]):
            return "guided_practice"
        elif any(word in desc for word in ["discover", "explore", "investigate"]):
            return "discovery_learning"
        elif any(word in desc for word in ["lecture", "explain", "present"]):
            return "direct_instruction"
        else:
            return "interactive_learning"

    def _extract_concept_progressions(
        self,
        propositional_extraction: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Extract concept progression patterns."""
        progressions = []
        propositions = propositional_extraction.get("propositions", [])

        for prop in propositions:
            progression = {
                "concept_id": prop.get("id", ""),
                "truth_type": prop.get("truth_type", "descriptive"),
                "statement": prop.get("statement", ""),
                "learning_implication": prop.get("implication_for_learning", ""),
                "connections": prop.get("connections_to_other_chapters", []),
                "reflection_question": prop.get("potential_student_reflection_question", "")
            }
            progressions.append(progression)

        return progressions

    def _extract_activity_structures(
        self,
        pedagogical_mapping: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Extract activity structures."""
        structures = []
        activities = pedagogical_mapping.get("student_activities", [])

        # Group by activity type
        activity_types = {}
        for activity in activities:
            atype = activity.get("activity_type", "general")
            if atype not in activity_types:
                activity_types[atype] = []
            activity_types[atype].append(activity)

        # Create structure templates for each type
        for atype, activities_list in activity_types.items():
            structure = {
                "activity_type": atype,
                "frequency": len(activities_list),
                "typical_description": activities_list[0].get("description", ""),
                "variations": [a.get("description", "") for a in activities_list[:3]]
            }
            structures.append(structure)

        return structures

    def _extract_temporal_insights(
        self,
        temporal_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Extract temporal insights for content maintenance."""
        return {
            "temporal_range": temporal_analysis.get("temporal_range", ""),
            "historical_examples_count": len(temporal_analysis.get("historical_examples", [])),
            "contemporary_examples_count": len(temporal_analysis.get("contemporary_examples", [])),
            "update_priority": self._calculate_update_priority(temporal_analysis)
        }

    def _calculate_update_priority(self, temporal_analysis: Dict[str, Any]) -> str:
        """Calculate content update priority based on temporal analysis."""
        contemporary = temporal_analysis.get("contemporary_examples", [])

        if not contemporary:
            return "low"

        high_priority_count = sum(
            1 for ex in contemporary
            if ex.get("update_priority") == "high"
        )

        if high_priority_count > 0:
            return "high"
        elif high_priority_count == 0 and len(contemporary) > 3:
            return "medium"
        else:
            return "low"

    def build_pattern_library(
        self,
        analyses: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Build comprehensive pattern library from multiple analyses.

        Args:
            analyses: List of Doc Digester analysis outputs

        Returns:
            Consolidated pattern library
        """
        logger.info(f"Building pattern library from {len(analyses)} analyses")

        all_patterns = {
            "lesson_flow_templates": [],
            "assessment_patterns": [],
            "teaching_strategies": [],
            "concept_progressions": [],
            "activity_structures": []
        }

        for analysis in analyses:
            patterns = self.extract_patterns(analysis)

            for key in all_patterns.keys():
                if key in patterns and isinstance(patterns[key], list):
                    all_patterns[key].extend(patterns[key])

        # Deduplicate and rank by frequency
        for key in all_patterns.keys():
            all_patterns[key] = self._deduplicate_patterns(all_patterns[key])

        logger.info(f"✓ Built library with {sum(len(v) for v in all_patterns.values())} total patterns")
        return all_patterns

    def _deduplicate_patterns(self, patterns: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Deduplicate patterns based on similarity."""
        # Simple deduplication by title/type
        # TODO: Implement more sophisticated similarity detection
        seen = set()
        unique = []

        for pattern in patterns:
            # Create key from first few meaningful fields
            key_parts = []
            for field in ["section_title", "activity_type", "question_type", "concept_id"]:
                if field in pattern:
                    key_parts.append(str(pattern[field]))

            key = "|".join(key_parts)

            if key not in seen:
                seen.add(key)
                unique.append(pattern)

        return unique
