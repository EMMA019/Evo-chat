// Event System Class - Handles real-time events and themes
class EventSystem {
    constructor(uiController) {
        this.ui = uiController;
        this.currentEvents = [];
        this.currentThemes = [];
        this.affectionBonus = 0;
        this.initialLoadComplete = false;
        this.initializeEvents();
    }

    initializeEvents() {
        this.loadCurrentEvents();
        // Update events every hour
        setInterval(() => this.loadCurrentEvents(), 60 * 60 * 1000);
    }

    async loadCurrentEvents() {
        try {
            const response = await fetch('/api/events/current');
            if (response.ok) {
                const eventData = await response.json();
                this.currentEvents = eventData.active_events || [];
                this.currentThemes = eventData.current_themes || [];
                this.affectionBonus = eventData.affection_bonus || 0;
                this.displayEvents(eventData);
                
                // Update welcome message if this is the first load
                if (!this.initialLoadComplete) {
                    this.updateWelcomeMessage(eventData.welcome_message);
                    this.initialLoadComplete = true;
                }
            }
        } catch (error) {
            console.error('Failed to load events:', error);
        }
    }

    displayEvents(eventData) {
        // Remove existing event display
        const existingIndicator = document.querySelector('.event-indicator');
        if (existingIndicator) {
            existingIndicator.remove();
        }

        if (eventData.active_events && eventData.active_events.length > 0) {
            const eventIndicator = this.createEventIndicator(eventData);
            const header = document.querySelector('.header');
            
            // 【修正】ヘッダーの中ではなく、ヘッダーの直後（外側）に追加する
            // これにより、レイアウト上で独立したブロックとなり、重なりを防ぐ
            if (header) {
                header.after(eventIndicator);
            }
        }
    }

    createEventIndicator(eventData) {
        const indicator = document.createElement('div');
        indicator.className = 'event-indicator';
        
        let eventHTML = '<div class="event-content">';
        eventHTML += '<div class="event-title">🎊 Active Events</div>';
        
        eventData.active_events.forEach(event => {
            eventHTML += `
                <div class="event-item" data-theme="${event.theme}">
                    <span class="event-icon">${event.icon}</span>
                    <span class="event-name">${event.name}</span>
                    ${event.affection_bonus > 0 ? 
                        `<span class="affection-bonus">+${event.affection_bonus}💖</span>` : ''}
                </div>
            `;
        });

        if (eventData.affection_bonus > 0) {
            eventHTML += `
                <div class="total-bonus">
                    Total Affection Bonus: +${eventData.affection_bonus}
                </div>
            `;
        }

        eventHTML += '</div>';
        indicator.innerHTML = eventHTML;

        return indicator;
    }

    updateWelcomeMessage(welcomeMessage) {
        // Update the initial welcome message if it exists
        const welcomeElement = document.querySelector('.welcome-message .message-content');
        if (welcomeElement && welcomeMessage) {
            welcomeElement.textContent = welcomeMessage;
        }
    }

    getAffectionBonus() {
        return this.affectionBonus;
    }

    getCurrentThemes() {
        return this.currentThemes;
    }

    hasActiveEvents() {
        return this.currentEvents.length > 0;
    }
}

// Main UI Controller Class
class EvolvingPersonaUI {
    constructor() {
        this.currentTheme = 'natural';
        this.currentStatus = null;
        this.radarChart = null;
        this.isStatusOpen = false;
        
        this.initializeApp();
        this.bindEvents();
        this.loadInitialStatus();

        // Initialize event system
        this.eventSystem = new EventSystem(this);
    }

    initializeApp() {
        // Apply theme
        this.applyTheme('natural');
        
        // Initialize radar chart
        this.initializeRadarChart();
    }

    bindEvents() {
        // Send button
        document.getElementById('sendButton').addEventListener('click', () => this.sendMessage());
        
        // Enter key to send (Shift+Enter for new line)
        const messageInput = document.getElementById('messageInput');
        messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });

        // Textarea auto-resize
        messageInput.addEventListener('input', () => this.autoResizeTextarea(messageInput));
        
        // Memory tag detection
        messageInput.addEventListener('input', () => this.detectMemoryTag(messageInput));

        // Status panel toggle
        document.getElementById('statusToggle').addEventListener('click', () => this.toggleStatusPanel());

        // Reset button
        document.getElementById('resetButton').addEventListener('click', () => this.resetConversation());

        // Evolution modal close
        document.addEventListener('click', (e) => {
            if (e.target.id === 'evolutionClose') {
                this.closeEvolutionModal();
            }
        });

        // Demo mode buttons
        const demoBtn = document.getElementById('demoModeBtn');
        if (demoBtn) demoBtn.addEventListener('click', () => this.enableDemoMode());
        
        const quickEvoBtn = document.getElementById('quickEvolutionBtn');
        if (quickEvoBtn) quickEvoBtn.addEventListener('click', () => this.quickEvolutionTest());
    }

    autoResizeTextarea(textarea) {
        // Reset height then set to scroll height
        textarea.style.height = 'auto';
        
        // Adjust height based on content (max 200px)
        const newHeight = Math.min(textarea.scrollHeight, 200);
        textarea.style.height = newHeight + 'px';
        
        // Show scrollbar if needed
        textarea.style.overflowY = textarea.scrollHeight > 200 ? 'auto' : 'hidden';
    }

    detectMemoryTag(textarea) {
        const inputContainer = textarea.closest('.input-container');
        const hint = document.querySelector('.input-hint');
        
        if (textarea.value.includes('#memory')) {
            // Highlight when memory tag detected
            inputContainer.classList.add('memory-tag-detected');
            hint.textContent = '💾 This message will be saved as long-term memory';
            hint.style.color = 'var(--primary-color)';
            hint.style.fontWeight = 'bold';
            
            // Visual emphasis for memory tag
            this.showMemoryTooltip();
        } else {
            // Return to normal state
            inputContainer.classList.remove('memory-tag-detected');
            hint.textContent = 'Use #memory tag to save important things to memory';
            hint.style.color = '';
            hint.style.fontWeight = '';
        }
    }

    showMemoryTooltip() {
        // Remove existing tooltip
        const existingTooltip = document.querySelector('.memory-tooltip');
        if (existingTooltip) {
            existingTooltip.remove();
        }

        // Create new tooltip
        const tooltip = document.createElement('div');
        tooltip.className = 'memory-tooltip';
        tooltip.innerHTML = `
            <div class="tooltip-content">
                <span class="tooltip-icon">💾</span>
                <span class="tooltip-text">This part will be memorized</span>
            </div>
        `;
        
        const inputArea = document.querySelector('.input-area');
        inputArea.appendChild(tooltip);
        
        // Auto-hide after 3 seconds
        setTimeout(() => {
            tooltip.style.opacity = '0';
            setTimeout(() => tooltip.remove(), 300);
        }, 3000);
    }

    async loadInitialStatus() {
        try {
            const response = await fetch('/api/status');
            if (response.ok) {
                const status = await response.json();
                this.updateUI(status);
            }
        } catch (error) {
            console.error('Failed to load status:', error);
        }
    }

    async sendMessage() {
        const input = document.getElementById('messageInput');
        const message = input.value.trim();
        
        if (!message) return;

        // Disable input
        this.setInputEnabled(false);
        
        // Display user message
        this.addMessage(message, 'user');
        input.value = '';

        // Reset textarea height
        this.autoResizeTextarea(input);

        // Show typing indicator
        this.showTypingIndicator();

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            });

            if (!response.ok) {
                throw new Error('API request failed');
            }

            const data = await response.json();
            
            // Hide typing indicator
            this.hideTypingIndicator();
            
            // Display AI response
            this.addMessage(data.ai_response, 'ai');
            
            // Update UI
            this.updateUI(data.current_status);
            
            // Handle evolution if triggered
            if (data.evolution_triggered && data.new_personality) {
                await this.showEvolutionEffect(data.new_personality);
            }

        } catch (error) {
            console.error('Message send error:', error);
            this.hideTypingIndicator();
            this.addMessage('Sorry, an error occurred. Please try again.', 'ai');
        } finally {
            this.setInputEnabled(true);
            input.focus();
        }
    }

    addMessage(content, role) {
        const messagesContainer = document.getElementById('chatMessages');
        const messageElement = document.createElement('div');
        messageElement.className = `message-bubble ${role}-message`;
        
        const contentElement = document.createElement('div');
        contentElement.className = 'message-content';
        contentElement.textContent = content;
        
        messageElement.appendChild(contentElement);
        messagesContainer.appendChild(messageElement);
        
        // Scroll to bottom
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    showTypingIndicator() {
        document.getElementById('typingIndicator').classList.remove('hidden');
        document.getElementById('chatMessages').scrollTop = document.getElementById('chatMessages').scrollHeight;
    }

    hideTypingIndicator() {
        document.getElementById('typingIndicator').classList.add('hidden');
    }

    setInputEnabled(enabled) {
        const input = document.getElementById('messageInput');
        const button = document.getElementById('sendButton');
        
        input.disabled = !enabled;
        button.disabled = !enabled;
        
        if (enabled) {
            input.focus();
        }
    }

    updateUI(status) {
        this.currentStatus = status;
        
        // Update theme
        if (status.personality.toLowerCase() !== this.currentTheme) {
            this.applyTheme(status.personality.toLowerCase());
        }
        
        // Update personality display
        document.getElementById('currentPersona').textContent = status.personality;
        
        // Update affection level
        const affectionPercent = Math.min(100, (status.affection / 30) * 100);
        document.getElementById('affectionProgress').style.width = `${affectionPercent}%`;
        document.getElementById('affectionText').textContent = `${status.affection}/30`;
        
        // Update radar chart
        this.updateRadarChart(status.scores);
        
        // Update long-term memories
        this.updateMemoriesList(status.long_term_memories);
    }

    applyTheme(personality) {
        // Remove current theme class
        document.body.classList.remove(`theme-${this.currentTheme}`);
        
        // Add new theme class
        this.currentTheme = personality;
        document.body.classList.add(`theme-${personality}`);
        
        // Update radar chart colors too
        if (this.radarChart) {
            const theme = this.getThemeColors(personality);
            this.radarChart.data.datasets[0].backgroundColor = theme.radarBackground;
            this.radarChart.data.datasets[0].borderColor = theme.radarBorder;
            this.radarChart.update();
        }
    }

    getThemeColors(personality) {
        const themes = {
            natural: { radarBackground: 'rgba(76, 175, 80, 0.2)', radarBorder: '#4CAF50' },
            tsundere: { radarBackground: 'rgba(255, 105, 180, 0.2)', radarBorder: '#FF69B4' },
            yandere: { radarBackground: 'rgba(220, 20, 60, 0.2)', radarBorder: '#DC143C' },
            kuudere: { radarBackground: 'rgba(0, 191, 255, 0.2)', radarBorder: '#00BFFF' },
            dandere: { radarBackground: 'rgba(216, 191, 216, 0.2)', radarBorder: '#D8BFD8' }
        };
        return themes[personality] || themes.natural;
    }

    initializeRadarChart() {
        const ctx = document.getElementById('personalityRadar').getContext('2d');
        const theme = this.getThemeColors(this.currentTheme);
        
        this.radarChart = new Chart(ctx, {
            type: 'radar',
            data: {
                labels: ['Tsundere', 'Yandere', 'Kuudere', 'Dandere'],
                datasets: [{
                    label: 'Personality Tendencies',
                    data: [0, 0, 0, 0],
                    backgroundColor: theme.radarBackground,
                    borderColor: theme.radarBorder,
                    borderWidth: 2,
                    pointBackgroundColor: theme.radarBorder,
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: theme.radarBorder
                }]
            },
            options: {
                scales: {
                    r: {
                        beginAtZero: true,
                        max: 30,
                        ticks: {
                            stepSize: 10,
                            display: false
                        },
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        },
                        angleLines: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        },
                        pointLabels: {
                            color: function(context) {
                                // Change point label color based on theme
                                const body = document.body;
                                if (body.classList.contains('theme-tsundere') || body.classList.contains('theme-yandere')) {
                                    return '#FFFFFF';
                                }
                                return '#333333';
                            },
                            font: {
                                size: 11
                            }
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    }
                },
                animation: {
                    duration: 1000,
                    easing: 'easeOutQuart'
                },
                responsive: true,
                maintainAspectRatio: false
            }
        });
    }

    updateRadarChart(scores) {
        if (this.radarChart) {
            this.radarChart.data.datasets[0].data = [
                scores.tsundere || 0,
                scores.yandere || 0,
                scores.kuudere || 0,
                scores.dandere || 0
            ];
            this.radarChart.update();
        }
    }

    updateMemoriesList(memories) {
        const container = document.getElementById('longTermMemories');
        
        if (memories && memories.length > 0) {
            container.innerHTML = memories.map(memory => 
                `<div class="memory-item">${this.escapeHtml(memory)}</div>`
            ).join('');
        } else {
            container.innerHTML = '<div class="no-memories">No memories yet</div>';
        }
    }

    toggleStatusPanel() {
        const panel = document.getElementById('statusPanel');
        this.isStatusOpen = !this.isStatusOpen;
        
        if (this.isStatusOpen) {
            panel.classList.remove('hidden');
        } else {
            panel.classList.add('hidden');
        }
    }

    async resetConversation() {
        if (!confirm('Reset conversation? All memories and evolution progress will be lost.')) {
            return;
        }

        try {
            const response = await fetch('/api/reset', { method: 'POST' });
            if (response.ok) {
                const newStatus = await response.json();
                this.resetChat();
                this.updateUI(newStatus);
                this.applyTheme('natural');
            }
        } catch (error) {
            console.error('Reset error:', error);
            alert('Reset failed');
        }
    }

    resetChat() {
        const messagesContainer = document.getElementById('chatMessages');
        messagesContainer.innerHTML = `
            <div class="welcome-message">
                <div class="message-bubble ai-message">
                    <div class="message-content">
                        Hello! I'm your AI partner. My personality evolves as we chat more.
                    </div>
                </div>
            </div>
        `;
    }

    async showEvolutionEffect(newPersonality, evolutionFactors = []) {
        const overlay = document.getElementById('evolutionOverlay');
        const modal = document.getElementById('evolutionModal');
        const particles = document.getElementById('evolutionParticles');
        
        // Show overlay
        overlay.classList.remove('hidden');
        
        // Flash effect
        overlay.style.backgroundColor = 'rgba(255, 255, 255, 0.9)';
        await this.delay(300);
        
        // Generate particle effects
        this.createParticles(particles, newPersonality);
        
        // Create evolution factors display
        let factorsHtml = '';
        if (evolutionFactors.length > 0) {
            factorsHtml = `
                <div class="evolution-factors">
                    <h3>Evolution Factors:</h3>
                    <ul>
                        ${evolutionFactors.map(factor => `<li>${this.escapeHtml(factor)}</li>`).join('')}
                    </ul>
                </div>
            `;
        }
        
        // Update modal content
        const evolutionContent = document.querySelector('.evolution-content');
        if (evolutionContent) {
            evolutionContent.innerHTML = `
                <h2 id="evolutionTitle">EVOLVED TO:</h2>
                <div id="evolutionPersona" class="evolution-persona">${newPersonality.toUpperCase()}</div>
                ${factorsHtml}
                <button id="evolutionClose" class="evolution-close">Close</button>
            `;
        }
        
        // Show modal
        await this.delay(1000);
        modal.classList.remove('hidden');
        
        // Update theme
        this.applyTheme(newPersonality.toLowerCase());
    }

    createParticles(container, personality) {
        const particleColors = {
            natural: ['#4CAF50', '#66BB6A', '#81C784'],
            tsundere: ['#FF69B4', '#FF85C2', '#FFA1D0'],
            yandere: ['#DC143C', '#E91E63', '#F06292'],
            kuudere: ['#00BFFF', '#4FC3F7', '#81D4FA'],
            dandere: ['#D8BFD8', '#E6E6FA', '#F0E8F0']
        };
        
        const colors = particleColors[personality.toLowerCase()] || particleColors.natural;
        
        for (let i = 0; i < 50; i++) {
            const particle = document.createElement('div');
            particle.style.position = 'absolute';
            particle.style.width = '10px';
            particle.style.height = '10px';
            particle.style.background = colors[Math.floor(Math.random() * colors.length)];
            particle.style.borderRadius = '50%';
            particle.style.left = `${Math.random() * 100}%`;
            particle.style.top = `${Math.random() * 100}%`;
            particle.style.opacity = '0';
            particle.style.animation = `particleFloat 2s ease-in-out ${Math.random() * 2}s forwards`;
            
            container.appendChild(particle);
        }

        // Dynamically add CSS animation
        if (!document.getElementById('particleAnimation')) {
            const style = document.createElement('style');
            style.id = 'particleAnimation';
            style.textContent = `
                @keyframes particleFloat {
                    0% {
                        opacity: 0;
                        transform: translateY(0) scale(0);
                    }
                    10% {
                        opacity: 1;
                        transform: translateY(-20px) scale(1);
                    }
                    90% {
                        opacity: 1;
                        transform: translateY(-100px) scale(1);
                    }
                    100% {
                        opacity: 0;
                        transform: translateY(-120px) scale(0);
                    }
                }
            `;
            document.head.appendChild(style);
        }
    }

    closeEvolutionModal() {
        const overlay = document.getElementById('evolutionOverlay');
        const modal = document.getElementById('evolutionModal');
        const particles = document.getElementById('evolutionParticles');
        
        modal.classList.add('hidden');
        particles.innerHTML = '';
        
        setTimeout(() => {
            overlay.classList.add('hidden');
        }, 500);
    }

    async enableDemoMode() {
        try {
            const response = await fetch('/api/demo/quick-start', {
                method: 'POST'
            });
            
            if (response.ok) {
                const result = await response.json();
                this.addMessage(result.message, 'ai');
                this.updateUI(result.current_status);
                
                // Show demo mode indicator
                this.showDemoIndicator();
            }
        } catch (error) {
            console.error('Demo mode start error:', error);
        }
    }

    async quickEvolutionTest() {
        // Special command for instant evolution testing
        this.addMessage('#evolve_now', 'user');
        await this.sendMessage();
    }

    showDemoIndicator() {
        const indicator = document.createElement('div');
        indicator.className = 'demo-indicator';
        indicator.innerHTML = '🚀 Demo Mode Activated';
        document.body.appendChild(indicator);
        
        setTimeout(() => {
            indicator.style.opacity = '0';
            setTimeout(() => indicator.remove(), 300);
        }, 3000);
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

// Application initialization
document.addEventListener('DOMContentLoaded', () => {
    new EvolvingPersonaUI();
});

// Service worker registration (PWA preparation)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js')
            .then(registration => {
                console.log('SW registered: ', registration);
            })
            .catch(registrationError => {
                console.log('SW registration failed: ', registrationError);
            });
    });
}