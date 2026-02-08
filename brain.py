import google.generativeai as genai
from google.api_core import exceptions

class AIBrain:
    """
    Core LLM logic for the AI system.
    Handles interaction with Google Gemini API.
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

    def generate_response(self, user_input, history):
        """
        Generates a response using the Gemini model given user input and history.
        """
        try:
            # Start a chat with the provided history
            chat = self.model.start_chat(history=history)
            response = chat.send_message(user_input)
            return response.text
        except exceptions.GoogleAPIError as e:
            return f"Error: Masalah pada API Gemini - {str(e)}"
        except ValueError:
            # Handle cases where response is blocked by safety filters
            return "Maaf, saya tidak dapat menanggapi pesan tersebut karena alasan keamanan."
        except Exception as e:
            return f"Error: Terjadi kesalahan tidak terduga - {str(e)}"
