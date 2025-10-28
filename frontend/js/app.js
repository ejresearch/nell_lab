// HARV SHIPPED - Main Application JavaScript
// API Configuration
const API_BASE = 'http://localhost:8085/api';
let authToken = localStorage.getItem('authToken');
let currentUser = JSON.parse(localStorage.getItem('currentUser') || 'null');
let currentModuleId = null;

// ============================================================================
// Initialization
// ============================================================================

document.addEventListener('DOMContentLoaded', async () => {
    console.log('🚀 HARV SHIPPED initializing...');

    // Update auth UI
    updateAuthUI();

    // Load dashboard data
    await loadDashboard();

    // Load curriculum weeks
    await loadWeeks();

    console.log('✅ HARV SHIPPED ready!');
});

// ============================================================================
// Tab Management
// ============================================================================

function switchTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });

    // Remove active class from all buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active', 'border-blue-600', 'text-blue-600');
        btn.classList.add('border-transparent', 'text-gray-600');
    });

    // Show selected tab
    document.getElementById(tabName).classList.add('active');

    // Update active button
    const activeBtn = event?.target || document.querySelector(`[onclick="switchTab('${tabName}')"]`);
    if (activeBtn) {
        activeBtn.classList.add('active', 'border-blue-600', 'text-blue-600');
        activeBtn.classList.remove('border-transparent', 'text-gray-600');
    }

    // Load tab-specific data
    if (tabName === 'tutor' && authToken) {
        loadModules();
    }
}

// ============================================================================
// Authentication
// ============================================================================

function showAuth() {
    document.getElementById('authModal').classList.remove('hidden');
    document.getElementById('authModal').classList.add('flex');
}

function hideAuth() {
    document.getElementById('authModal').classList.add('hidden');
    document.getElementById('authModal').classList.remove('flex');
}

function switchAuthTab(tab) {
    // Hide all forms
    document.querySelectorAll('.auth-form').forEach(form => form.classList.add('hidden'));

    // Remove active from all tabs
    document.querySelectorAll('.auth-tab-btn').forEach(btn => {
        btn.classList.remove('border-blue-600', 'text-blue-600');
        btn.classList.add('border-transparent', 'text-gray-600');
    });

    // Show selected form
    document.getElementById(`${tab}Form`).classList.remove('hidden');

    // Activate tab
    event.target.classList.add('border-blue-600', 'text-blue-600');
    event.target.classList.remove('border-transparent', 'text-gray-600');
}

async function login() {
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;

    if (!email || !password) {
        showToast('Please enter email and password', 'error');
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/tutoring/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        if (response.ok) {
            authToken = data.access_token;
            currentUser = { id: data.user_id, email };
            localStorage.setItem('authToken', authToken);
            localStorage.setItem('currentUser', JSON.stringify(currentUser));

            updateAuthUI();
            hideAuth();
            showToast('Login successful!', 'success');

            // Reload dashboard
            await loadDashboard();
        } else {
            showToast(data.detail || 'Login failed', 'error');
        }
    } catch (error) {
        console.error('Login error:', error);
        showToast('Login failed. Is the server running?', 'error');
    }
}

async function register() {
    const name = document.getElementById('registerName').value;
    const email = document.getElementById('registerEmail').value;
    const password = document.getElementById('registerPassword').value;

    if (!name || !email || !password) {
        showToast('Please fill all fields', 'error');
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/tutoring/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, email, password })
        });

        const data = await response.json();

        if (response.ok) {
            authToken = data.access_token;
            currentUser = { id: data.user_id, email, name };
            localStorage.setItem('authToken', authToken);
            localStorage.setItem('currentUser', JSON.stringify(currentUser));

            updateAuthUI();
            hideAuth();
            showToast('Registration successful!', 'success');

            // Reload dashboard
            await loadDashboard();
        } else {
            showToast(data.detail || 'Registration failed', 'error');
        }
    } catch (error) {
        console.error('Registration error:', error);
        showToast('Registration failed. Is the server running?', 'error');
    }
}

function logout() {
    authToken = null;
    currentUser = null;
    localStorage.removeItem('authToken');
    localStorage.removeItem('currentUser');
    updateAuthUI();
    showToast('Logged out successfully', 'success');

    // Clear sensitive data
    document.getElementById('modulesList').innerHTML = '<div class="text-sm text-gray-500">Login to view modules</div>';
    document.getElementById('chatMessages').innerHTML = '<div class="text-center text-gray-500 text-sm py-8">Please login to chat</div>';
}

function updateAuthUI() {
    const authBtn = document.getElementById('authBtn');
    const userInfo = document.getElementById('userInfo');

    if (authToken && currentUser) {
        authBtn.textContent = 'Logout';
        authBtn.onclick = logout;
        userInfo.textContent = `👤 ${currentUser.email}`;
        userInfo.classList.remove('hidden');
    } else {
        authBtn.textContent = 'Login';
        authBtn.onclick = showAuth;
        userInfo.classList.add('hidden');
    }
}

// ============================================================================
// API Helpers
// ============================================================================

async function apiRequest(endpoint, options = {}) {
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };

    if (authToken) {
        headers['Authorization'] = `Bearer ${authToken}`;
    }

    const response = await fetch(`${API_BASE}${endpoint}`, {
        ...options,
        headers
    });

    if (!response.ok && response.status === 401) {
        // Token expired
        logout();
        showToast('Session expired. Please login again.', 'error');
        throw new Error('Unauthorized');
    }

    return response;
}

// ============================================================================
// Dashboard
// ============================================================================

async function loadDashboard() {
    try {
        // Load pipeline status
        const statusResponse = await apiRequest('/pipeline/status');
        const status = await statusResponse.json();

        // Update stat cards
        document.getElementById('totalModules').textContent = status.modules?.total || 0;
        document.getElementById('publishedModules').textContent = status.modules?.published || 0;
        document.getElementById('avgQuality').textContent = status.quality?.average_score?.toFixed(1) || '0.0';

        // Load analytics if authenticated
        if (authToken) {
            const analyticsResponse = await apiRequest('/analytics/dashboard');
            const analytics = await analyticsResponse.json();
            document.getElementById('totalStudents').textContent = analytics.students || 0;
        }
    } catch (error) {
        console.error('Dashboard load error:', error);
        // Show placeholder data
        document.getElementById('totalModules').textContent = '0';
        document.getElementById('publishedModules').textContent = '0';
        document.getElementById('avgQuality').textContent = '0.0';
        document.getElementById('totalStudents').textContent = '0';
    }
}

// ============================================================================
// Pipeline Functions
// ============================================================================

async function importToHarv() {
    const week = document.getElementById('importWeek').value;

    if (!week || week < 1 || week > 35) {
        showToast('Please enter a valid week number (1-35)', 'error');
        return;
    }

    try {
        showToast('Importing week to Harv...', 'info');

        const response = await apiRequest('/pipeline/import-to-harv', {
            method: 'POST',
            body: JSON.stringify({ weeks: [parseInt(week)] })
        });

        const result = await response.json();

        if (response.ok) {
            showPipelineResults(result);
            showToast(`Week ${week} imported successfully!`, 'success');
            await loadWeeks(); // Refresh weeks list
        } else {
            showToast(result.detail || 'Import failed', 'error');
        }
    } catch (error) {
        console.error('Import error:', error);
        showToast('Import failed. Check console for details.', 'error');
    }
}

async function validateWeek() {
    const week = document.getElementById('validateWeek').value;

    if (!week || week < 1 || week > 35) {
        showToast('Please enter a valid week number (1-35)', 'error');
        return;
    }

    try {
        showToast('Validating week quality...', 'info');

        const response = await apiRequest('/pipeline/validate', {
            method: 'POST',
            body: JSON.stringify({ week: parseInt(week) })
        });

        const result = await response.json();

        if (response.ok) {
            showPipelineResults(result);
            showToast(`Week ${week} validated! Score: ${result.quality_score}/10`, 'success');
        } else {
            showToast(result.detail || 'Validation failed', 'error');
        }
    } catch (error) {
        console.error('Validation error:', error);
        showToast('Validation failed. Check console for details.', 'error');
    }
}

async function runFullCycle() {
    const week = document.getElementById('cycleWeek').value;
    const autoRefine = document.getElementById('autoRefine').checked;

    if (!week || week < 1 || week > 35) {
        showToast('Please enter a valid week number (1-35)', 'error');
        return;
    }

    try {
        showToast('Running complete automation cycle...', 'info');

        const response = await apiRequest('/pipeline/full-cycle', {
            method: 'POST',
            body: JSON.stringify({
                week: parseInt(week),
                auto_refine: autoRefine
            })
        });

        const result = await response.json();

        if (response.ok) {
            showPipelineResults(result);
            showToast(`Complete cycle finished for Week ${week}!`, 'success');
        } else {
            showToast(result.detail || 'Cycle failed', 'error');
        }
    } catch (error) {
        console.error('Full cycle error:', error);
        showToast('Cycle failed. Check console for details.', 'error');
    }
}

function showPipelineResults(result) {
    const resultsDiv = document.getElementById('pipelineResults');
    const outputDiv = document.getElementById('pipelineOutput');

    outputDiv.textContent = JSON.stringify(result, null, 2);
    resultsDiv.classList.remove('hidden');

    // Scroll to results
    resultsDiv.scrollIntoView({ behavior: 'smooth' });
}

// ============================================================================
// Curriculum Management
// ============================================================================

async function loadWeeks() {
    try {
        const response = await apiRequest('/curriculum/weeks');
        const data = await response.json();

        const weeksList = document.getElementById('weeksList');

        if (data.total === 0) {
            weeksList.innerHTML = `
                <div class="col-span-full text-center py-8">
                    <p class="text-gray-600 mb-4">No weeks available yet</p>
                    <p class="text-sm text-gray-500">Use the Pipeline tab to import curriculum</p>
                </div>
            `;
            return;
        }

        weeksList.innerHTML = data.weeks.map(week => `
            <div class="border-2 border-gray-200 rounded-lg p-4 hover:border-blue-500 transition duration-200 cursor-pointer">
                <div class="flex items-start justify-between mb-2">
                    <h3 class="font-semibold text-gray-900">Week ${week.week_number}</h3>
                    ${week.is_published
                        ? '<span class="px-2 py-1 bg-green-100 text-green-800 text-xs rounded-full">Published</span>'
                        : '<span class="px-2 py-1 bg-gray-100 text-gray-800 text-xs rounded-full">Draft</span>'
                    }
                </div>
                <p class="text-sm text-gray-600 mb-2">${week.title || 'Untitled'}</p>
                <p class="text-xs text-gray-500">${week.grammar_focus || 'No grammar focus'}</p>
                ${week.quality_score
                    ? `<div class="mt-2 text-xs text-gray-600">Quality: ${week.quality_score.toFixed(1)}/10</div>`
                    : ''
                }
            </div>
        `).join('');
    } catch (error) {
        console.error('Load weeks error:', error);
        document.getElementById('weeksList').innerHTML = `
            <div class="col-span-full text-center py-8 text-red-600">
                Failed to load weeks. Is the server running?
            </div>
        `;
    }
}

// ============================================================================
// AI Tutor Functions
// ============================================================================

async function loadModules() {
    try {
        const response = await apiRequest('/tutoring/modules');
        const data = await response.json();

        const modulesList = document.getElementById('modulesList');

        if (data.total === 0) {
            modulesList.innerHTML = '<div class="text-sm text-gray-500">No modules available</div>';
            return;
        }

        modulesList.innerHTML = data.modules.map(module => `
            <button onclick="selectModule(${module.id}, '${module.title}')"
                class="w-full text-left p-3 rounded-lg hover:bg-blue-50 transition duration-200 ${currentModuleId === module.id ? 'bg-blue-100' : 'bg-gray-50'}">
                <div class="font-medium text-gray-900 text-sm">Week ${module.week_number}</div>
                <div class="text-xs text-gray-600 truncate">${module.title}</div>
            </button>
        `).join('');
    } catch (error) {
        console.error('Load modules error:', error);
    }
}

function selectModule(moduleId, title) {
    currentModuleId = moduleId;

    // Update UI
    loadModules(); // Refresh to show selected

    // Clear and prepare chat
    const chatMessages = document.getElementById('chatMessages');
    chatMessages.innerHTML = `
        <div class="bg-blue-50 border-l-4 border-blue-500 p-4 rounded">
            <p class="text-sm text-blue-900">
                <strong>Module Selected:</strong> ${title}
            </p>
            <p class="text-xs text-blue-700 mt-1">
                Ask Sparky any questions about this module!
            </p>
        </div>
    `;

    // Enable chat input
    document.getElementById('chatInput').disabled = false;
    document.getElementById('sendBtn').disabled = false;

    showToast('Module selected! Start chatting with Sparky', 'success');
}

async function sendMessage() {
    const input = document.getElementById('chatInput');
    const message = input.value.trim();

    if (!message || !currentModuleId) return;

    // Add user message to chat
    addChatMessage('user', message);
    input.value = '';

    try {
        const response = await apiRequest('/tutoring/chat', {
            method: 'POST',
            body: JSON.stringify({
                module_id: currentModuleId,
                message: message
            })
        });

        const data = await response.json();

        // Add AI response
        addChatMessage('assistant', data.reply);
    } catch (error) {
        console.error('Chat error:', error);
        addChatMessage('system', 'Sorry, I encountered an error. Please try again.');
    }
}

function addChatMessage(role, content) {
    const chatMessages = document.getElementById('chatMessages');

    const messageDiv = document.createElement('div');
    messageDiv.className = `flex ${role === 'user' ? 'justify-end' : 'justify-start'}`;

    const bubble = document.createElement('div');
    bubble.className = `max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
        role === 'user'
            ? 'bg-blue-600 text-white'
            : role === 'assistant'
            ? 'bg-gray-200 text-gray-900'
            : 'bg-yellow-100 text-yellow-900'
    }`;
    bubble.textContent = content;

    messageDiv.appendChild(bubble);
    chatMessages.appendChild(messageDiv);

    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Enable Enter key for chat
document.addEventListener('DOMContentLoaded', () => {
    const chatInput = document.getElementById('chatInput');
    if (chatInput) {
        chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !chatInput.disabled) {
                sendMessage();
            }
        });
    }
});

// ============================================================================
// Content Analyzer
// ============================================================================

document.getElementById('fileInput')?.addEventListener('change', async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    // Check file size (100MB limit)
    if (file.size > 100 * 1024 * 1024) {
        showToast('File too large. Maximum size is 100MB.', 'error');
        return;
    }

    // Check file type
    const allowedTypes = ['.txt', '.docx', '.pdf'];
    const fileExt = '.' + file.name.split('.').pop().toLowerCase();
    if (!allowedTypes.includes(fileExt)) {
        showToast('Unsupported file type. Use .txt, .docx, or .pdf', 'error');
        return;
    }

    try {
        showToast('Analyzing content... This may take a few minutes.', 'info');

        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch(`${API_BASE}/analysis/analyze`, {
            method: 'POST',
            headers: authToken ? { 'Authorization': `Bearer ${authToken}` } : {},
            body: formData
        });

        const result = await response.json();

        if (response.ok) {
            showAnalysisResults(result);
            showToast('Analysis complete!', 'success');
        } else {
            showToast(result.detail || 'Analysis failed', 'error');
        }
    } catch (error) {
        console.error('Analysis error:', error);
        showToast('Analysis failed. Check console for details.', 'error');
    }
});

function showAnalysisResults(result) {
    const resultsDiv = document.getElementById('analysisResults');
    const outputDiv = document.getElementById('analysisOutput');

    outputDiv.innerHTML = `
        <pre class="text-sm overflow-x-auto">${JSON.stringify(result, null, 2)}</pre>
    `;

    resultsDiv.classList.remove('hidden');
}

// ============================================================================
// Toast Notifications
// ============================================================================

function showToast(message, type = 'info') {
    const toast = document.getElementById('toast');
    const toastMessage = document.getElementById('toastMessage');

    toastMessage.textContent = message;

    // Color based on type
    toast.className = 'fixed bottom-4 right-4 px-6 py-3 rounded-lg shadow-lg transform transition-all duration-300';

    if (type === 'success') {
        toast.classList.add('bg-green-600', 'text-white');
    } else if (type === 'error') {
        toast.classList.add('bg-red-600', 'text-white');
    } else if (type === 'info') {
        toast.classList.add('bg-blue-600', 'text-white');
    } else {
        toast.classList.add('bg-gray-900', 'text-white');
    }

    toast.classList.remove('hidden');

    // Auto-hide after 3 seconds
    setTimeout(() => {
        toast.classList.add('hidden');
    }, 3000);
}
