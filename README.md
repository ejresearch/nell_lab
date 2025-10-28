# 🚀 HARV SHIPPED: Unified Educational Technology Platform

**Version 1.0.0** | A self-improving curriculum generation, analysis, and delivery ecosystem

---

## 🎯 Vision

HARV SHIPPED is a comprehensive educational technology platform that combines three powerful systems into one unified pipeline:

1. **Content Analysis** (from Doc Digester) - Extract pedagogical intelligence from existing materials
2. **Curriculum Generation** (from Steel2) - AI-powered curriculum creation with quality validation
3. **AI Tutoring Delivery** (from Harv) - Personalized Socratic teaching with 4-layer memory

Together, these create a **self-improving educational ecosystem** where:
- Reference materials inform generation
- Generated curriculum is automatically validated
- Student learning data drives continuous improvement
- Quality increases with every iteration

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    HARV SHIPPED ECOSYSTEM                        │
└─────────────────────────────────────────────────────────────────┘

PHASE 1: ANALYZE                 PHASE 2: GENERATE               PHASE 3: DELIVER
─────────────────                ─────────────────               ─────────────────
Reference Materials              Pattern Library                 Live AI Tutoring
      ↓                                ↓                               ↓
Content Analyzer        →        Curriculum Generator     →      AI Tutor Platform
(Doc Digester)                   (Steel2)                        (Harv)
      ↓                                ↓                               ↓
Pedagogical Patterns             35-Week Curriculum              Student Learning Data
                                       ↓                               ↓
                                 Quality Validation          ←─────────┘
                                 (Doc Digester)                  Feedback Loop
```

---

## ✨ Key Features

### 🔍 Content Analysis Engine
- 5-phase deep analysis of educational materials
- Extract pedagogical patterns, teaching strategies, assessment types
- Identify learning objectives and concept progressions
- Temporal analysis for content maintenance
- **Output**: Structured JSON analysis ready for curriculum generation

### 📚 Curriculum Generation
- AI-powered 35-week Latin A curriculum (extensible to any subject)
- Two-phase generation: Week planning → Day creation
- Automatic spiral learning enforcement (≥25%)
- Virtue and faith integration
- Prior knowledge digest system
- **Output**: Complete lesson plans with activities, assessments, teacher support

### 🎓 AI Tutoring Platform
- Socratic method teaching (questions over answers)
- 4-layer dynamic memory system
- Personalized to student learning style
- Cross-module knowledge continuity
- Real-time analytics and progress tracking
- **Output**: Deep student understanding through guided discovery

### 🔄 Integration Layer (NEW)
- **Steel → Harv**: Auto-import generated curriculum as modules
- **Digester → Steel**: Feed pedagogical patterns to generators
- **Harv → Steel**: Return student data for curriculum improvement
- **Quality Loop**: Automated validation pipeline
- **Dashboard**: Unified view of entire ecosystem health

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- OpenAI API key
- 2GB disk space
- Modern web browser

### One-Command Setup

```bash
cd harv_shipped
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# Option 1: Docker (recommended)
docker-compose up -d

# Option 2: Manual
pip install -r requirements.txt
python backend/app/main.py
```

Visit: http://localhost:8000

---

## 📖 Core Workflows

### Workflow 1: Create New Curriculum from Reference Materials

```bash
# 1. Analyze reference textbook
curl -X POST http://localhost:8000/api/analyze \
  -F file=@wheelock_chapter5.txt

# 2. Extract patterns for generation
curl -X POST http://localhost:8000/api/pipeline/extract-patterns \
  -d '{"analysis_id": "ch-abc123"}'

# 3. Generate curriculum using patterns
curl -X POST http://localhost:8000/api/curriculum/generate \
  -d '{"weeks": [5], "use_patterns": true}'

# 4. Auto-import to tutoring platform
curl -X POST http://localhost:8000/api/pipeline/import-to-harv \
  -d '{"week": 5}'

# Result: Complete Week 5 curriculum ready for students in 10 minutes
```

### Workflow 2: Quality Assurance Loop

```bash
# 1. Generate new week
POST /api/curriculum/generate {"weeks": [16]}

# 2. Auto-validate with analyzer
POST /api/pipeline/validate {"week": 16}

# 3. View quality report
GET /api/pipeline/quality-report/16

# 4. Regenerate if needed
POST /api/curriculum/regenerate {"week": 16, "fixes": ["add_virtue_integration"]}

# Result: High-quality, validated curriculum
```

### Workflow 3: Student-Driven Improvement

```bash
# 1. Students work through Module 5 in Harv
# (Happens via web UI at http://localhost:8000/tutoring)

# 2. Export student analytics
GET /api/tutoring/analytics/module/5

# 3. Identify improvement opportunities
POST /api/pipeline/analyze-feedback {"module": 5}

# 4. Refine curriculum based on data
POST /api/curriculum/refine {"week": 5, "feedback_id": "fb-xyz"}

# Result: Next cohort gets improved curriculum
```

---

## 🗂️ Project Structure

```
harv_shipped/
├── backend/
│   ├── app/                     # FastAPI application
│   ├── services/
│   │   ├── curriculum_generator/    # Steel2 core
│   │   ├── content_analyzer/        # Doc Digester core
│   │   ├── ai_tutor/                # Harv core
│   │   └── integrations/            # NEW - Unified layer
│   └── api/                     # REST endpoints
│
├── frontend/                    # Unified web interface
│   ├── pages/
│   │   ├── curriculum/          # Curriculum management UI
│   │   ├── analysis/            # Content analysis UI
│   │   ├── tutoring/            # Student tutoring UI
│   │   └── pipeline/            # Pipeline dashboard (NEW)
│   └── js/
│       └── pipeline-dashboard.js # Ecosystem overview
│
└── data/
    ├── curriculum/              # Generated curriculum
    ├── analyzed_content/        # Analysis outputs
    └── harv.db                  # Unified database
```

---

## 🔗 API Endpoints

### Content Analysis
- `POST /api/analyze` - Analyze educational content
- `GET /api/analysis/{id}` - Retrieve analysis
- `POST /api/pipeline/extract-patterns` - Extract patterns for generation

### Curriculum Generation
- `POST /api/curriculum/generate` - Generate weeks
- `GET /api/curriculum/week/{id}` - View generated week
- `POST /api/curriculum/refine` - Improve based on feedback

### AI Tutoring
- `POST /api/tutoring/chat` - Student chat interface
- `GET /api/tutoring/modules` - List all modules
- `GET /api/tutoring/analytics/module/{id}` - Module analytics

### Pipeline Integration (NEW)
- `POST /api/pipeline/import-to-harv` - Import curriculum to tutoring
- `POST /api/pipeline/validate` - Run quality validation
- `GET /api/pipeline/quality-report/{week}` - View QA results
- `GET /api/pipeline/status` - Ecosystem health dashboard
- `POST /api/pipeline/full-cycle` - Run complete pipeline

---

## 💡 Use Cases

### For Curriculum Developers
1. Analyze competitor textbooks for best practices
2. Generate complete curriculum in hours (not months)
3. Validate quality automatically
4. Export to any format

### For Educational Institutions
1. Deploy complete AI tutoring platform
2. Track student progress across entire curriculum
3. Identify struggling concepts automatically
4. Continuously improve based on real student data

### For Researchers
1. Extract pedagogical patterns from historical materials
2. Compare teaching strategies across different approaches
3. A/B test curriculum variations
4. Measure learning outcomes

---

## 📊 Integration Benefits

| Feature | Standalone Systems | HARV SHIPPED Integration |
|---------|-------------------|-------------------------|
| **Quality Assurance** | Manual review | Automated validation pipeline |
| **Pattern Learning** | Manual extraction | AI-powered pattern library |
| **Student Feedback** | Surveys, manual | Real-time analytics integration |
| **Deployment Time** | Hours/days | Minutes (auto-import) |
| **Improvement Cycle** | Weeks/months | Continuous (every cohort) |
| **Cross-Subject Scaling** | Recreate from scratch | Reuse patterns & infrastructure |

---

## 🎓 Example: Week 5 Complete Lifecycle

```
Day 1: Reference Analysis
────────────────────────
Upload: Wheelock Chapter 5 (2nd Declension)
Result: Pedagogical patterns extracted (3 minutes)

Day 1: Curriculum Generation
────────────────────────────
Generate: Week 5 using patterns
Result: 4 complete days with activities (5 minutes)

Day 1: Quality Validation
─────────────────────────
Auto-validate: Structure, objectives, spiral learning
Result: Quality score 9.2/10, 2 minor improvements suggested

Day 1: Deployment
────────────────
Auto-import: Week 5 → Harv Module 5
Result: Ready for students

Week 1-2: Student Learning
──────────────────────────
15 students complete Module 5
Analytics: 35% struggle with ablative case

Week 3: Improvement
──────────────────
System auto-suggests: Add ablative drills
Regenerate: Week 5 Day 3 with improvements
Next cohort: 68% success rate (up from 35%)
```

---

## 🛠️ Technology Stack

### Backend
- **FastAPI** - Modern async web framework
- **SQLAlchemy** - ORM for database operations
- **Pydantic** - Data validation
- **OpenAI API** - GPT-4o for AI generation
- **JWT** - Authentication

### Frontend
- **Vanilla JavaScript** - No framework dependencies
- **Chart.js** - Data visualizations
- **CSS Variables** - Dynamic theming

### Database
- **SQLite** - Development (embedded)
- **PostgreSQL** - Production (recommended)

---

## 📚 Documentation

- [Architecture Guide](docs/ARCHITECTURE.md) - System design deep-dive
- [API Reference](docs/API_REFERENCE.md) - Complete endpoint documentation
- [Integration Guide](docs/INTEGRATION_GUIDE.md) - How systems work together
- [Development Guide](docs/DEVELOPMENT.md) - Contributing guidelines

---

## 🔐 Security

- JWT authentication with HS256 signing
- Bcrypt password hashing (12 salt rounds)
- API key management via environment variables
- CORS configuration
- SQL injection prevention (ORM)
- Input validation (Pydantic)

---

## 📈 Roadmap

### v1.0 (Current)
- [x] Unified architecture design
- [x] Core integration layer
- [x] Basic pipeline automation
- [x] Unified API

### v1.1 (Next)
- [ ] Advanced analytics dashboard
- [ ] Multi-subject support (Greek, Rhetoric)
- [ ] Enhanced pattern library
- [ ] A/B testing framework

### v2.0 (Future)
- [ ] Multi-tenant support
- [ ] WebSocket real-time updates
- [ ] Mobile app
- [ ] LMS integrations (Canvas, Blackboard)

---

## 🤝 Contributing

We welcome contributions! This project combines:
- **Steel2** (Elle Jansick / YT Research LLC) - Curriculum generation
- **Doc Digester** (Elle Jansick) - Content analysis
- **Harv** (Elle Jansick) - AI tutoring platform

Contact: ellejansickresearch@gmail.com

---

## 📄 License

MIT License - See LICENSE file for details

---

## 🙏 Acknowledgments

This unified platform stands on the shoulders of three specialized systems:
- **Steel2/TEQUILA** - Advanced curriculum generation with spiral learning
- **Doc Digester** - 5-phase educational content analysis
- **Harv** - Socratic AI tutoring with 4-layer memory

By integrating them, we create something greater than the sum of its parts.

---

**Built with Claude Code**

Generated with [Claude Code](https://claude.com/claude-code)
