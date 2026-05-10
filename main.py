import sys
import os

# Add the current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    try:
        from app.bot import run_bot
        print("Launching LLM Council Bot...")
        run_bot()
    except ImportError as e:
        print(f"Import failed: {e}")
        print("Please ensure you have installed the requirements: pip install -r requirements.txt")
    except Exception as e:
        print(f"Startup failed: {e}")
