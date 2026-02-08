import re

class ReasoningLayer:
    """
    Handles the structured reasoning process for the AI system.
    Encapsulates the logic of thinking step-by-step before producing an output.
    """

    def __init__(self):
        self.reasoning_instruction = (
            "\n\nInstruksi Tambahan: Sebelum memberikan jawaban akhir, lakukan penalaran internal secara bertahap. "
            "Gunakan format berikut dalam respons Anda:\n"
            "<reasoning>\n"
            "[Analisis niat pengguna, evaluasi memori/konteks, dan rencanakan jawaban di sini]\n"
            "</reasoning>\n"
            "<final_answer>\n"
            "[Tuliskan jawaban akhir Anda dalam Bahasa Indonesia di sini]\n"
            "</final_answer>"
        )

    def format_prompt(self, user_input, long_term_context=None):
        """
        Constructs a structured internal prompt that encourages reasoning.
        """
        prompt = user_input
        if long_term_context:
            prompt = (
                f"Konteks Memori Jangka Panjang:\n{long_term_context}\n\n"
                f"Pertanyaan Pengguna: {user_input}"
            )

        return prompt + self.reasoning_instruction

    def extract_final_answer(self, raw_response):
        """
        Parses the raw LLM output to extract only the final answer.
        Returns the content within <final_answer> tags, or the raw response if tags are missing.
        """
        # Search for content inside <final_answer> tags
        match = re.search(r'<final_answer>(.*?)</final_answer>', raw_response, re.DOTALL)

        if match:
            return match.group(1).strip()

        # Fallback: if <final_answer> is missing, try to remove <reasoning> if it exists
        clean_response = re.sub(r'<reasoning>.*?</reasoning>', '', raw_response, flags=re.DOTALL)
        return clean_response.strip()
