import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from app.council import LLMCouncil
from dotenv import load_dotenv

load_dotenv()

# --- LOGGING ---
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- INITIALIZATION ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
council = LLMCouncil(GEMINI_API_KEY)

# --- USER STATE (Memory-efficient storage for modes) ---
user_modes = {}

# --- COMMANDS ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "🧠 *LLM Council Bot Activated*\n\n"
        "I am a multi-agent system optimized for low-end hardware.\n"
        "Current Mode: *Learning*\n\n"
        "Available Modes:\n"
        "🚀 /coding - Best-practice code solutions\n"
        "📚 /research - In-depth data analysis\n"
        "⚙️ /automation - Workflow & logic tools\n"
        "🎓 /learning - Simple conceptual explanations\n\n"
        "Send me any question to start the internal reasoning flow."
    )
    await update.message.reply_text(welcome_text, parse_mode='Markdown')

async def set_mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    command = update.message.text.split()[0].replace("/", "").lower()
    user_id = update.effective_user.id
    user_modes[user_id] = command
    await update.message.reply_text(f"✅ Mode switched to: *{command.capitalize()}*", parse_mode='Markdown')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    query = update.message.text
    mode = user_modes.get(user_id, "learning")

    status_msg = await update.message.reply_text("🤔 *The Council is convening...*", parse_mode='Markdown')

    try:
        # Iterate through the council generator for progress
        final_answer = ""
        for update_step in council.run_council(query, mode=mode):
            if update_step in ["Analyst", "Researcher", "Critic", "Optimizer", "Final Judge"]:
                # Update status message with current agent
                await context.bot.edit_message_text(
                    chat_id=update.effective_chat.id,
                    message_id=status_msg.message_id,
                    text=f"⏳ *Council in session...*\nCurrently: _{update_step}_ is reasoning.",
                    parse_mode='Markdown'
                )
            else:
                final_answer = update_step

        # Final update with the synthesized answer (with fallback for markdown parsing errors)
        try:
            await context.bot.edit_message_text(
                chat_id=update.effective_chat.id,
                message_id=status_msg.message_id,
                text=final_answer,
                parse_mode='Markdown'
            )
        except Exception as e:
            logger.warning(f"Markdown parsing failed, falling back to plain text: {e}")
            await context.bot.edit_message_text(
                chat_id=update.effective_chat.id,
                message_id=status_msg.message_id,
                text=final_answer
            )
    except Exception as e:
        logger.error(f"Bot error: {e}")
        await context.bot.edit_message_text(
            chat_id=update.effective_chat.id,
            message_id=status_msg.message_id,
            text="❌ *Error*: The council encountered a problem. Please try again."
        )

# --- BOT RUNNER ---
def run_bot():
    if not TELEGRAM_TOKEN or not GEMINI_API_KEY:
        print("CRITICAL: TELEGRAM_BOT_TOKEN or GEMINI_API_KEY missing in .env")
        return

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler(["coding", "research", "automation", "learning"], set_mode))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("Bot is starting...")
    app.run_polling()

if __name__ == '__main__':
    run_bot()
