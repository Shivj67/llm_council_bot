import sys
import os

# Add the current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    print("-----------------------------------------")
    print("LLM Council Bot V2 - Elite Edition")
    print("-----------------------------------------")
    print("1. Launching Telegram Bot...")
    print("2. Admin Dashboard is ready (run: streamlit run dashboard.py)")
    print("-----------------------------------------")
    
    try:
        from app.bot import run_bot
        run_bot()
    except ImportError as e:
        print(f"Import failed: {e}")
        print("Please run: pip install -r requirements.txt")
    except Exception as e:
        print(f"Startup failed: {e}")
