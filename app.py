import os
from dotenv import load_dotenv
from brain import AIBrain
from memory import ShortTermMemory
from long_memory import LongTermMemory

# Load environment variables
load_dotenv()

def main():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "YOUR_API_KEY_HERE":
        print("Error: GEMINI_API_KEY belum dikonfigurasi di file .env")
        print("Silakan ikuti petunjuk di README.md untuk pengaturan API Key.")
        return

    # Initialize components
    brain = AIBrain(api_key=api_key)
    memory = ShortTermMemory(max_turns=10)

    print("Initializing Long-Term Memory (Stage 2)...")
    ltm = LongTermMemory()

    print("\n=== AI Core System (CLI) ===")
    print("Sistem siap. Silakan kirim pesan atau ketik 'exit' untuk keluar.")
    print("=" * 28 + "\n")

    while True:
        try:
            # Get user input
            user_input = input("User: ").strip()

            if not user_input:
                continue

            if user_input.lower() in ["exit", "quit"]:
                print("\nSistem dimatikan. Sampai jumpa.")
                break

            # 1. Retrieve relevant context from Long-Term Memory
            ltm_context = ltm.query_memory(user_input)

            # 2. Get response from brain using short-term and long-term context
            response_text = brain.generate_response(
                user_input,
                memory.get_history(),
                long_term_context=ltm_context
            )

            # Print response
            print(f"AI: {response_text}\n")

            # Update short-term memory with this exchange
            memory.add_turn("user", user_input)
            memory.add_turn("model", response_text)

        except KeyboardInterrupt:
            print("\n\nSistem dihentikan paksa. Keluar...")
            break
        except Exception as e:
            print(f"Terjadi kesalahan pada sistem: {e}\n")

if __name__ == "__main__":
    main()
