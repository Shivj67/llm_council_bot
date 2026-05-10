# 🏛️ LLM Council V2 Elite - Project Walkthrough

Welcome to the **V2 Elite Edition** of your multi-agent Telegram bot. This document explains the high-end architecture and features we've implemented to maximize the Gemini Free Tier on lightweight hardware.

## 🌟 Key Features

### 🧠 Persistent Memory (Context-Aware)
The bot now uses a local **SQLite** database (`council.db`) to store your conversation history.
- **How it works**: Every time you ask a question, the bot fetches your last 10 messages and feeds them to the Council.
- **Benefit**: You can ask follow-up questions like *"Can you explain that more simply?"* or *"How does that relate to what we discussed earlier?"*

### 👁️ Multimodal Vision & Voice
We've unlocked the full power of **Gemini 1.5 Flash**.
- **Photos**: You can upload any image, and the Council will analyze it (e.g., debugging code from a photo, explaining a chart, or identifying objects).
- **Voice Notes**: You can send voice messages. The bot automatically transcribes them and processes the request through the Council.

### 🌐 Real-Time Web Search
The **Researcher** agent is now "Live."
- **Grounding**: When you ask about current events or specific facts, the Researcher uses Google Search tools to verify data before presenting it to the Judge.

### ⚙️ Interactive Configuration (`/settings`)
You no longer need to touch the code to change how the bot thinks.
- **Council Depth**:
    - **Quick Scan**: 2 agents (Fast & light).
    - **Standard**: 3 agents (Balanced).
    - **Deep Council**: 5 agents (Maximum reasoning).
- **Personas**: Switch between Learning, Coding, Debater, Creative, and Socratic modes instantly.

### 🖥️ Admin Dashboard (`dashboard.py`)
A dedicated **Streamlit** dashboard for developers.
- **Live Audit**: Watch the "internal" thoughts of the Analyst, Critic, and Researcher in real-time.
- **Stats**: Track your API usage and agent activity.

---

## 🚀 Technical Architecture
- **Language**: Python 3.12+
- **Database**: SQLAlchemy + SQLite
- **API**: Google Generative AI (Gemini 2.0/1.5 Flash)
- **UI**: python-telegram-bot (v21+)
- **Dashboard**: Streamlit + Plotly

## 🕹️ Setup & Usage
1. Ensure your keys are in the `.env` file.
2. Run `python main.py` to start the bot.
3. (Optional) Run `streamlit run dashboard.py` in a separate terminal to see the logs.

---

*This project was built to be fast on i3 systems and 100% free to operate.*
