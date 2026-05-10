# 🧠 LLM Council Telegram Bot

A lightweight, multi-agent AI assistant optimized for low-end hardware and free-tier Gemini API usage.

## ✨ Features
- **Multi-Agent Council**: Analyst, Researcher, Critic, Optimizer, and Judge reason internally to provide high-quality answers.
- **Low-Resource Design**: Runs natively on Python without Docker or heavy local models. Stable on i3/8GB systems.
- **Free-Tier Optimized**: Uses ONLY Gemini Free API. No paid subscriptions required.
- **Telegram Native**: Clean chat interface with mode-switching commands.

## 📂 Folder Structure
```text
llm_council_bot/
├── app/
│   ├── agents.py       # Agent personas & system prompts
│   ├── bot.py          # Telegram bot logic
│   └── council.py      # Multi-agent orchestration
├── .env                # API Keys (Create this!)
├── main.py             # Entry point
└── requirements.txt    # Dependencies
```

## 🚀 Setup Instructions

### 1. Get Your API Keys
1. **Gemini API Key**: Go to [Google AI Studio](https://aistudio.google.com/) and create a free API key.
2. **Telegram Bot Token**: Message [@BotFather](https://t.me/botfather) on Telegram to create a new bot and get your token.

### 2. Installation
1. Install Python (3.9+ recommended).
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### 3. Configuration
Create a file named `.env` in the root folder and add your keys:
```env
GEMINI_API_KEY=your_gemini_key_here
TELEGRAM_BOT_TOKEN=your_telegram_token_here
```

### 4. Run the Bot
```bash
python main.py
```

## 🤖 Bot Commands
- `/start` - Initial setup and help.
- `/coding` - Switch to High-Performance Coding mode.
- `/research` - Switch to Academic/Data Research mode.
- `/automation` - Switch to Workflow/Logic mode.
- `/learning` - Switch to Simple Conceptual mode.

## 💡 Optimization for Low-End Systems
- **Sequential Execution**: Agents run one after another to keep RAM usage below 200MB.
- **Free Quota Handling**: Includes built-in delays to avoid hitting the 15 RPM limit of Gemini Free.
- **No Heavy Inference**: All "intelligence" is handled in the cloud; your local machine only handles simple API calls.

---
**Built for stability, efficiency, and speed.**
