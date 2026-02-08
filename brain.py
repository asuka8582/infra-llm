import google.generativeai as genai
from google.api_core import exceptions
from reasoning import ReasoningLayer

class AIBrain:
    """
    Core LLM logic for the AI system.
    Handles interaction with Google Gemini API and reasoning layer.
    """
    def __init__(self, api_key, model_name="gemini-1.5-flash"):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(
            model_name=model_name,
            system_instruction=(
                "Kamu adalah AI Core yang cerdas, netral, dan membantu. "
                "Tugasmu adalah berpikir logis dan memberikan jawaban yang akurat dalam Bahasa Indonesia. "
                "Gunakan nada bicara yang sopan, profesional, dan dewasa. "
                "Jangan berpura-pura menjadi manusia, tetaplah menjadi entitas AI yang membantu."
            )
        )
        self.reasoning = ReasoningLayer()

    def generate_response(self, user_input, history, long_term_context=None):
        """
        Generates a response using the Gemini model and reasoning layer.
        """
        try:
            # 1. Use reasoning layer to format the prompt
            structured_prompt = self.reasoning.format_prompt(user_input, long_term_context)

            # 2. Start a chat with the provided history
            chat = self.model.start_chat(history=history)

            # 3. Send the structured prompt
            response = chat.send_message(structured_prompt)
            raw_text = response.text

            # 4. Extract final answer from reasoning
            final_answer = self.reasoning.extract_final_answer(raw_text)

            return final_answer

        except exceptions.GoogleAPIError as e:
            return f"Error: Masalah pada API Gemini - {str(e)}"
        except ValueError:
            # Handle cases where response is blocked by safety filters
            return "Maaf, saya tidak dapat menanggapi pesan tersebut karena alasan keamanan."
        except Exception as e:
            return f"Error: Terjadi kesalahan tidak terduga - {str(e)}"
