import logging
import os
import io
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from app.council import LLMCouncil
from app.database import init_db, get_session, User, Message
from dotenv import load_dotenv
from PIL import Image

load_dotenv()
init_db()

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

# --- DB HELPERS ---
def get_user_config(user_id):
    session = get_session()
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        user = User(id=user_id)
        session.add(user)
        session.commit()
    config = {"mode": user.mode, "depth": user.council_depth, "persona": user.persona}
    session.close()
    return config

def save_message(user_id, role, content):
    session = get_session()
    msg = Message(user_id=user_id, role=role, content=content)
    session.add(msg)
    session.commit()
    session.close()

# --- COMMANDS ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "👑 *LLM Council V2 Elite*\n\n"
        "I am now upgraded with multimodal vision, voice support, and persistent memory.\n\n"
        "⚙️ /settings - Configure Council Depth & Personas\n"
        "🚀 /coding, /research, /debater... - Quick mode switch\n\n"
        "Send me a question, a *Photo*, or a *Voice Note* to begin."
    )
    await update.message.reply_text(welcome_text, parse_mode='Markdown')

async def settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Council Depth: Quick", callback_data='depth_quick'),
         InlineKeyboardButton("Standard", callback_data='depth_standard'),
         InlineKeyboardButton("Deep", callback_data='depth_deep')],
        [InlineKeyboardButton("Persona: Balanced", callback_data='mode_learning'),
         InlineKeyboardButton("Debater", callback_data='mode_debater'),
         InlineKeyboardButton("Creative", callback_data='mode_creative')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🛠️ *Council Configuration*", reply_markup=reply_markup, parse_mode='Markdown')

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    data = query.data

    session = get_session()
    user = session.query(User).filter(User.id == user_id).first()
    
    if data.startswith('depth_'):
        user.council_depth = data.replace('depth_', '')
    elif data.startswith('mode_'):
        user.mode = data.replace('mode_', '')
    
    session.commit()
    session.close()
    await query.edit_message_text(f"✅ Setting updated: *{data}*", parse_mode='Markdown')

async def set_mode_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mode = update.message.text.split()[0].replace("/", "").lower()
    user_id = update.effective_user.id
    session = get_session()
    user = session.query(User).filter(User.id == user_id).first()
    if user:
        user.mode = mode
        session.commit()
    session.close()
    await update.message.reply_text(f"✅ Mode switched to: *{mode.capitalize()}*", parse_mode='Markdown')

# --- MESSAGE HANDLERS ---
async def process_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    config = get_user_config(user_id)
    
    # Handle Text, Photo, or Voice
    query_text = update.message.text or update.message.caption or "[Media Input]"
    media_data = None

    if update.message.photo:
        # Get the highest resolution photo
        photo_file = await update.message.photo[-1].get_file()
        img_bytes = await photo_file.download_as_bytearray()
        media_data = Image.open(io.BytesIO(img_bytes))
    elif update.message.voice:
        voice_file = await update.message.voice.get_file()
        voice_bytes = await voice_file.download_as_bytearray()
        # Gemini 1.5 handles audio bytes if wrapped correctly
        media_data = {"mime_type": "audio/ogg", "data": bytes(voice_bytes)}

    status_msg = await update.message.reply_text("🤔 *The Council is convening...*", parse_mode='Markdown')

    try:
        save_message(user_id, "user", query_text)
        final_answer = ""
        
        for update_step in council.run_council(query_text, user_id, mode=config['mode'], depth=config['depth'], media=media_data):
            if update_step in ["Analyst", "Researcher", "Critic", "Optimizer", "Final Judge"]:
                await context.bot.edit_message_text(
                    chat_id=update.effective_chat.id,
                    message_id=status_msg.message_id,
                    text=f"⏳ *Council in session...*\nCurrently: _{update_step}_ is reasoning.",
                    parse_mode='Markdown'
                )
            else:
                final_answer = update_step

        # Final update with fallback
        try:
            await context.bot.edit_message_text(
                chat_id=update.effective_chat.id,
                message_id=status_msg.message_id,
                text=final_answer,
                parse_mode='Markdown'
            )
        except:
            await context.bot.edit_message_text(
                chat_id=update.effective_chat.id,
                message_id=status_msg.message_id,
                text=final_answer
            )
        
        save_message(user_id, "assistant", final_answer)

    except Exception as e:
        logger.error(f"Bot error: {e}")
        await context.bot.edit_message_text(
            chat_id=update.effective_chat.id,
            message_id=status_msg.message_id,
            text=f"❌ *Error*: {str(e)[:100]}"
        )

# --- RUNNER ---
def run_bot():
    if not TELEGRAM_TOKEN or not GEMINI_API_KEY:
        print("CRITICAL: TELEGRAM_BOT_TOKEN or GEMINI_API_KEY missing in .env")
        return

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("settings", settings))
    app.add_handler(CommandHandler(["coding", "research", "automation", "learning", "debater", "creative", "socratic"], set_mode_command))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT | filters.PHOTO | filters.VOICE, process_input))

    print("Bot V2 is starting...")
    app.run_polling()

if __name__ == '__main__':
    run_bot()
