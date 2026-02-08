import os
import google.generativeai as genai
from google.api_core import exceptions
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "YOUR_API_KEY_HERE":
        print("Error: GEMINI_API_KEY belum diisi di file .env")
        print("Silakan salin .env.example ke .env dan masukkan API Key Anda.")
        return

    # Configure Gemini
    genai.configure(api_key=api_key)

    try:
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction="""
Kamu adalah AI yang ramah, jelas, dan membantu.
Gunakan Bahasa Indonesia yang sopan dan mudah dipahami.
"""
        )
        chat = model.start_chat(history=[])
    except Exception as e:
        print(f"Error saat menginisialisasi model: {e}")
        return

    print("=== Chat Gemini LLM (CLI) ===")
    print("Ketik 'exit' atau 'quit' untuk keluar.\n")

    while True:
        try:
            user_input = input("Kamu: ").strip()

            if not user_input:
                continue

            if user_input.lower() in ["exit", "quit"]:
                print("Terima kasih! Sampai jumpa.")
                break

            response = chat.send_message(user_input)

            try:
                # Menampilkan respon teks
                print(f"AI: {response.text}\n")
            except ValueError:
                # Terjadi jika respon diblokir oleh filter keamanan
                print("AI: Maaf, saya tidak bisa merespons pesan tersebut karena filter keamanan.\n")

        except exceptions.GoogleAPIError as e:
            print(f"Error dari API: {e}\n")
        except KeyboardInterrupt:
            print("\nKeluar...")
            break
        except Exception as e:
            print(f"Terjadi kesalahan: {e}\n")

if __name__ == "__main__":
    main()
