# Evolving Persona AI - Personality Evolving AI Partner
<img width="2914" height="1505" alt="image" src="https://github.com/user-attachments/assets/8ff7a3be-c626-4a81-99c1-09871eb27ef5" />
<img width="2891" height="1538" alt="image" src="https://github.com/user-attachments/assets/94ed8be6-9024-4631-8c5d-1e0353b3036a" />
<img width="2911" height="1497" alt="image" src="https://github.com/user-attachments/assets/0e69a913-a60a-440a-95e2-9ba834da6d7b" />
<img width="2905" height="1483" alt="image" src="https://github.com/user-attachments/assets/ea80c3c3-2a8c-4780-9568-65aa279e66c3" />
<img width="2911" height="1483" alt="image" src="https://github.com/user-attachments/assets/15de5250-2e9f-4f73-aa36-f25eb8919799" />

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.3.3-green)

## Overview

"Personality Evolving AI Partner" is an innovative chatbot system where the AI's personality dynamically changes and evolves through conversations with the user. A Flask API backend and modern frontend UI work together to provide an immersive user experience.

Safety & Consent (must-read)

• Parent/child and workplace usage: parental guidance and organization policies should be considered.
• Sensitive-topic filters automatically trigger safe-response templates (e.g., underage, alcohol+driving, sexual content).

## 🌟 Key Features

### 🎨 Dynamic UI Themes
- Complete color themes for 5 personality types (Natural, Tsundere, Yandere, Kuudere, Dandere)
- Smooth theme transition animations
- Consistent changes to message bubbles, backgrounds, and text colors

### 📊 Real-time Status Display
- Collapsible status panel
- Personality tendency radar chart (using Chart.js)
- Affection level progress bar
- Long-term memory list display

### ✨ Spectacular Evolution Effects
- Full-screen flash effects
- Particle animations matching theme colors
- Evolution announcement in modal window
- Smooth theme switching

### 💬 Modern Chat UI
- Smooth message animations
- Typing indicator
- Auto-scroll
- Responsive design
- Textarea auto-resize

### 🧠 Intelligent AI Integration
- Integration with Google Gemini AI
- Single API call for response + personality analysis
- Long-term memory system (#memory tag)
- Conversation context maintenance
- Memory-based evolution system

### 🚀 Instant Demo Experience
- Demo mode with accelerated evolution
- Quick start functionality
- Instant evolution test commands

## 🎮 Instant Demo Experience

### Quick Start
1. After starting the app, click the "🚀 Start Demo Mode" button
2. Chat 2-3 times to trigger evolution!
3. Or use "⚡ Instant Evolution Test" for immediate evolution

### Permanent Demo Mode via Environment Variables
```bash
# Set in .env file
DEMO_MODE=true
EVOLUTION_AFFECTION_THRESHOLD=3
EVOLUTION_SCORE_DIFFERENCE=2
Evolution Test Command
Type #evolve_now in chat for instant evolution

🛠 Setup Instructions
1. Environment Setup
bash
# Clone repository
git clone < https://github.com/EMMA019/Evo-chat.git >
cd evolving-persona-ai

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
2. Environment Variable Configuration
bash
# Create .env file
cp .env.example .env

# --- Application Configuration ---
SECRET_KEY=your secret key here

# --- Database Configuration ---
DATABASE_URL=sqlite:///instance/project.db

# --- External Services ---
GEMINI_API_KEY=your GEMINI key here

# --- Evolution Parameters ---
EVOLUTION_AFFECTION_THRESHOLD=30
EVOLUTION_SCORE_DIFFERENCE=5

# --- Application Limits ---
MAX_CHAT_MESSAGES_PER_USER=100
MAX_REQUESTS_PER_MINUTE=60

# --- Demo Mode ---
DEMO_MODE=false
DEMO_EVOLUTION_THRESHOLD=3
DEMO_SCORE_DIFFERENCE=2

# --- Environment ---
FLASK_ENV=development

3. Database Initialization
bash
# Create database and run migrations
flask db upgrade
4. Application Startup
bash
# Start development server
python run.py

# Or use Flask command
flask run
5. Access
Open browser and navigate to http://localhost:5000

📁 Project Structure
text
evolving-persona-ai/
├── app/
│   ├── __init__.py              # Application factory
│   ├── extensions.py            # Database extensions
│   ├── models.py                # Database models
│   ├── api/                     # API endpoints
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── frontend/                # Frontend
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   ├── templates/
│   │   │   └── index.html
│   │   └── static/
│   │       ├── css/
│   │       │   └── style.css
│   │       └── js/
│   │           └── sw.js
│   │           └── script.js
│   └── ...
├── bot/                         # AI logic
│   ├── __init__.py
│   ├── engine.py               # AI response generation
│   ├── evolution.py            # Evolution logic
│   ├── memory.py               # Memory management
│   ├── memory_analyzer.py      # Memory analysis
│   └── prompts.py              # Prompt management
├── config.py                   # Configuration management
├── run.py                      # Application entry point
├── unpacker.py                 # Project unpacking tool
├── requirements.txt            # Dependencies
├── .env.example               # Environment variable template
└── tests/                     # Tests
    └── test_basic.py

🔌 API Endpoints
POST /api/chat
Send user message and get AI response

json
{
  "message": "Hello!"
}
GET /api/status
Get current user status

POST /api/reset
Reset user data

POST /api/demo/quick-start
Create pre-evolution state for demo mode

💡 Usage
Start Conversation: Type message in input field and send

Add Memories: Use #memory important information format to add long-term memories

Check Status: Click "Status" button for detailed information

Observe Evolution: Evolution triggers when affection reaches threshold and personality scores have sufficient difference

🧩 Technology Stack
Backend
Flask: Web framework

SQLAlchemy: ORM

Google Gemini AI: AI language model

Flask-Migrate: Database migrations

Frontend
Vanilla JavaScript: Interactive features

CSS3: Modern styling and animations

Chart.js: Radar chart display

Responsive Design: Multi-device support

Security Features
Session fixation attack protection

Rate limiting

Input validation

Secure cookie settings

⚙️ Customization
Evolution Parameter Adjustment
Adjust these parameters in .env file:

bash
EVOLUTION_AFFECTION_THRESHOLD=30      # Affection required for evolution
EVOLUTION_SCORE_DIFFERENCE=5          # Score difference required for evolution
MAX_CHAT_MESSAGES_PER_USER=100        # Message retention per user
Theme Color Changes
Edit CSS variables in app/frontend/static/css/style.css:

css
:root {
  --primary-color: #your-color;
  --background-color: #your-background-color;
  /* Other color variables */
}
Memory Analysis Customization
Edit keyword mappings in bot/memory_analyzer.py to adjust reactions to specific words.

🧪 Running Tests
bash
# Run tests
pytest tests/

# Detailed test output
pytest tests/ -v
📄 License
This project is released under the MIT License.

🤝 Contributing
Bug reports, feature requests, and pull requests are welcome.

🔮 Future Feature Extensions
Voice recognition & synthesis

Multi-user support

Evolution history visualization

Custom personality type addition

Mobile app support

Cloud storage functionality

# Credits
Original concept and implementation by Emma Saka
GitHub: EMMA019/Evo-chat
=======
# Evo-chat
Evolving Persona AI is a cutting-edge chatbot system that moves beyond simple conversation. It empowers AI with a persistent, dynamic personality that evolves based on user interaction and relationship depth.  
>>>>>>> 2a93dcfce7acae8d43a950db11adb5548a4be359
