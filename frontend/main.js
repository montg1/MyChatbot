/**
 * Chat Widget Logic
 * Handles session management, API calls, and UI updates
 */

// Configuration - Environment Variable (VITE_API_BASE_URL)
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

// Session Management
function generateSessionId() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
        const r = (Math.random() * 16) | 0;
        const v = c === 'x' ? r : (r & 0x3) | 0x8;
        return v.toString(16);
    });
}

function getSessionId() {
    let sessionId = localStorage.getItem('chat_session_id');
    if (!sessionId) {
        sessionId = generateSessionId();
        localStorage.setItem('chat_session_id', sessionId);
    }
    return sessionId;
}

// Chat History Management
function getChatHistory() {
    const history = localStorage.getItem('chat_history');
    return history ? JSON.parse(history) : [];
}

function saveChatHistory(history) {
    localStorage.setItem('chat_history', JSON.stringify(history));
}

function clearChatHistory() {
    localStorage.removeItem('chat_history');
    localStorage.removeItem('chat_session_id');
}

// DOM Elements
const chatMessages = document.getElementById('chatMessages');
const chatForm = document.getElementById('chatForm');
const chatInput = document.getElementById('chatInput');
const sendBtn = document.getElementById('sendBtn');
const clearChatBtn = document.getElementById('clearChat');

// State
let isLoading = false;
let chatHistory = getChatHistory();

// Initialize
function init() {
    // Load existing messages
    if (chatHistory.length > 0) {
        renderMessages();
    }

    // Event listeners
    chatForm.addEventListener('submit', handleSubmit);
    clearChatBtn.addEventListener('click', handleClearChat);

    // Quick question buttons
    document.querySelectorAll('.quick-question').forEach(btn => {
        btn.addEventListener('click', () => {
            const question = btn.dataset.question;
            chatInput.value = question;
            chatForm.dispatchEvent(new Event('submit'));
        });
    });
}

// Render all messages
function renderMessages() {
    // Clear welcome message and existing messages
    chatMessages.innerHTML = '';

    chatHistory.forEach(msg => {
        appendMessage(msg.role, msg.content, false);
    });

    scrollToBottom();
}

// Append a single message
function appendMessage(role, content, save = true) {
    // Remove welcome message if it exists
    const welcomeMsg = chatMessages.querySelector('.welcome-message');
    if (welcomeMsg) {
        welcomeMsg.remove();
    }

    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;
    messageDiv.innerHTML = `
        <div class="message-content">${escapeHtml(content)}</div>
    `;
    chatMessages.appendChild(messageDiv);

    if (save) {
        chatHistory.push({ role, content });
        saveChatHistory(chatHistory);
    }

    scrollToBottom();
}

// Show typing indicator
function showTypingIndicator() {
    const indicator = document.createElement('div');
    indicator.className = 'message assistant typing';
    indicator.id = 'typingIndicator';
    indicator.innerHTML = `
        <div class="message-content">
            <div class="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </div>
    `;
    chatMessages.appendChild(indicator);
    scrollToBottom();
}

// Remove typing indicator
function removeTypingIndicator() {
    const indicator = document.getElementById('typingIndicator');
    if (indicator) {
        indicator.remove();
    }
}

// Scroll to bottom of chat
function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Handle form submission
async function handleSubmit(e) {
    e.preventDefault();

    const message = chatInput.value.trim();
    if (!message || isLoading) return;

    // Clear input
    chatInput.value = '';

    // Add user message
    appendMessage('user', message);

    // Show loading state
    isLoading = true;
    sendBtn.disabled = true;
    showTypingIndicator();

    try {
        const response = await fetch(`${API_BASE_URL}/api/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message,
                sessionId: getSessionId(),
                history: chatHistory.slice(-10), // Last 10 messages for context
            }),
        });

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }

        const data = await response.json();
        removeTypingIndicator();
        appendMessage('assistant', data.reply);

    } catch (error) {
        console.error('Chat error:', error);
        removeTypingIndicator();
        appendMessage('assistant', `Sorry, I couldn't process your request. Please make sure the backend server is running on ${API_BASE_URL}`);
    } finally {
        isLoading = false;
        sendBtn.disabled = false;
        chatInput.focus();
    }
}

// Handle clear chat
function handleClearChat() {
    if (confirm('Are you sure you want to clear the chat history?')) {
        clearChatHistory();
        chatHistory = [];

        // Reset to welcome message
        chatMessages.innerHTML = `
            <div class="welcome-message">
                <div class="welcome-icon">👋</div>
                <h3>Welcome!</h3>
                <p>Ask me anything about my experience, skills, or projects.</p>
                <div class="quick-questions">
                    <button class="quick-question" data-question="What's your experience with Python?">
                        Python experience?
                    </button>
                    <button class="quick-question" data-question="Tell me about your projects">
                        Your projects?
                    </button>
                    <button class="quick-question" data-question="What are your main skills?">
                        Main skills?
                    </button>
                </div>
            </div>
        `;

        // Reattach quick question listeners
        document.querySelectorAll('.quick-question').forEach(btn => {
            btn.addEventListener('click', () => {
                const question = btn.dataset.question;
                chatInput.value = question;
                chatForm.dispatchEvent(new Event('submit'));
            });
        });
    }
}

// Start the app
init();
