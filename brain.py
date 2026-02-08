import google.generativeai as genai
from google.api_core import exceptions
from reasoning import ReasoningLayer
from tools import ToolExecutor

class AIBrain:
    """
    Core LLM logic for the AI system.
    Handles interaction with Google Gemini API, reasoning layer, and tools.
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
        self.tools = ToolExecutor()

    def generate_response(self, user_input, history, long_term_context=None):
        """
        Generates a response using the Gemini model, reasoning layer, and optional tool execution.
        """
        try:
            # 1. Start a chat with the provided history
            chat = self.model.start_chat(history=history)

            # 2. Use reasoning layer to format the initial prompt
            structured_prompt = self.reasoning.format_prompt(user_input, long_term_context)

            # 3. Initial generation
            response = chat.send_message(structured_prompt)
            raw_text = response.text

            # 4. Check for tool call
            tool_call = self.reasoning.extract_tool_call(raw_text)

            if tool_call and "error" not in tool_call:
                tool_name = tool_call.get("name")
                params = tool_call.get("params", {})

                # Execute tool
                tool_result = self.tools.execute(tool_name, params)

                # Format feedback
                feedback = self.reasoning.format_tool_result(tool_name, tool_result)

                # Second generation with tool result
                response = chat.send_message(feedback)
                raw_text = response.text
            elif tool_call and "error" in tool_call:
                # Handle tool call error
                raw_text = f"<final_answer>Maaf, terjadi kesalahan dalam memproses permintaan tool: {tool_call['error']}</final_answer>"

            # 5. Extract final answer
            final_answer = self.reasoning.extract_final_answer(raw_text)

            return final_answer

        except exceptions.GoogleAPIError as e:
            return f"Error: Masalah pada API Gemini - {str(e)}"
        except ValueError:
            # Handle cases where response is blocked by safety filters
            return "Maaf, saya tidak dapat menanggapi pesan tersebut karena alasan keamanan."
        except Exception as e:
            return f"Error: Terjadi kesalahan tidak terduga - {str(e)}"
