// Netherworld Navigator - Frontend JavaScript
class NetherworldNavigator {
    constructor() {
        this.apiBaseUrl = '/api';
        this.isConnected = false;
        this.currentRealm = 'mortal';
        this.conversationHistory = [];
        
        this.init();
    }
    
    async init() {
        console.log('🔮 Initializing Netherworld Navigator...');
        
        // Set up event listeners
        this.setupEventListeners();
        
        // Check API connection
        await this.checkConnection();
        
        // Initialize the system
        await this.initializeSystem();
        
        console.log('✅ Netherworld Navigator initialized');
    }
    
    setupEventListeners() {
        // Send button
        document.getElementById('sendButton').addEventListener('click', () => this.sendQuery());
        
        // Enter key in textarea
        document.getElementById('queryInput').addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendQuery();
            }
        });
        
        // Realm navigation
        document.querySelectorAll('.realm-item').forEach(item => {
            item.addEventListener('click', () => this.selectRealm(item.dataset.realm));
        });
    }
    
    async checkConnection() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/health`);
            const data = await response.json();
            
            if (data.status === 'connected') {
                this.updateConnectionStatus(true, data.message);
            } else {
                this.updateConnectionStatus(false, 'API returned unexpected status');
            }
        } catch (error) {
            console.error('Connection check failed:', error);
            this.updateConnectionStatus(false, 'Failed to connect to API server');
        }
    }
    
    updateConnectionStatus(connected, message) {
        this.isConnected = connected;
        const indicator = document.getElementById('statusIndicator');
        const statusText = document.getElementById('statusText');
        
        if (connected) {
            indicator.className = 'status-indicator connected';
            statusText.textContent = 'Connected';
            statusText.style.color = 'var(--mint)';
        } else {
            indicator.className = 'status-indicator disconnected';
            statusText.textContent = 'Disconnected';
            statusText.style.color = 'var(--crimson)';
        }
        
        console.log(`Connection status: ${connected ? 'Connected' : 'Disconnected'} - ${message}`);
    }
    
    async initializeSystem() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/initialize`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });
            
            if (response.ok) {
                const data = await response.json();
                console.log('🏛️ System initialized:', data);
            }
        } catch (error) {
            console.error('Failed to initialize system:', error);
        }
    }
    
    selectRealm(realmName) {
        // Update active realm
        document.querySelectorAll('.realm-item').forEach(item => {
            item.classList.remove('active');
        });
        
        document.querySelector(`[data-realm="${realmName}"]`).classList.add('active');
        this.currentRealm = realmName;
        
        console.log(`🏛️ Selected realm: ${realmName}`);
    }
    
    async sendQuery() {
        const queryInput = document.getElementById('queryInput');
        const sendButton = document.getElementById('sendButton');
        const query = queryInput.value.trim();
        
        if (!query) return;
        
        // Check connection
        if (!this.isConnected) {
            this.addMessage('system', '⚠️ Not connected to API server. Please check if the backend is running on port 3001.');
            return;
        }
        
        // Disable input while processing
        sendButton.disabled = true;
        sendButton.innerHTML = '<span class="loading"></span> <span>Navigating...</span>';
        
        // Add user message
        this.addMessage('user', query);
        queryInput.value = '';
        
        try {
            // Send to API
            const response = await fetch(`${this.apiBaseUrl}/search`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    query: query,
                    realm: this.currentRealm,
                    conversation_history: this.conversationHistory.slice(-5) // Last 5 messages for context
                })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            const data = await response.json();
            console.log('📡 API Response:', data);
            
            // Process and display response
            this.processApiResponse(data);
            
        } catch (error) {
            console.error('Query failed:', error);
            this.addMessage('system', `❌ Error: ${error.message}`);
        } finally {
            // Re-enable input
            sendButton.disabled = false;
            sendButton.innerHTML = '<span class="btn-text">Navigate</span><span class="btn-icon">🧭</span>';
            queryInput.focus();
        }
    }
    
    processApiResponse(data) {
        if (!data) {
            this.addMessage('system', '❌ Received empty response from server');
            return;
        }
        
        // Extract navigation message
        let responseText = data.navigation_message || 'Response received';
        
        // Add results information
        if (data.results && data.results.length > 0) {
            responseText += `\n\n📚 **Found ${data.total_matches || data.results.length} relevant documents:**\n`;
            
            data.results.forEach((result, index) => {
                responseText += `\n**${index + 1}. ${result.title}**\n`;
                responseText += `*Realm: ${result.realm}* | *Score: ${result.score}%*\n`;
                responseText += `${result.snippet}\n`;
                
                // Add state law links if available
                if (result.state_law_links && result.state_law_links.length > 0) {
                    responseText += `\n🔗 **State Law References:**\n`;
                    result.state_law_links.forEach(link => {
                        responseText += `• [${link.source}](${link.url}) - ${link.state} ${link.area}\n`;
                    });
                }
                
                responseText += `\n---\n`;
            });
        }
        
        // Add detected states info
        if (data.states_detected && data.states_detected.length > 0) {
            responseText += `\n🗺️ **States Detected:** ${data.states_detected.join(', ')}`;
        }
        
        // Add legal area info
        if (data.legal_area) {
            responseText += `\n⚖️ **Legal Area:** ${data.legal_area.replace('_', ' ').toUpperCase()}`;
        }
        
        this.addMessage('ai', responseText);
        
        // Store in conversation history
        this.conversationHistory.push({
            query: data.query,
            response: responseText,
            timestamp: new Date().toISOString()
        });
    }
    
    addMessage(sender, content) {
        const messagesContainer = document.getElementById('chatMessages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const messageBubble = document.createElement('div');
        messageBubble.className = 'message-bubble';
        
        const messageHeader = document.createElement('div');
        messageHeader.className = 'message-header';
        
        const senderIcon = sender === 'user' ? '👤' : sender === 'ai' ? '🔮' : '⚙️';
        const senderName = sender === 'user' ? 'You' : sender === 'ai' ? 'Netherworld Navigator' : 'System';
        
        messageHeader.innerHTML = `${senderIcon} ${senderName}`;
        
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        
        // Convert markdown-style formatting to HTML
        const formattedContent = this.formatMessage(content);
        messageContent.innerHTML = formattedContent;
        
        messageBubble.appendChild(messageHeader);
        messageBubble.appendChild(messageContent);
        messageDiv.appendChild(messageBubble);
        
        messagesContainer.appendChild(messageDiv);
        
        // Scroll to bottom
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
    
    formatMessage(content) {
        return content
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2" target="_blank" class="law-link">$1</a>')
            .replace(/\n/g, '<br>')
            .replace(/---/g, '<hr style="border: 1px solid var(--emerald); margin: 1rem 0;">');
    }
}

// Quick Action Functions
function startStateComparison() {
    const navigator = window.netherworldNavigator;
    const queryInput = document.getElementById('queryInput');
    queryInput.value = 'Compare estate laws between different states - what are the key differences I should know about?';
    queryInput.focus();
}

function generateCommunication() {
    const navigator = window.netherworldNavigator;
    const queryInput = document.getElementById('queryInput');
    queryInput.value = 'Generate a professional communication template for updating beneficiaries about estate proceedings';
    queryInput.focus();
}

function exportDatabase() {
    const navigator = window.netherworldNavigator;
    const queryInput = document.getElementById('queryInput');
    queryInput.value = 'Export current legal database and realm information for review';
    queryInput.focus();
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', () => {
    window.netherworldNavigator = new NetherworldNavigator();
});

// Periodic connection check
setInterval(async () => {
    if (window.netherworldNavigator) {
        await window.netherworldNavigator.checkConnection();
    }
}, 30000); // Check every 30 seconds
