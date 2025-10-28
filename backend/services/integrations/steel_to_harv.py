"""
Steel2 → Harv Converter
Transforms Steel2 curriculum weeks into Harv teaching modules
"""
from typing import Dict, Any, List, Optional
from pathlib import Path
import json
import logging

logger = logging.getLogger(__name__)


class SteelToHarvConverter:
    """
    Converts Steel2 curriculum format to Harv module format.

    Steel2 Format (Input):
    - Week{XX}/internal_documents/week_spec.json
    - Week{XX}/Day{N}_{W}.{N}/*.txt, *.json, *.md
    - Week{XX}/internal_documents/week_summary.md

    Harv Format (Output):
    - Module with title, description, prompts, corpus
    - system_prompt: Socratic teaching instructions
    - module_prompt: Specific learning objectives
    - system_corpus: Knowledge base
    - module_corpus: Examples and exercises
    """

    def __init__(self, curriculum_base_path: Path):
        """
        Initialize converter.

        Args:
            curriculum_base_path: Path to Steel2 curriculum directory
        """
        self.curriculum_path = Path(curriculum_base_path)

    def convert_week_to_module(self, week_number: int) -> Dict[str, Any]:
        """
        Convert a Steel2 week to Harv module format.

        Args:
            week_number: Week number (1-35)

        Returns:
            Dictionary in Harv module format

        Raises:
            FileNotFoundError: If week data doesn't exist
            ValueError: If week data is invalid
        """
        week_path = self.curriculum_path / f"Week{week_number:02d}"

        if not week_path.exists():
            raise FileNotFoundError(f"Week {week_number} not found at {week_path}")

        logger.info(f"Converting Week {week_number} to Harv module")

        # Load week specification
        week_spec = self._load_week_spec(week_path)

        # Load week summary
        week_summary = self._load_week_summary(week_path)

        # Extract day activities
        day_activities = self._extract_day_activities(week_path, week_number)

        # Build Harv module
        module = {
            "id": week_number,
            "title": self._build_module_title(week_number, week_spec),
            "description": self._build_description(week_spec),
            "system_prompt": self._build_system_prompt(week_spec),
            "module_prompt": self._build_module_prompt(week_spec, day_activities),
            "system_corpus": self._build_system_corpus(week_spec),
            "module_corpus": self._build_module_corpus(day_activities),
            "learning_objectives": self._extract_learning_objectives(week_spec),
            "resources": self._extract_resources(week_spec),
            "metadata": {
                "source": "Steel2",
                "week_number": week_number,
                "grammar_focus": week_spec.get("grammar_focus", ""),
                "virtue": week_spec.get("faith_integration", {}).get("virtue", ""),
                "faith_phrase": week_spec.get("faith_integration", {}).get("faith_phrase", "")
            }
        }

        logger.info(f"✓ Successfully converted Week {week_number}")
        return module

    def _load_week_spec(self, week_path: Path) -> Dict[str, Any]:
        """Load week_spec.json from internal_documents."""
        spec_path = week_path / "internal_documents" / "week_spec.json"
        if not spec_path.exists():
            raise FileNotFoundError(f"Week spec not found: {spec_path}")

        with open(spec_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _load_week_summary(self, week_path: Path) -> str:
        """Load week_summary.md from internal_documents."""
        summary_path = week_path / "internal_documents" / "week_summary.md"
        if summary_path.exists():
            return summary_path.read_text(encoding='utf-8')
        return ""

    def _extract_day_activities(
        self,
        week_path: Path,
        week_number: int
    ) -> List[Dict[str, Any]]:
        """
        Extract activities from all 4 days.

        Returns:
            List of day dictionaries with activities
        """
        days = []

        for day_num in range(1, 5):  # Days 1-4
            day_name = f"Day{day_num}_{week_number}.{day_num}"
            day_path = week_path / day_name

            if not day_path.exists():
                logger.warning(f"Day path not found: {day_path}")
                continue

            day_data = {
                "day": day_num,
                "class_name": self._read_file(day_path / "01_class_name.txt"),
                "summary": self._read_file(day_path / "02_summary.md"),
                "grade_level": self._read_file(day_path / "03_grade_level.txt"),
                "guidelines": self._read_file(day_path / "05_guidelines_for_sparky.md"),
                "greeting": self._read_file(day_path / "07_sparkys_greeting.txt"),
            }

            # Extract teacher support documents
            doc_dir = day_path / "06_document_for_sparky"
            if doc_dir.exists():
                day_data["support_documents"] = self._extract_support_docs(doc_dir)

            days.append(day_data)

        return days

    def _read_file(self, file_path: Path) -> str:
        """Read text file, return empty string if not found."""
        try:
            return file_path.read_text(encoding='utf-8').strip()
        except FileNotFoundError:
            return ""

    def _extract_support_docs(self, doc_dir: Path) -> Dict[str, str]:
        """Extract all 6 teacher support documents."""
        docs = {}
        doc_files = [
            "01_vocabulary_list.md",
            "02_chant_guide.md",
            "03_spiral_review.md",
            "04_teacher_tips.md",
            "05_virtue_faith_integration.md",
            "06_weekly_topics.md"
        ]

        for doc_file in doc_files:
            doc_path = doc_dir / doc_file
            if doc_path.exists():
                key = doc_file.replace(".md", "").replace("0", "").replace("_", " ").title()
                docs[key] = doc_path.read_text(encoding='utf-8')

        return docs

    def _build_module_title(self, week_number: int, week_spec: Dict[str, Any]) -> str:
        """Build module title from week data."""
        title = week_spec.get("metadata", {}).get("title", "")
        if not title:
            title = week_spec.get("objectives", {}).get("grammar_focus", f"Week {week_number}")
        return f"Week {week_number}: {title}"

    def _build_description(self, week_spec: Dict[str, Any]) -> str:
        """Build module description."""
        grammar = week_spec.get("objectives", {}).get("grammar_focus", "")
        return f"This week focuses on {grammar}"

    def _build_system_prompt(self, week_spec: Dict[str, Any]) -> str:
        """
        Build Harv system_prompt from Steel2 data.

        The system prompt defines Sparky's Socratic teaching behavior.
        """
        virtue = week_spec.get("faith_integration", {}).get("virtue", "")
        faith_phrase = week_spec.get("faith_integration", {}).get("faith_phrase", "")

        return f"""You are Sparky, an AI Latin tutor using the Socratic method.

**Teaching Philosophy:**
- Guide students to discover knowledge through strategic questions
- Never give direct answers initially—ask leading questions instead
- Encourage critical thinking and pattern recognition
- Celebrate small victories and progress

**This Week's Focus:**
{week_spec.get('objectives', {}).get('grammar_focus', '')}

**Virtue Integration:**
Weave {virtue} into discussions naturally. Reference the faith phrase "{faith_phrase}" when appropriate.

**Approach:**
1. Start with what they know (prior knowledge)
2. Ask guiding questions that reveal patterns
3. Let them make connections
4. Confirm and celebrate discoveries
5. Provide practice opportunities

**Tone:**
Encouraging, patient, enthusiastic about Latin. Use age-appropriate language for grades 3-5.
"""

    def _build_module_prompt(
        self,
        week_spec: Dict[str, Any],
        day_activities: List[Dict[str, Any]]
    ) -> str:
        """Build module_prompt with specific learning sequence."""
        objectives = week_spec.get("objectives", {}).get("skill_goals", [])

        prompt = f"""**Learning Sequence for this Week:**

**Day 1 - Discovery:**
{day_activities[0].get('summary', 'Introduction to new concepts') if day_activities else ''}

**Day 2 - Reinforcement:**
{day_activities[1].get('summary', 'Practice and reinforcement') if len(day_activities) > 1 else ''}

**Day 3 - Integration:**
{day_activities[2].get('summary', 'Integration with prior knowledge') if len(day_activities) > 2 else ''}

**Day 4 - Assessment:**
{day_activities[3].get('summary', 'Mastery check') if len(day_activities) > 3 else ''}

**Mastery Goals:**
"""
        for obj in objectives:
            prompt += f"\n- {obj}"

        return prompt

    def _build_system_corpus(self, week_spec: Dict[str, Any]) -> str:
        """Build knowledge base from week spec."""
        corpus_parts = []

        # Grammar focus
        grammar = week_spec.get("grammar_focus", "")
        if grammar:
            corpus_parts.append(f"**Grammar Focus:**\n{grammar}")

        # Vocabulary
        vocab = week_spec.get("vocabulary", {}).get("core_items", [])
        if vocab:
            vocab_str = ", ".join(vocab)
            corpus_parts.append(f"**Core Vocabulary:**\n{vocab_str}")

        # Faith integration
        faith = week_spec.get("faith_integration", {})
        if faith:
            corpus_parts.append(f"**Virtue:** {faith.get('virtue', '')}")
            corpus_parts.append(f"**Faith Phrase:** {faith.get('faith_phrase', '')}")

        return "\n\n".join(corpus_parts)

    def _build_module_corpus(self, day_activities: List[Dict[str, Any]]) -> str:
        """Build examples and exercises from day activities."""
        corpus_parts = []

        for day in day_activities:
            day_num = day.get("day", 0)
            corpus_parts.append(f"### Day {day_num}: {day.get('class_name', '')}")

            # Add summary
            if day.get("summary"):
                corpus_parts.append(day["summary"])

            # Add support documents
            support_docs = day.get("support_documents", {})
            for doc_name, doc_content in support_docs.items():
                if doc_content:
                    corpus_parts.append(f"**{doc_name}:**\n{doc_content[:500]}...")  # Truncate for brevity

            corpus_parts.append("")  # Blank line between days

        return "\n".join(corpus_parts)

    def _extract_learning_objectives(self, week_spec: Dict[str, Any]) -> List[str]:
        """Extract structured learning objectives."""
        return week_spec.get("objectives", {}).get("skill_goals", [])

    def _extract_resources(self, week_spec: Dict[str, Any]) -> List[str]:
        """Extract required resources/materials."""
        # TODO: Extract from week spec if available
        return [
            "Whiteboard or digital display",
            "Latin vocabulary flashcards",
            "Chant reference sheet",
            "Student workbooks"
        ]

    def convert_all_weeks(
        self,
        start_week: int = 1,
        end_week: int = 35
    ) -> Dict[int, Dict[str, Any]]:
        """
        Convert multiple weeks to Harv modules.

        Args:
            start_week: Starting week number
            end_week: Ending week number

        Returns:
            Dictionary mapping week number to module data
        """
        modules = {}

        for week in range(start_week, end_week + 1):
            try:
                module = self.convert_week_to_module(week)
                modules[week] = module
                logger.info(f"✓ Converted Week {week}")
            except Exception as e:
                logger.error(f"✗ Failed to convert Week {week}: {e}")
                continue

        logger.info(f"Converted {len(modules)} out of {end_week - start_week + 1} weeks")
        return modules
