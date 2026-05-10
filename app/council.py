import google.generativeai as genai
import time
import logging
from app.agents import COUNCIL_PROMPTS, MODE_PROMPTS
from app.database import get_session, AuditLog, Message

class LLMCouncil:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        # Initialize model with Google Search tool enabled
        # Switching to 2.0 Flash for a fresh quota
        self.model = genai.GenerativeModel('gemini-2.0-flash')
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
        if depth == "quick":
            agent_order = ["Analyst", "Final Judge"]
        elif depth == "deep":
            agent_order = ["Analyst", "Critic", "Final Judge"]
        else: # standard
            agent_order = ["Analyst", "Final Judge"]

        final_response = ""

        for agent in agent_order:
            yield agent
            try:
                system_prompt = COUNCIL_PROMPTS[agent]
                
                # Prepare content (Multimodal Support)
                content_parts = [f"System: {system_prompt}\n\nCOUNCIL HISTORY:\n{history}\n\nAction: Provide your contribution."]
                if media:
                    content_parts.append(media) # Append image/audio data if present

                time.sleep(20) # Rate limit protection
                
                response = self.model.generate_content(content_parts)
                contribution = response.text if response and hasattr(response, 'text') else f"Agent {agent} failed to respond."
                
                # Audit Logging for Dashboard
                audit = AuditLog(user_id=user_id, query=user_query, agent_name=agent, agent_output=contribution)
                session.add(audit)
                session.commit()

                if agent == "Final Judge":
                    final_response = contribution
                else:
                    history += f"\n--- {agent} Output ---\n{contribution}\n"
                
                self.logger.info(f"Completed {agent} phase.")
                
            except Exception as e:
                self.logger.error(f"Error in {agent} phase: {e}")
                history += f"\n--- {agent} Output ---\nError occurred: {e}\n"

        session.close()

        if not final_response:
            yield "❌ *The Council was unable to reach a decision.*"
        else:
            yield final_response
