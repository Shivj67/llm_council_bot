import google.generativeai as genai
import time
import os
import logging
from app.agents import COUNCIL_PROMPTS, MODE_PROMPTS

class LLMCouncil:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-flash-latest')
        self.logger = logging.getLogger(__name__)

    def run_council(self, user_query, mode="learning"):
        self.logger.info(f"Starting Council for query: {user_query[:50]}... in mode: {mode}")
        
        mode_context = MODE_PROMPTS.get(mode.lower(), MODE_PROMPTS["learning"])
        history = f"USER QUERY: {user_query}\nMODE CONTEXT: {mode_context}\n"
        
        agent_order = ["Analyst", "Researcher", "Critic", "Optimizer", "Final Judge"]
        final_response = ""

        for agent in agent_order:
            yield agent # Yield the name of the agent currently working
            try:
                system_prompt = COUNCIL_PROMPTS[agent]
                prompt = f"System: {system_prompt}\n\nCOUNCIL HISTORY:\n{history}\n\nAction: Provide your contribution."
                
                # Increased delay to 6s for ultra-stability
                time.sleep(6) 
                
                response = self.model.generate_content(prompt)
                contribution = response.text if response and hasattr(response, 'text') else f"Agent {agent} failed to respond."
                
                if agent == "Final Judge":
                    final_response = contribution
                else:
                    history += f"\n--- {agent} Output ---\n{contribution}\n"
                
                self.logger.info(f"Completed {agent} phase.")
                
            except Exception as e:
                self.logger.error(f"Error in {agent} phase: {e}")
                history += f"\n--- {agent} Output ---\nError occurred: {e}\n"

        if not final_response:
            yield "❌ *The Council was unable to reach a decision.*"
        else:
            yield final_response
