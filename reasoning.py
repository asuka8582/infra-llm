import re
import json

class ReasoningLayer:
    """
    Handles structured reasoning, tool selection, and response validation.
    """

    def __init__(self):
        self.tools_doc = """
### TOOLS TERSEDIA ###
1. web_search(query): Mencari informasi terbaru di internet.
2. read_file(file_path): Membaca file di sandbox.
3. write_file(file_path, content): Menulis file di sandbox.
4. list_directory(directory_path): Melihat daftar file di sandbox.
5. run_command(command): Menjalankan perintah terbatas (ls, pwd, python, pip list).
6. write_memory(fact, importance): Menyimpan fakta penting (skor 1-10) ke memori jangka panjang.
"""

        self.quality_instruction = """
### INSTRUKSI KUALITAS ###
- Berikan jawaban dalam Bahasa Indonesia yang sopan, cerdas, dan membantu.
- Hindari halusinasi. Jika tidak tahu, katakan tidak tahu.
- Pastikan jawaban konsisten dengan memori dan konteks yang diberikan.
- Gunakan nada bicara yang dewasa dan profesional.
"""

        self.reasoning_instruction = """
### FORMAT RESPONS ###
Gunakan format berikut secara berurutan:
1. <reasoning>: Analisis niat pengguna, evaluasi memori, dan tentukan rencana.
2. <tool_call> (Opsional): Panggil SATU tool jika diperlukan. Format: {"name": "...", "params": {...}}
3. <initial_answer>: Draft jawaban pertama Anda.
4. <validation>: Tinjau draft Anda (kejelasan, konsistensi, kebenaran).
5. <final_answer>: Jawaban akhir yang telah divalidasi dan diperbaiki.
"""

    def format_prompt(self, user_input, long_term_context=None):
        """
        Constructs a structured prompt separating rules, context, and input.
        """
        prompt = "### ATURAN SISTEM ###\n"
        prompt += self.quality_instruction + "\n"
        prompt += self.tools_doc + "\n"
        prompt += self.reasoning_instruction + "\n\n"

        prompt += "### KONTEKS ###\n"
        if long_term_context:
            prompt += f"Memori Jangka Panjang:\n{long_term_context}\n\n"
        else:
            prompt += "Memori Jangka Panjang: Tidak ada informasi relevan ditemukan.\n\n"

        prompt += "### INPUT PENGGUNA ###\n"
        prompt += user_input + "\n"

        return prompt

    def extract_tool_call(self, raw_response):
        """
        Extracts tool call JSON from the response.
        """
        match = re.search(r'<tool_call>(.*?)</tool_call>', raw_response, re.DOTALL)
        if match:
            try:
                content = match.group(1).strip()
                # Simple cleanup for JSON
                if content.startswith("```json"):
                    content = content[7:-3].strip()
                return json.loads(content)
            except json.JSONDecodeError:
                return {"error": "Format JSON tidak valid dalam tool_call"}
        return None

    def format_tool_result(self, tool_name, result):
        """
        Formats the tool result to be fed back into the brain.
        """
        return (
            f"\n### HASIL TOOL: {tool_name} ###\n"
            f"```\n{result}\n```\n"
            "Gunakan hasil ini untuk melengkapi penalaran dan memberikan <final_answer> yang divalidasi."
        )

    def extract_final_answer(self, raw_response):
        """
        Parses the raw LLM output to extract only the final validated answer.
        """
        match = re.search(r'<final_answer>(.*?)</final_answer>', raw_response, re.DOTALL)

        if match:
            return match.group(1).strip()

        # Fallback cascade
        for tag in ['initial_answer', 'reasoning']:
            match = re.search(f'<{tag}>(.*?)</{tag}>', raw_response, re.DOTALL)
            if match:
                return match.group(1).strip()

        # Remove all tags for raw output
        clean_response = re.sub(r'<.*?>', '', raw_response, flags=re.DOTALL)
        return clean_response.strip()

    def get_importance_eval_prompt(self, fact):
        """
        Prompt for evaluating the importance of a fact.
        """
        return (
            f"Evaluasi tingkat kepentingan fakta berikut untuk disimpan dalam memori jangka panjang: '{fact}'\n"
            "Berikan skor dari 1 sampai 10, di mana:\n"
            "1-2: Trivial/Sapaan/Obrolan ringan tidak penting.\n"
            "3-5: Informasi umum yang mungkin berguna.\n"
            "6-8: Informasi spesifik tentang preferensi pengguna atau data teknis.\n"
            "9-10: Informasi kritis atau instruksi permanen.\n\n"
            "Hanya berikan angka skornya saja (1-10)."
        )
