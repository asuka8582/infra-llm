import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY belum diisi di file .env")

# Configure Gemini
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction="""
Kamu adalah AI yang ramah, jelas, dan membantu.
Gunakan Bahasa Indonesia yang sopan dan mudah dipahami.
"""
)

chat = model.start_chat(history=[])

print("Chat Gemini LLM (ketik 'exit' untuk keluar)\n")

while True:
    user_input = input("Kamu: ")
    if user_input.lower() in ["exit", "quit"]:
        print("Keluar.")
        break

    response = chat.send_message(user_input)
    print(f"AI: {response.text}\n")
