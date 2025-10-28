# 🚀 HARV SHIPPED - Currently Running

**Date**: 2025-10-28
**Status**: ✅ Fully Operational

---

## 🎉 Platform is Live!

Both backend and frontend are currently running and ready to use.

### 📡 Backend Server
- **URL**: http://localhost:8085
- **Status**: ✅ Running
- **Process**: uvicorn with auto-reload
- **Health**: http://localhost:8085/health

### 🖥️ Frontend Server
- **URL**: http://localhost:8080
- **Status**: ✅ Running
- **Process**: Python HTTP server

---

## 🔗 Quick Access Links

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend** | http://localhost:8080 | Main web interface |
| **Backend API** | http://localhost:8085 | REST API endpoints |
| **API Docs** | http://localhost:8085/docs | Interactive Swagger UI |
| **ReDoc** | http://localhost:8085/redoc | Alternative API docs |
| **Health Check** | http://localhost:8085/health | System health status |
| **System Status** | http://localhost:8085/api/status | Detailed system info |

---

## 🎯 How to Use

### 1. Open the Frontend
Navigate to: **http://localhost:8080**

### 2. Create an Account
1. Click **"Login"** button (top right)
2. Switch to **"Register"** tab
3. Enter your email, name, and password
4. Click **"Register"**

### 3. Explore the Platform

#### 📊 Dashboard Tab
- View system statistics
- Check module counts
- See quality scores
- Monitor system health

#### 🔄 Pipeline Tab
- **Import Week**: Convert Steel2 weeks to Harv modules
- **Validate Quality**: Check curriculum with Doc Digester
- **Full Cycle**: Run complete automation (validate → import → feedback → refine)

#### 📚 Curriculum Tab
- Browse all 35 weeks of Latin A curriculum
- View status badges (Published/Draft)
- Check quality scores
- See grammar focus for each week

#### 🔍 Content Analyzer Tab
- Upload educational content (.txt, .docx, .pdf)
- Run 5-phase Doc Digester analysis
- View analysis results

#### 🎓 AI Tutor Tab
- Select a module (Week 1-35)
- Chat with Sparky, the AI Latin tutor
- Ask questions about Latin grammar and vocabulary
- Get Socratic-style teaching

---

## 🛠️ Management Commands

### Check if servers are running:
```bash
# Check backend
lsof -ti:8085

# Check frontend
lsof -ti:8080
```

### Stop servers:
```bash
# Stop backend
lsof -ti:8085 | xargs kill -9

# Stop frontend
lsof -ti:8080 | xargs kill -9
```

### Restart servers:
```bash
# Backend
cd /Users/elle_jansick/harv_shipped
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8085 &

# Frontend
cd /Users/elle_jansick/harv_shipped/frontend
python -m http.server 8080 &
```

---

## 📊 Current Configuration

### Environment (.env)
- **Port**: 8085
- **Environment**: development
- **Debug**: Enabled
- **Database**: SQLite at `backend/data/harv.db`
- **OPENAI_API_KEY**: Configured ✅
- **SECRET_KEY**: Set ✅

### Features Enabled
✅ Auto-validation
✅ Auto-import
✅ Pattern extraction
✅ Feedback loop
✅ Analytics

### AI Configuration
- **Provider**: OpenAI
- **Model**: gpt-4o
- **Temperature**: 0.2
- **Max Tokens**: 2000

---

## 🔍 Testing the Platform

### Test Backend Health:
```bash
curl http://localhost:8085/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "app": "HARV SHIPPED",
  "version": "1.0.0",
  "components": {
    "curriculum_generator": "ready",
    "content_analyzer": "ready",
    "ai_tutor": "ready",
    "integration_layer": "ready"
  }
}
```

### Test System Status:
```bash
curl http://localhost:8085/api/status
```

### Test Frontend:
```bash
curl -I http://localhost:8080
```

**Expected**: `HTTP/1.0 200 OK`

---

## 📝 API Endpoints Available

### Pipeline (11 endpoints)
```
POST /api/pipeline/generate
POST /api/pipeline/import-to-harv
POST /api/pipeline/validate
POST /api/pipeline/full-cycle
GET  /api/pipeline/quality-report/{week}
GET  /api/pipeline/status
POST /api/pipeline/batch-validate
POST /api/pipeline/extract-patterns
GET  /api/pipeline/feedback/{module_id}
```

### Curriculum (3 endpoints)
```
POST /api/curriculum/generate
GET  /api/curriculum/weeks
GET  /api/curriculum/week/{id}
```

### Analysis (3 endpoints)
```
POST /api/analysis/analyze
GET  /api/analysis/list
GET  /api/analysis/{id}
```

### Tutoring (5 endpoints)
```
POST /api/tutoring/register
POST /api/tutoring/login
GET  /api/tutoring/modules
POST /api/tutoring/chat
```

### Analytics (3 endpoints)
```
GET /api/analytics/dashboard
GET /api/analytics/module/{id}
GET /api/analytics/student/{id}
```

**Total**: 25 endpoints

---

## 🐛 Troubleshooting

### Frontend not connecting to backend?
1. Check both servers are running
2. Verify `frontend/js/app.js` has `API_BASE = 'http://localhost:8085/api'`
3. Check browser console for CORS errors
4. Clear browser cache and reload

### Backend not starting?
1. Check `.env` file exists with `SECRET_KEY` and `OPENAI_API_KEY`
2. Verify port 8085 is not in use: `lsof -ti:8085`
3. Check Python environment has all dependencies: `pip install -r requirements.txt`
4. Review backend logs for errors

### Database issues?
1. Database location: `backend/data/harv.db`
2. To reset: Delete `harv.db` and restart backend (tables will be recreated)
3. Check database permissions

### Authentication not working?
1. Clear browser localStorage: `localStorage.clear()`
2. Check JWT token expiration (24 hours)
3. Verify SECRET_KEY is set in `.env`
4. Try registering a new account

---

## 📚 Documentation

For more detailed information, see:

- **README.md** - Project overview
- **PLATFORM_READY.md** - Complete platform guide
- **IMPORT_FIXES_COMPLETE.md** - Technical implementation details
- **FRONTEND_COMPLETE.md** - Frontend documentation
- **docs/INTEGRATION_GUIDE.md** - Integration patterns

---

## 🎉 You're All Set!

The HARV SHIPPED platform is fully operational and ready to use.

**Next**: Open http://localhost:8080 and start exploring! 🚀

---

**Built with**: Claude Code
**Platform**: HARV SHIPPED v1.0
**Date**: 2025-10-28
