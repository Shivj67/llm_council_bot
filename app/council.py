import google.generativeai as genai
import time
import logging
from app.agents import COUNCIL_PROMPTS, MODE_PROMPTS
from app.database import get_session, AuditLog, Message

class LLMCouncil:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        # Initialize model with Google Search tool enabled
        # Switching to Flash Lite for higher free-tier quotas
        self.model = genai.GenerativeModel('gemini-flash-lite-latest')
        self.logger = logging.getLogger(__name__)

    def run_council(self, user_query, user_id, mode="learning", depth="standard", media=None):
        self.logger.info(f"Starting Council V2 for user {user_id} in mode: {mode}")
        
        # 1. Fetch History from Database
        session = get_session()
        past_messages = session.query(Message).filter(Message.user_id == user_id).order_by(Message.timestamp.desc()).limit(10).all()
        history_context = "\n".join([f"{m.role.upper()}: {m.content}" for m in reversed(past_messages)])
        
        mode_context = MODE_PROMPTS.get(mode.lower(), MODE_PROMPTS["learning"])
        history = f"--- CONVERSATION HISTORY ---\n{history_context}\n\n--- CURRENT TASK ---\nUSER QUERY: {user_query}\nMODE CONTEXT: {mode_context}\n"
        
        # 2. Dynamic Agent Selection (Reduced for Quota Stability)
        agent_order = ["Analyst", "Final Judge"] if depth != "quick" else ["Final Judge"]

        final_response = ""

        try:
            for agent in agent_order:
                yield agent
                system_prompt = COUNCIL_PROMPTS[agent]
                content_parts = [f"System: {system_prompt}\n\nCOUNCIL HISTORY:\n{history}\n\nAction: Provide your contribution."]
                if media: content_parts.append(media)

                time.sleep(15) # 15s delay
                response = self.model.generate_content(content_parts)
                contribution = response.text if response and hasattr(response, 'text') else "Error"
                
                if agent == "Final Judge":
                    final_response = contribution
                else:
                    history += f"\n--- {agent} Output ---\n{contribution}\n"
        except Exception as e:
            self.logger.warning(f"Council failed, falling back to Single Agent: {e}")
            yield "⚠️ *Quota Low: Running Single-Agent Mode...*"
            time.sleep(5)
            try:
                response = self.model.generate_content([f"Direct Answer Mode: {user_query}"])
                final_response = response.text
            except Exception as e2:
                final_response = f"❌ *Total Quota Depleted*: {str(e2)[:100]}"

        session.close()
        yield final_response
