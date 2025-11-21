// HealthNest AI - Frontend JavaScript
// API Configuration
const API_BASE_URL = 'http://localhost:5000';

// User Profile
let userProfile = {
    age: 25,
    gender: 'male',
    weight: 70,
    height: 170,
    activity: 'moderate'
};

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    console.log('HealthNest AI initialized');
    checkAPIHealth();
});

// Check API Health
async function checkAPIHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        const data = await response.json();
        
        if (data.status === 'healthy') {
            updateStatus('Ready', 'success');
        } else {
            updateStatus('API Error', 'error');
        }
    } catch (error) {
        updateStatus('Offline', 'error');
        console.error('API not reachable:', error);
        addBotMessage('⚠️ Backend API is not running. Please start the Flask server first:\n\ncd backend\npython app.py');
    }
}

// Update Status
function updateStatus(text, type) {
    const statusEl = document.getElementById('status');
    const dotEl = statusEl.querySelector('.status-dot');
    
    statusEl.innerHTML = `<span class="status-dot"></span> ${text}`;
    
    const newDot = statusEl.querySelector('.status-dot');
    if (type === 'success') {
        newDot.style.background = 'var(--success-color)';
    } else if (type === 'error') {
        newDot.style.background = 'var(--danger-color)';
    }
}

// Update Profile
async function updateProfile() {
    const age = parseInt(document.getElementById('age').value);
    const gender = document.getElementById('gender').value;
    const weight = parseFloat(document.getElementById('weight').value);
    const height = parseFloat(document.getElementById('height').value);
    const activity = document.getElementById('activity').value;

    userProfile = { age, gender, weight, height, activity };

    // Get health analysis
    try {
        updateStatus('Analyzing...', 'warning');
        
        const response = await fetch(`${API_BASE_URL}/health-check`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(userProfile)
        });

        const data = await response.json();

        if (data.metrics) {
            displayMetrics(data.metrics);
            displayRecommendations(data.recommendations);
        }

        updateStatus('Ready', 'success');
    } catch (error) {
        console.error('Error:', error);
        updateStatus('Error', 'error');
        addBotMessage('❌ Could not analyze health data. Please check if the backend is running.');
    }
}

// Display Metrics
function displayMetrics(metrics) {
    const metricsCard = document.getElementById('metricsCard');
    metricsCard.style.display = 'block';

    document.querySelector('#bmiMetric .metric-value').textContent = 
        `${metrics.bmi} (${metrics.bmi_category})`;
    
    document.querySelector('#calorieMetric .metric-value').textContent = 
        `${metrics.daily_calories} kcal`;
    
    document.querySelector('#waterMetric .metric-value').textContent = 
        `${metrics.daily_water_liters}L`;
    
    document.querySelector('#stepMetric .metric-value').textContent = 
        `${metrics.step_goal} steps`;
}

// Display Recommendations
function displayRecommendations(recommendations) {
    let message = '📊 <strong>Your Health Analysis:</strong><br><br>';
    
    recommendations.forEach(rec => {
        message += `<strong>${rec.type}:</strong> ${rec.message}<br><br>`;
    });

    addBotMessage(message);
}

// Send Message
async function sendMessage() {
    const input = document.getElementById('chatInput');
    const message = input.value.trim();

    if (!message) return;

    // Add user message
    addUserMessage(message);
    input.value = '';

    // Show typing indicator
    addTypingIndicator();

    try {
        const response = await fetch(`${API_BASE_URL}/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message: message,
                profile: userProfile
            })
        });

        const data = await response.json();

        // Remove typing indicator
        removeTypingIndicator();

        // Add bot response
        if (data.response) {
            addBotMessage(data.response);
        } else {
            addBotMessage('Sorry, I encountered an error. Please try again.');
        }

    } catch (error) {
        console.error('Error:', error);
        removeTypingIndicator();
        addBotMessage('❌ Could not get response. Please ensure the backend server is running.');
    }
}

// Ask Quick Question
function askQuestion(question) {
    document.getElementById('chatInput').value = question;
    sendMessage();
}

// Add User Message
function addUserMessage(text) {
    const messagesContainer = document.getElementById('chatMessages');
    
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message user-message';
    
    messageDiv.innerHTML = `
        <div class="message-avatar">👤</div>
        <div class="message-content">
            <p>${escapeHtml(text)}</p>
        </div>
    `;
    
    messagesContainer.appendChild(messageDiv);
    scrollToBottom();
}

// Add Bot Message
function addBotMessage(text) {
    const messagesContainer = document.getElementById('chatMessages');
    
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot-message';
    
    // Format text (convert newlines to <br>, preserve formatting)
    const formattedText = text.replace(/\n/g, '<br>');
    
    messageDiv.innerHTML = `
        <div class="message-avatar">🤖</div>
        <div class="message-content">
            ${formattedText}
        </div>
    `;
    
    messagesContainer.appendChild(messageDiv);
    scrollToBottom();
}

// Add Typing Indicator
function addTypingIndicator() {
    const messagesContainer = document.getElementById('chatMessages');
    
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message bot-message';
    typingDiv.id = 'typingIndicator';
    
    typingDiv.innerHTML = `
        <div class="message-avatar">🤖</div>
        <div class="message-content">
            <div class="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </div>
    `;
    
    messagesContainer.appendChild(typingDiv);
    scrollToBottom();
}

// Remove Typing Indicator
function removeTypingIndicator() {
    const indicator = document.getElementById('typingIndicator');
    if (indicator) {
        indicator.remove();
    }
}

// Scroll to Bottom
function scrollToBottom() {
    const messagesContainer = document.getElementById('chatMessages');
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// Handle Enter Key
function handleKeyPress(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}

// Escape HTML
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

// Export for HTML onclick
window.updateProfile = updateProfile;
window.sendMessage = sendMessage;
window.askQuestion = askQuestion;
window.handleKeyPress = handleKeyPress;
