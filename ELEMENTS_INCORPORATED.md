# HARV SHIPPED - Explicit Elements Incorporated from Each System

Comprehensive breakdown of what was taken from Steel2, Doc Digester, and Harv.

---

## 🔵 FROM STEEL2 (Latin A Curriculum Generator)

### ✅ **Already Incorporated in Foundation**

#### **Conceptual Elements**
1. **Two-Phase Generation Architecture**
   - Phase 1: Week planning (internal_documents/)
   - Phase 2: Day generation (4 days per week)
   - Used in: Integration planning, quality loop design

2. **File Structure & Organization**
   - `Week{XX}/` directory structure
   - `internal_documents/` concept (week_spec.json, week_summary.md)
   - `Day{N}_{W}.{N}/` naming convention
   - Used in: `steel_to_harv.py` converter

3. **7-Field Day Structure**
   - 01_class_name.txt
   - 02_summary.md
   - 03_grade_level.txt
   - 04_role_context.json
   - 05_guidelines_for_sparky.md
   - 06_document_for_sparky/ (6 teacher docs)
   - 07_sparkys_greeting.txt
   - **Mapped to**: Harv module fields in converter

4. **Prior Knowledge Digest System** (Designed but TODO in Steel2)
   - Structure: `07_prior_knowledge_digest.json`
   - Fields: vocabulary_recycled[], grammar_recycled[], chant_recycled[]
   - **Incorporated in**: `harv_to_steel.py` feedback analysis

5. **Curriculum Outline Structure**
   - 35 weeks total
   - Grammar progression sequence
   - Spiral learning concept (≥25%)
   - Used in: Configuration (TOTAL_WEEKS=35)

6. **Validation Rules**
   - Spiral learning enforcement (25% minimum)
   - Grammar focus consistency
   - Day 4 assessment requirements
   - Used in: `quality_loop.py` validation phase

7. **Configuration Parameters**
   - `TOTAL_WEEKS = 35`
   - `DAYS_PER_WEEK = 4`
   - `MAX_RETRIES = 10`
   - **Location**: `backend/app/config.py`

#### **Data Formats**
1. **week_spec.json Structure**
   ```python
   {
       "metadata": {"week": int, "title": str},
       "objectives": {"grammar_focus": str, "skill_goals": []},
       "vocabulary": {"core_items": []},
       "grammar_focus": str,
       "faith_integration": {
           "virtue": str,
           "faith_phrase": str,
           "scripture": str
       },
       "spiral_links": {"prior_weeks_referenced": []},
       "assessment": {"day4_focus": str}
   }
   ```
   - **Used by**: `SteelToHarvConverter._load_week_spec()`

2. **Day Activity Structure**
   - class_name (student-facing title)
   - summary (lesson overview)
   - guidelines (teaching instructions)
   - support_documents (6 teacher files)
   - **Mapped to**: Harv corpus in converter

3. **Virtue & Faith Integration**
   - Catholic classical education focus
   - Weekly virtue themes
   - Latin faith phrases
   - **Preserved in**: Module metadata

### 📋 **Planned to Copy (Not Yet Done)**

#### **Core Modules** (from `steel2/src/services/`)
1. **generator_week.py** (~400 lines)
   - `generate_week_spec_from_outline()`
   - `generate_week_summary()`
   - LLM-based week planning
   - **Target**: `backend/services/curriculum_generator/`

2. **generator_day.py** (~800 lines)
   - `generate_day()` main function
   - 7-field generation with retries
   - Subject validation (Latin vs other subjects)
   - Spiral learning injection
   - **Target**: `backend/services/curriculum_generator/`

3. **llm_client.py** (~250 lines)
   - `LLMClient` class
   - OpenAI API integration
   - Retry logic with exponential backoff
   - JSON schema enforcement
   - **Target**: `backend/services/curriculum_generator/`

4. **validator.py** (~400 lines)
   - `validate_day()` function
   - Schema validation (Pydantic)
   - Spiral learning checks
   - Grammar consistency checks
   - **Target**: `backend/services/curriculum_generator/`

5. **storage.py** (~300 lines)
   - `week_dir()`, `day_dir()` path helpers
   - `internal_doc_path()` for planning docs
   - `read_json()`, `write_json()` utilities
   - File-based curriculum storage
   - **Target**: `backend/services/curriculum_generator/`

6. **curriculum_outline.py** (~200 lines)
   - `load_curriculum_outline()`
   - Week-by-week scope & sequence
   - Grammar progression tracking
   - **Target**: `backend/services/curriculum_generator/`

7. **exporter.py** (~150 lines)
   - ZIP export with SHA-256 hashing
   - `manifest.json` generation
   - Week packaging for distribution
   - **Target**: `backend/services/curriculum_generator/`

#### **Prompt System** (from `steel2/src/services/prompts/`)
All prompt templates and task functions:
1. **week/week_spec.json** - Week planning prompt
2. **week/week_summary.json** - Summary generation prompt
3. **day/day_summary.json** - Day summary prompt
4. **day/role_context.json** - Sparky persona prompt
5. **day/guidelines.json** - Teaching guidelines prompt
6. **day/day_document.json** - Main lesson document prompt
7. **day/greeting.json** - Sparky greeting prompt
8. **digest/prior_knowledge_digest.json** - Spiral learning prompt
9. **kit_tasks.py** (~3,000 lines) - All task functions
   - `task_week_spec()`
   - `task_week_summary()`
   - `task_day_summary()`
   - `task_role_context()`
   - `task_guidelines()`
   - `task_day_document()`
   - `task_greeting()`
   - `task_prior_knowledge_digest()`
   - **Target**: `backend/services/curriculum_generator/prompts/`

#### **Data Models** (from `steel2/src/models/`)
1. **schemas_day.py** (~120 lines)
   - `DayMetadata` - Lesson metadata
   - `LessonStep` - Individual lesson steps
   - `BehaviorProfile` - Sparky's teaching behavior
   - `DayObjectives` - Learning objectives
   - `DaySpiralLinks` - Prior knowledge connections
   - `DayDocument` - Complete lesson plan
   - Validators: `validate_spiral_opening()`, `validate_digest_length()`
   - **Target**: `backend/services/curriculum_generator/models.py`

#### **Configuration** (from `steel2/`)
1. **curriculum_outline.json** (~20KB)
   - Complete 35-week scope & sequence
   - Grammar focus per week
   - Session durations
   - Vocabulary counts
   - **Target**: `backend/data/curriculum_outline.json`

### ❌ **Explicitly NOT Incorporated**
1. **Anthropic/Claude Support** - OpenAI GPT-4o only
2. **Multi-model support** - Single provider initially
3. **Complex validation chains** - Simplified for MVP
4. **Budget enforcement** - Tracking only, no hard limits
5. **Phase 0 research** - Simplified prompt approach

---

## 🟢 FROM DOC DIGESTER (Educational Content Analyzer)

### ✅ **Already Incorporated in Foundation**

#### **Conceptual Elements**
1. **5-Phase Analysis Pipeline**
   - Phase 1: Comprehension Pass (WHO/WHAT/WHEN/WHY/HOW)
   - Phase 2: Structural Outline (hierarchical structure)
   - Phase 3: Propositional Extraction (truth claims)
   - Phase 4: Analytical Metadata (curriculum context)
   - Phase 5: Pedagogical Mapping (teaching elements)
   - **Used in**: `digester_to_steel.py` pattern extraction

2. **Pattern Extraction Methodology**
   - Lesson flow templates from structural outline
   - Assessment patterns from pedagogical mapping
   - Teaching strategies from student activities
   - Concept progressions from propositions
   - **Implemented in**: `DigesterToSteelExtractor` class

3. **Temporal Analysis Concept**
   - Historical vs contemporary examples
   - Content staleness detection
   - Update priority calculation
   - **Used in**: Pattern library metadata

4. **Evidence Pointers System**
   - Bidirectional traceability to source
   - Section/subsection references
   - Location markers
   - **Concept used in**: Quality validation

#### **Data Structures**
1. **Structural Outline Format**
   ```python
   {
       "chapter_title": str,
       "outline": [
           {
               "section_title": str,
               "pedagogical_purpose": str,
               "rhetorical_mode": str,  # expository/narrative/analytical
               "subtopics": [
                   {
                       "subtopic_title": str,
                       "key_concepts": [],
                       "supporting_examples": [],
                       "student_discussion_prompts": []
                   }
               ]
           }
       ]
   }
   ```
   - **Extracted to**: Lesson flow templates

2. **Pedagogical Mapping Format**
   ```python
   {
       "learning_objectives": [],
       "student_activities": [
           {
               "activity_type": str,
               "description": str,
               "location": str
           }
       ],
       "assessment_questions": [
           {
               "question": str,
               "question_type": str,
               "location": str
           }
       ],
       "temporal_analysis": {
           "historical_examples": [],
           "contemporary_examples": [],
           "temporal_range": str
       }
   }
   ```
   - **Extracted to**: Teaching strategies, assessment patterns

3. **Propositional Extraction Format**
   ```python
   {
       "propositions": [
           {
               "id": str,
               "truth_type": str,  # descriptive/analytical/normative
               "statement": str,
               "implication_for_learning": str,
               "connections_to_other_chapters": []
           }
       ]
   }
   ```
   - **Extracted to**: Concept progressions

#### **Processing Logic**
1. **Pattern Extraction Functions**
   - `_extract_lesson_flow()` - Structural outline → lesson templates
   - `_extract_assessment_patterns()` - Questions → question types
   - `_extract_teaching_strategies()` - Activities → strategy classification
   - `_extract_concept_progressions()` - Propositions → concept chains
   - `_extract_activity_structures()` - Activities → structure templates
   - **Location**: `digester_to_steel.py` (lines 47-280)

2. **Classification Logic**
   - `_infer_step_type()` - Maps activity description to lesson step type
   - `_infer_cognitive_level()` - Maps question type to Bloom's taxonomy
   - `_classify_teaching_mode()` - Identifies Socratic/discovery/direct instruction
   - **Location**: `digester_to_steel.py`

3. **Pattern Deduplication**
   - `_deduplicate_patterns()` - Removes duplicate patterns by similarity
   - Frequency-based ranking
   - **Location**: `digester_to_steel.py` (lines 260-280)

### 📋 **Planned to Copy (Not Yet Done)**

#### **Core Modules** (from `doc_digester/src/services/`)
1. **orchestrator.py** (~300 lines)
   - `digest_chapter()` main function
   - 5-phase sequential processing
   - Retry logic per phase
   - Validation between phases
   - **Target**: `backend/services/content_analyzer/`

2. **phase_processors.py** (assumed, or split across files)
   - Phase 1: `process_comprehension_pass()`
   - Phase 2: `process_structural_outline()`
   - Phase 3: `process_propositional_extraction()`
   - Phase 4: `process_analytical_metadata()`
   - Phase 5: `process_pedagogical_mapping()`
   - **Target**: `backend/services/content_analyzer/`

3. **validators.py**
   - Pydantic schema validation
   - JSON Schema validation (Draft 2020-12)
   - Phase-specific validators
   - **Target**: `backend/services/content_analyzer/`

4. **schemas.py**
   - Pydantic models for all 5 phases
   - `ComprehensionPass` model
   - `StructuralOutline` model
   - `PropositionExtraction` model
   - `AnalyticalMetadata` model
   - `PedagogicalMapping` model
   - **Target**: `backend/services/content_analyzer/`

#### **LLM Integration** (from `doc_digester/src/services/`)
1. **openai_client.py**
   - Structured JSON output enforcement
   - Retry logic with exponential backoff
   - Temperature-specific calls per phase
   - **Target**: Merge with Steel2's llm_client.py

#### **File Processing** (from `doc_digester/src/`)
1. **Document Extraction**
   - `.txt` file reader (UTF-8, Latin-1)
   - `.docx` processor (python-docx)
   - `.pdf` processor (PyPDF2)
   - Encoding detection
   - **Target**: `backend/services/content_analyzer/`

#### **Configuration**
1. **Phase-specific settings**
   - Temperature per phase (0.15-0.25)
   - Max tokens per phase (1600-16000)
   - **Target**: `backend/app/config.py`

2. **File handling settings**
   - `MAX_FILE_SIZE_MB = 100`
   - `SUPPORTED_FORMATS = "txt,docx,pdf"`
   - **Already in**: `backend/app/config.py`

### ❌ **Explicitly NOT Incorporated**
1. **Complex HTML to markdown conversion** - Direct text only
2. **Advanced NLP analysis** - Pattern matching sufficient
3. **Multi-document batch processing UI** - CLI focused
4. **Web scraping capabilities** - File upload only

---

## 🟠 FROM HARV (AI Socratic Tutoring Platform)

### ✅ **Already Incorporated in Foundation**

#### **Conceptual Elements**
1. **Module-Based Teaching Structure**
   - Modules as teaching units
   - system_prompt (Socratic instructions)
   - module_prompt (learning objectives)
   - system_corpus (knowledge base)
   - module_corpus (examples/exercises)
   - **Used in**: `steel_to_harv.py` converter output format

2. **4-Layer Memory System Concept** (Simplified to 2-layer for MVP)
   - Layer 1: User profile & learning style
   - Layer 2: Module context
   - Layer 3: Conversation history (simplified)
   - Layer 4: Prior knowledge (deferred)
   - **Referenced in**: Architecture design, future enhancement

3. **Socratic Teaching Method**
   - Questions over answers
   - Guided discovery
   - Strategic questioning
   - **Embedded in**: `steel_to_harv.py` system_prompt generation

4. **Analytics-Driven Feedback**
   - Completion rates
   - Grade tracking
   - Time to mastery
   - Common misconceptions
   - **Implemented in**: `harv_to_steel.py` feedback analyzer

5. **Student Progress Tracking**
   - Module completion status
   - Letter grade assignments
   - Time spent per module
   - Attempt counts
   - **Used in**: `HarvToSteelFeedback.analyze_module_performance()`

#### **Data Structures**
1. **Module Format**
   ```python
   {
       "id": int,
       "title": str,
       "description": str,
       "system_prompt": str,  # Socratic teaching instructions
       "module_prompt": str,  # Learning objectives
       "system_corpus": str,  # Knowledge base
       "module_corpus": str,  # Examples & exercises
       "learning_objectives": [],
       "resources": []
   }
   ```
   - **Output of**: `SteelToHarvConverter`

2. **Conversation Format**
   ```python
   {
       "id": int,
       "user_id": int,
       "module_id": int,
       "messages_json": [
           {"role": "user", "content": str, "timestamp": str},
           {"role": "assistant", "content": str, "timestamp": str}
       ],
       "current_grade": str,
       "finalized": bool
   }
   ```
   - **Analyzed by**: `harv_to_steel.py` misconception detection

3. **User Progress Format**
   ```python
   {
       "user_id": int,
       "module_id": int,
       "completed": bool,
       "grade": str,  # Letter grade
       "time_spent": int,  # Minutes
       "attempts": int,
       "completion_date": datetime
   }
   ```
   - **Used in**: `HarvToSteelFeedback._calculate_completion_rate()`

4. **Memory Summary Format**
   ```python
   {
       "user_id": int,
       "module_id": int,
       "what_learned": str,
       "how_learned": str,
       "key_concepts": str,
       "learning_insights": str,
       "understanding_level": str  # beginner/proficient/advanced
   }
   ```
   - **Used in**: `HarvToSteelFeedback._identify_struggling_concepts()`

#### **Analysis Logic**
1. **Performance Metrics**
   - `_calculate_completion_rate()` - % students completed
   - `_calculate_average_grade()` - Letter grade to GPA conversion
   - `_calculate_time_to_mastery()` - Average & median time
   - **Location**: `harv_to_steel.py` (lines 60-135)

2. **Misconception Detection**
   - `_identify_misconceptions()` - Pattern matching in conversations
   - Correction language detection ("actually", "not quite")
   - Frequency counting and ranking
   - **Location**: `harv_to_steel.py` (lines 140-185)

3. **Concept Difficulty Analysis**
   - `_identify_struggling_concepts()` - Low understanding levels
   - `_count_concept_turns()` - Interaction count per concept
   - Difficulty indicators (high/medium/low)
   - **Location**: `harv_to_steel.py` (lines 190-245)

4. **Recommendation Generation**
   - `_generate_recommendations()` - Actionable curriculum fixes
   - Priority assignment (high/medium/low)
   - Steel2-ready action codes
   - **Location**: `harv_to_steel.py` (lines 280-340)

### 📋 **Planned to Copy (Not Yet Done)**

#### **Decision: Use Harv Simple (Not Full Harv_2)**
- Source: `/Users/elle_jansick/harv_demo/harv_simple/`
- Rationale: 82% less code, 3-minute setup, easier to understand
- Trade-off: 2-layer memory instead of 4-layer (acceptable for MVP)

#### **Core Modules** (from `harv_demo/harv_simple/backend/`)
1. **main.py** (~500 lines)
   - FastAPI app setup
   - All endpoints in single file (simple version)
   - `/auth/register`, `/auth/login`
   - `/chat`, `/modules`, `/progress`
   - **Target**: Split into separate routers in `backend/api/`

2. **models.py** (~50 lines - Simple version)
   - `User` model (3 fields: id, email, hashed_password)
   - `Module` model (7 fields: id, title, description, prompts, corpus)
   - `Conversation` model (5 fields: id, user_id, module_id, messages, grade)
   - **Target**: `backend/app/models.py` (expand to 5-6 tables)

3. **auth.py** (~65 lines)
   - `create_access_token()` - JWT generation
   - `get_password_hash()` - Bcrypt hashing
   - `verify_password()` - Password checking
   - `get_current_user()` - JWT verification
   - **Target**: `backend/app/auth.py`

#### **Frontend** (from `harv_demo/harv_simple/frontend/`)
1. **index.html** (~150 lines)
   - Main SPA structure
   - Navigation
   - Module list view
   - Chat interface
   - **Target**: `frontend/index.html` (expand with pipeline dashboard)

2. **app.js** (~580 lines)
   - API client
   - Chat handler
   - Module management
   - Authentication flow
   - **Target**: `frontend/js/tutor-interface.js`

3. **styles.css** (~765 lines)
   - Dark mode support
   - Responsive design
   - Chat bubbles
   - Module cards
   - **Target**: `frontend/css/unified-styles.css`

#### **Database Schema**
From Harv Simple (3 tables):
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    hashed_password TEXT NOT NULL
);

CREATE TABLE modules (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    system_prompt TEXT,
    module_prompt TEXT,
    system_corpus TEXT,
    module_corpus TEXT
);

CREATE TABLE conversations (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    module_id INTEGER,
    messages_json TEXT,  -- JSON array
    current_grade TEXT,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (module_id) REFERENCES modules (id)
);
```

**Expand to 6 tables in HARV SHIPPED**:
- Keep: `users`, `modules`, `conversations`
- Add: `user_progress`, `memory_summaries`, `pattern_library`

### ❌ **Explicitly NOT Incorporated from Full Harv_2**
1. **4-Layer Memory System** - Simplified to 2-layer for MVP
2. **Multi-Provider AI Support** - OpenAI only initially
3. **Complex Analytics Dashboard** - Basic metrics only
4. **12 Database Tables** - Reduced to 6 tables
5. **10+ Admin Pages** - Simplified to 4-5 pages
6. **Classes/Enrollment System** - Single course focus
7. **Onboarding Surveys** - Simplified registration

---

## 🆕 NEW ELEMENTS (Created for HARV SHIPPED)

### **Integration Layer** (100% Original)
1. **`SteelToHarvConverter` class** (~300 lines)
   - Week → Module transformation logic
   - Field mapping algorithms
   - Batch conversion support
   - **Location**: `steel_to_harv.py`

2. **`DigesterToSteelExtractor` class** (~330 lines)
   - 5-phase analysis → pattern extraction
   - Teaching strategy classification
   - Cognitive level inference
   - Pattern library builder
   - **Location**: `digester_to_steel.py`

3. **`HarvToSteelFeedback` class** (~350 lines)
   - Student analytics → curriculum recommendations
   - Misconception detection algorithms
   - Difficulty calculation logic
   - Refinement instruction generator
   - **Location**: `harv_to_steel.py`

4. **`QualityAssuranceLoop` class** (~420 lines)
   - Complete cycle orchestration
   - Auto-validation pipeline
   - Auto-import workflow
   - Feedback collection automation
   - Batch processing support
   - Quality report generation
   - **Location**: `quality_loop.py`

### **Unified Configuration**
1. **`Settings` class** (~150 lines)
   - Combines all three systems' config
   - Feature flags for automation
   - Quality thresholds
   - Budget tracking setup
   - **Location**: `backend/app/config.py`

### **Documentation**
1. **Integration architecture diagrams**
2. **Data flow specifications**
3. **API endpoint designs**
4. **Implementation roadmap**

---

## 📊 SUMMARY TABLE

| Source System | Files/Modules | Lines of Code | Elements Used | Status |
|---------------|---------------|---------------|---------------|--------|
| **Steel2** | 15 modules | ~5,000 lines | Architecture, data formats, validation | ✓ Conceptual, ⏳ Code copy pending |
| **Doc Digester** | 8 modules | ~2,500 lines | 5-phase pipeline, pattern extraction | ✓ Conceptual, ⏳ Code copy pending |
| **Harv Simple** | 3 modules | ~1,750 lines | Module structure, analytics, chat | ✓ Conceptual, ⏳ Code copy pending |
| **NEW (Integration)** | 4 modules | ~1,400 lines | Converters, extractors, feedback, QA loop | ✅ Complete |
| **NEW (Config/Docs)** | 5 files | ~2,000 lines | Unified config, documentation | ✅ Complete |
| **TOTAL PLANNED** | 35 modules | ~12,650 lines | Complete unified platform | 🔄 60% architecture, 40% implementation |

---

## 🎯 IMPLEMENTATION PRIORITY

### **Phase 1: Core Systems (Week 1)**
Copy 26 files, ~9,250 lines:
- Steel2: 15 files (~5,000 lines)
- Doc Digester: 8 files (~2,500 lines)
- Harv Simple: 3 files (~1,750 lines)

### **Phase 2: API Layer (Week 2)**
Create 5 new routers, ~1,500 lines:
- `curriculum.py` (~300 lines)
- `analysis.py` (~300 lines)
- `tutoring.py` (~300 lines)
- `pipeline.py` (~400 lines)
- `analytics.py` (~200 lines)

### **Phase 3: Database & Frontend (Week 3)**
- Models expansion (~200 lines)
- Frontend dashboard (~2,000 lines)

### **Phase 4: Testing & Deployment (Week 4)**
- Test suite (~1,000 lines)
- Docker config (~100 lines)
- CI/CD (~200 lines)

**Total Target**: ~14,300 lines of production code

---

**Current Status**: Foundation complete with 1,400 lines of NEW integration code that connects everything.

**Next Step**: Copy the 26 core files from source systems (9,250 lines).
