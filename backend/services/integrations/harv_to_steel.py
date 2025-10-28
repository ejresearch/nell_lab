"""
Harv → Steel2 Feedback Loop
Analyzes student learning data from Harv to improve Steel2 curriculum
"""
from typing import Dict, Any, List, Optional
from collections import Counter
import logging

logger = logging.getLogger(__name__)


class HarvToSteelFeedback:
    """
    Analyzes Harv student data and generates actionable feedback
    for Steel2 curriculum improvement.

    Input: Harv analytics data (conversations, progress, memory summaries)
    Output: Curriculum improvement recommendations
    """

    def analyze_module_performance(
        self,
        module_id: int,
        conversations: List[Dict[str, Any]],
        progress_data: List[Dict[str, Any]],
        memory_summaries: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Analyze student performance for a specific module.

        Args:
            module_id: Module/week number
            conversations: List of student conversations
            progress_data: Student progress records
            memory_summaries: Learning memory summaries

        Returns:
            Performance analysis with improvement recommendations
        """
        logger.info(f"Analyzing performance data for Module {module_id}")

        analysis = {
            "module_id": module_id,
            "student_count": len(set(p.get("user_id") for p in progress_data)),
            "completion_rate": self._calculate_completion_rate(progress_data),
            "average_grade": self._calculate_average_grade(progress_data),
            "time_to_mastery": self._calculate_time_to_mastery(progress_data),
            "common_misconceptions": self._identify_misconceptions(conversations),
            "struggling_concepts": self._identify_struggling_concepts(
                conversations,
                memory_summaries
            ),
            "successful_strategies": self._identify_successful_strategies(memory_summaries),
            "improvement_recommendations": []
        }

        # Generate recommendations
        analysis["improvement_recommendations"] = self._generate_recommendations(analysis)

        logger.info(f"✓ Analyzed Module {module_id}: {analysis['student_count']} students")
        return analysis

    def _calculate_completion_rate(self, progress_data: List[Dict[str, Any]]) -> float:
        """Calculate module completion rate."""
        if not progress_data:
            return 0.0

        completed = sum(1 for p in progress_data if p.get("completed", False))
        return round(completed / len(progress_data), 3)

    def _calculate_average_grade(self, progress_data: List[Dict[str, Any]]) -> str:
        """Calculate average grade."""
        grades = [p.get("grade", "") for p in progress_data if p.get("grade")]
        if not grades:
            return "N/A"

        # Convert letter grades to numeric
        grade_map = {
            "A+": 4.3, "A": 4.0, "A-": 3.7,
            "B+": 3.3, "B": 3.0, "B-": 2.7,
            "C+": 2.3, "C": 2.0, "C-": 1.7,
            "D+": 1.3, "D": 1.0, "F": 0.0
        }

        numeric_grades = [grade_map.get(g, 0) for g in grades]
        avg = sum(numeric_grades) / len(numeric_grades)

        # Convert back to letter
        if avg >= 4.0:
            return "A"
        elif avg >= 3.7:
            return "A-"
        elif avg >= 3.3:
            return "B+"
        elif avg >= 3.0:
            return "B"
        elif avg >= 2.7:
            return "B-"
        elif avg >= 2.3:
            return "C+"
        elif avg >= 2.0:
            return "C"
        else:
            return "C-"

    def _calculate_time_to_mastery(self, progress_data: List[Dict[str, Any]]) -> Dict[str, float]:
        """Calculate average time to mastery."""
        times = [p.get("time_spent", 0) for p in progress_data if p.get("completed")]

        if not times:
            return {"average_minutes": 0, "median_minutes": 0}

        times.sort()
        avg = sum(times) / len(times)
        median = times[len(times) // 2]

        return {
            "average_minutes": round(avg, 1),
            "median_minutes": round(median, 1)
        }

    def _identify_misconceptions(
        self,
        conversations: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Identify common student misconceptions from conversations.

        Looks for patterns in questions, repeated errors, and AI corrections.
        """
        misconceptions = []
        error_patterns = []

        for conv in conversations:
            messages = conv.get("messages_json", [])

            for i, msg in enumerate(messages):
                if msg.get("role") == "assistant":
                    content = msg.get("content", "").lower()

                    # Look for correction language
                    if any(phrase in content for phrase in [
                        "actually", "not quite", "let's reconsider",
                        "common mistake", "remember that"
                    ]):
                        # Get previous user message for context
                        if i > 0 and messages[i-1].get("role") == "user":
                            error_patterns.append({
                                "student_message": messages[i-1].get("content", ""),
                                "correction": content[:200]
                            })

        # Count and rank by frequency
        error_counter = Counter(
            self._extract_concept(e["student_message"])
            for e in error_patterns
        )

        for concept, count in error_counter.most_common(5):
            misconceptions.append({
                "concept": concept,
                "frequency": count,
                "severity": "high" if count > 3 else "medium"
            })

        return misconceptions

    def _extract_concept(self, message: str) -> str:
        """Extract the core concept from a student message."""
        # Simple extraction - could be enhanced with NLP
        message_lower = message.lower()

        # Check for common Latin concepts
        concepts = [
            "nominative", "genitive", "accusative", "ablative", "dative",
            "declension", "conjugation", "verb", "noun", "case",
            "gender", "number", "tense", "mood", "voice"
        ]

        for concept in concepts:
            if concept in message_lower:
                return concept

        return "general_understanding"

    def _identify_struggling_concepts(
        self,
        conversations: List[Dict[str, Any]],
        memory_summaries: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Identify concepts students struggle with."""
        struggling = []

        # Analyze memory summaries for "struggling" or "difficult" mentions
        for summary in memory_summaries:
            understanding_level = summary.get("understanding_level", "").lower()

            if understanding_level in ["beginner", "struggling"]:
                key_concepts = summary.get("key_concepts", "")
                struggling.append({
                    "concepts": key_concepts,
                    "understanding_level": understanding_level,
                    "how_learned": summary.get("how_learned", "")
                })

        # Count conversation turns per concept (more turns = more difficulty)
        concept_turns = self._count_concept_turns(conversations)

        for concept, turns in concept_turns.most_common(5):
            struggling.append({
                "concept": concept,
                "interaction_count": turns,
                "difficulty_indicator": "high" if turns > 10 else "medium"
            })

        return struggling

    def _count_concept_turns(
        self,
        conversations: List[Dict[str, Any]]
    ) -> Counter:
        """Count conversation turns per concept."""
        concept_turns = Counter()

        for conv in conversations:
            messages = conv.get("messages_json", [])

            for msg in messages:
                concept = self._extract_concept(msg.get("content", ""))
                concept_turns[concept] += 1

        return concept_turns

    def _identify_successful_strategies(
        self,
        memory_summaries: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Identify teaching strategies that worked well."""
        strategies = []

        for summary in memory_summaries:
            understanding = summary.get("understanding_level", "").lower()
            teaching_effectiveness = summary.get("teaching_effectiveness", "")

            if understanding in ["proficient", "advanced", "mastered"]:
                strategies.append({
                    "how_learned": summary.get("how_learned", ""),
                    "teaching_effectiveness": teaching_effectiveness,
                    "understanding_achieved": understanding
                })

        return strategies

    def _generate_recommendations(
        self,
        analysis: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate actionable curriculum improvement recommendations."""
        recommendations = []

        # Low completion rate
        if analysis["completion_rate"] < 0.7:
            recommendations.append({
                "type": "pacing",
                "priority": "high",
                "issue": f"Only {analysis['completion_rate']*100:.0f}% completion rate",
                "recommendation": "Consider breaking module into smaller chunks or reducing content density",
                "steel2_action": "reduce_day_content_density"
            })

        # Low average grade
        if analysis["average_grade"] in ["C", "C-", "D", "F"]:
            recommendations.append({
                "type": "difficulty",
                "priority": "high",
                "issue": f"Average grade is {analysis['average_grade']}",
                "recommendation": "Add more scaffolding and practice opportunities",
                "steel2_action": "add_guided_practice_steps"
            })

        # Common misconceptions
        if analysis["common_misconceptions"]:
            for misconception in analysis["common_misconceptions"][:2]:
                recommendations.append({
                    "type": "content",
                    "priority": "high",
                    "issue": f"Common error with {misconception['concept']}",
                    "recommendation": f"Add explicit teaching on {misconception['concept']} earlier in lesson",
                    "steel2_action": "add_misconception_prevention",
                    "target_concept": misconception['concept']
                })

        # Excessive time to mastery
        time_data = analysis["time_to_mastery"]
        if time_data["average_minutes"] > 60:
            recommendations.append({
                "type": "pacing",
                "priority": "medium",
                "issue": f"Takes {time_data['average_minutes']:.0f} min average to master",
                "recommendation": "Consider reducing scope or adding more efficient practice activities",
                "steel2_action": "optimize_lesson_duration"
            })

        return recommendations

    def generate_refinement_instructions(
        self,
        analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate specific instructions for Steel2 to refine curriculum.

        Returns:
            Dictionary with week number and specific changes to make
        """
        return {
            "week_number": analysis["module_id"],
            "analysis_summary": {
                "completion_rate": analysis["completion_rate"],
                "average_grade": analysis["average_grade"],
                "student_count": analysis["student_count"]
            },
            "modifications": [
                {
                    "target": rec.get("steel2_action"),
                    "reason": rec.get("issue"),
                    "priority": rec.get("priority")
                }
                for rec in analysis["improvement_recommendations"]
            ]
        }
