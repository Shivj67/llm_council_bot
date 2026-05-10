# 🏛️ LLM Council V2 Elite - Multi-Agent Telegram Bot

An elite, multi-agent AI assistant optimized for low-end hardware and free-tier usage.

## 🚀 New V2 Features
- **🧠 Persistent Memory**: Remembers your previous conversation turns.
- **👁️ Multimodal Vision**: Send photos for the council to analyze.
- **🎤 Voice Support**: Send voice notes; the bot transcribes and responds.
- **🌐 Web Search**: The Researcher agent now pulls real-time facts from Google.
- **⚙️ Interactive Settings**: Use `/settings` to change council depth and personas.
- **🖥️ Admin Dashboard**: Monitor agent reasoning live via Streamlit.

## 🛠️ Setup
1. **API Keys**: Add your tokens to `.env`.
2. **Install**: `pip install -r requirements.txt`
3. **Run Bot**: `python main.py`
4. **Run Dashboard**: `streamlit run dashboard.py`

## 🕹️ How to Use
- **/start**: Get the welcome menu.
- **/settings**: Change your Council Depth (Quick/Standard/Deep) and Persona.
- **/coding, /research, /debater...**: Quick-switch between specialized reasoning modes.
- **Send Media**: Attach a photo or send a voice message for advanced analysis.

## ⚙️ Optimization
- **Hardware**: Optimized for i3/i5 systems (Low RAM footprint).
- **Quota**: Uses a 6-second inter-agent delay to safely stay within Gemini Free Tier limits.
