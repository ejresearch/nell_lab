# HARV SHIPPED Frontend

Beautiful, modern Tailwind CSS frontend for the unified educational platform.

## Features

### 📊 Dashboard
- System status overview
- Real-time statistics (modules, students, quality scores)
- Quick actions for common tasks
- Health monitoring

### 🔄 Pipeline Tab
- **Import to Harv**: Convert Steel2 weeks to Harv modules
- **Validate Quality**: Check curriculum quality with Doc Digester
- **Complete Cycle**: Run full automation (validate → import → feedback → refine)
- Real-time results display

### 📚 Curriculum Tab
- View all 35 weeks of Latin A curriculum
- Published/draft status indicators
- Quality scores per week
- Grammar focus overview

### 🔍 Content Analyzer Tab
- Drag-and-drop file upload
- Support for .txt, .docx, .pdf files
- 5-phase Doc Digester analysis
- Results visualization

### 🎓 AI Tutor Tab
- Module selection (35 weeks)
- Real-time chat with Sparky (AI tutor)
- Socratic teaching method
- Conversation history

### 🔐 Authentication
- User registration
- Login/logout
- JWT token management
- Session persistence

## Tech Stack

- **Tailwind CSS** - Modern utility-first CSS framework (CDN)
- **Vanilla JavaScript** - No framework dependencies
- **REST API** - FastAPI backend integration
- **LocalStorage** - Client-side session management

## Quick Start

### 1. Start Backend

```bash
cd /Users/elle_jansick/harv_shipped/backend
python -m app.main
```

Backend runs at: http://localhost:8000

### 2. Serve Frontend

**Option A: Python HTTP Server**
```bash
cd /Users/elle_jansick/harv_shipped/frontend
python -m http.server 3000
```

**Option B: Node.js HTTP Server**
```bash
cd /Users/elle_jansick/harv_shipped/frontend
npx http-server -p 3000
```

**Option C: VS Code Live Server**
- Right-click `index.html`
- Select "Open with Live Server"

Frontend opens at: http://localhost:3000

### 3. Test the System

1. **Register an account**
   - Click "Login" in top right
   - Switch to "Register" tab
   - Create your account

2. **Explore the Dashboard**
   - View system status
   - Check quick actions

3. **Try the Pipeline**
   - Go to Pipeline tab
   - Import a week (e.g., Week 1)
   - Validate quality

4. **View Curriculum**
   - Go to Curriculum tab
   - See all available weeks

5. **Chat with Sparky**
   - Go to Tutor tab
   - Select a module
   - Ask questions about Latin!

## API Endpoints Used

### Pipeline
- `POST /api/pipeline/import-to-harv` - Import weeks
- `POST /api/pipeline/validate` - Validate quality
- `POST /api/pipeline/full-cycle` - Complete automation
- `GET /api/pipeline/status` - System status

### Curriculum
- `GET /api/curriculum/weeks` - List all weeks
- `GET /api/curriculum/week/{id}` - Week details

### Content Analyzer
- `POST /api/analysis/analyze` - Analyze content

### AI Tutor
- `POST /api/tutoring/register` - Register user
- `POST /api/tutoring/login` - Login user
- `GET /api/tutoring/modules` - List modules
- `POST /api/tutoring/chat` - Chat with AI

### Analytics
- `GET /api/analytics/dashboard` - Dashboard metrics

## File Structure

```
frontend/
├── index.html          # Main single-page application
├── js/
│   └── app.js         # All JavaScript logic
├── css/
│   └── harv-styles.css # Custom styles (from Harv)
└── README.md          # This file
```

## Features by Tab

### Dashboard
- ✅ System status monitoring
- ✅ Quick statistics
- ✅ Health indicators
- ✅ Quick action buttons

### Pipeline
- ✅ Week import to Harv
- ✅ Quality validation
- ✅ Complete automation cycles
- ✅ Results visualization
- ⏳ Batch operations (coming soon)

### Curriculum
- ✅ Week listing with status
- ✅ Quality scores
- ⏳ Week editing (coming soon)
- ⏳ Export functionality (coming soon)

### Content Analyzer
- ✅ File upload interface
- ✅ Format validation
- ⏳ 5-phase analysis display (API pending)
- ⏳ Pattern extraction (coming soon)

### AI Tutor
- ✅ Module selection
- ✅ Chat interface
- ⏳ Memory system integration (coming soon)
- ⏳ Progress tracking (coming soon)

## Design Philosophy

### Colors
- **Primary (Blue)**: Main actions, pipeline operations
- **Secondary (Green)**: Success states, published content
- **Accent (Yellow)**: Quality metrics, warnings

### Layout
- **Responsive**: Works on mobile, tablet, desktop
- **Tab-based**: Single-page app with smooth transitions
- **Card design**: Clean, modern card-based layouts
- **Toast notifications**: Non-intrusive feedback

### UX Principles
- **Clear feedback**: Loading states, success/error messages
- **Intuitive navigation**: Tab-based with clear labels
- **Consistent design**: Same patterns throughout
- **Accessible**: Proper contrast, keyboard navigation

## Browser Support

- ✅ Chrome/Edge (latest)
- ✅ Firefox (latest)
- ✅ Safari (latest)
- ⚠️ IE11 (not supported - Tailwind CSS requires modern browsers)

## Customization

### Change Colors

Edit `tailwind.config` in `index.html`:

```javascript
tailwind.config = {
    theme: {
        extend: {
            colors: {
                primary: '#your-color',
                secondary: '#your-color',
                accent: '#your-color',
            }
        }
    }
}
```

### Change API URL

Edit `API_BASE` in `js/app.js`:

```javascript
const API_BASE = 'https://your-api-url.com/api';
```

## Troubleshooting

### Backend not connecting
- Check backend is running: http://localhost:8000/health
- Check CORS settings in backend config
- Check API_BASE URL in app.js

### Authentication not working
- Clear localStorage: `localStorage.clear()`
- Check JWT token expiration
- Verify backend auth endpoints

### Modules not loading
- Ensure you're logged in
- Check backend has published modules
- Import weeks via Pipeline tab first

## Next Steps

1. **Import Curriculum**: Use Pipeline → Import to load weeks
2. **Register Account**: Create your first user
3. **Select Module**: Choose a week in Tutor tab
4. **Start Learning**: Chat with Sparky!

## Development

To modify the frontend:

1. Edit `index.html` for structure
2. Edit `js/app.js` for functionality
3. Use Tailwind utility classes for styling
4. Test with backend running

## Production Deployment

For production:

1. Replace Tailwind CDN with build:
   ```bash
   npm install -D tailwindcss
   npx tailwindcss -o css/tailwind.css --minify
   ```

2. Minify JavaScript:
   ```bash
   npx terser js/app.js -o js/app.min.js
   ```

3. Update API_BASE to production URL

4. Serve via Nginx/Apache/CDN

---

**Built with ❤️ using Tailwind CSS**

Part of the HARV SHIPPED unified educational platform.
