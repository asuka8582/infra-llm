import google.generativeai as genai
import re
from google.api_core import exceptions
from reasoning import ReasoningLayer
from tools import ToolExecutor

class AIBrain:
    """
    Core LLM logic for the AI system with quality improvements (Stage 5).
    """
    def __init__(self, api_key, ltm, model_name="gemini-1.5-flash"):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(
            model_name=model_name,
            system_instruction=(
                "Kamu adalah AI Core yang cerdas, netral, dan membantu. "
                "Tugasmu adalah berpikir logis dan memberikan jawaban yang akurat dalam Bahasa Indonesia. "
                "Gunakan nada bicara yang sopan, profesional, dan dewasa. "
                "Patuhi instruksi kualitas dan format respons yang diberikan dalam prompt."
            )
        )
        self.reasoning = ReasoningLayer()
        self.tools = ToolExecutor(ltm=ltm)

    def _evaluate_importance(self, fact):
        """
        Evaluates the importance of a fact using the LLM.
        """
        try:
            prompt = self.reasoning.get_importance_eval_prompt(fact)
            response = self.model.generate_content(prompt)
            # Extract number from response
            score_match = re.search(r'\d+', response.text)
            if score_match:
                return int(score_match.group())
            return 5 # Default importance
        except:
            return 5

    def generate_response(self, user_input, history, long_term_context=None):
        """
        Generates a validated response using reasoning, tools, and quality checks.
        """
        try:
            # 1. Start chat session
            chat = self.model.start_chat(history=history)

            # 2. Format and send structured prompt
            structured_prompt = self.reasoning.format_prompt(user_input, long_term_context)
            response = chat.send_message(structured_prompt)
            raw_text = response.text

            # 3. Check for tool call
            tool_call = self.reasoning.extract_tool_call(raw_text)

            if tool_call and "error" not in tool_call:
                tool_name = tool_call.get("name")
                params = tool_call.get("params", {})

                # Special handling for write_memory importance if not provided
                if tool_name == "write_memory" and "importance" not in params:
                    fact = params.get("fact", "")
                    params["importance"] = self._evaluate_importance(fact)

                # Execute tool
                tool_result = self.tools.execute(tool_name, params)

                # Feedback to brain for final answer and validation
                feedback = self.reasoning.format_tool_result(tool_name, tool_result)
                response = chat.send_message(feedback)
                raw_text = response.text

            elif tool_call and "error" in tool_call:
                raw_text = f"<final_answer>Kesalahan Tool: {tool_call['error']}</final_answer>"

            # 4. Extract final validated answer
            final_answer = self.reasoning.extract_final_answer(raw_text)

            return final_answer

        except exceptions.GoogleAPIError as e:
            return f"Error API: {str(e)}"
        except ValueError:
            return "Maaf, pesan diblokir oleh filter keamanan."
        except Exception as e:
            return f"Kesalahan Sistem: {str(e)}"
