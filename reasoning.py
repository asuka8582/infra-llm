import re
import json

class ReasoningLayer:
    """
    Handles the structured reasoning process and tool selection for the AI system.
    """

    def __init__(self):
        self.tools_doc = """
Daftar Tool yang tersedia:
1. web_search(query): Mencari informasi di internet.
2. read_file(file_path): Membaca isi file di dalam sandbox.
3. write_file(file_path, content): Menulis konten ke file di dalam sandbox.
4. list_directory(directory_path): Melihat daftar file di direktori sandbox.
5. run_command(command): Menjalankan perintah terbatas (ls, pwd, python script.py, pip list).
6. write_memory(fact): Menyimpan informasi penting ke memori jangka panjang.
"""

        self.reasoning_instruction = (
            "\n\nInstruksi Tambahan: Sebelum memberikan jawaban akhir, lakukan penalaran internal secara bertahap. "
            "Jika Anda membutuhkan informasi tambahan atau perlu mengambil tindakan, Anda dapat memanggil SATU tool.\n"
            "Gunakan format berikut dalam respons Anda:\n"
            "<reasoning>\n"
            "[Analisis niat pengguna, evaluasi memori, dan tentukan apakah perlu memanggil tool]\n"
            "</reasoning>\n"
            "(Opsional) <tool_call>\n"
            '{"name": "nama_tool", "params": {"param1": "value1"}}\n'
            "</tool_call>\n"
            "<final_answer>\n"
            "[Jawaban akhir dalam Bahasa Indonesia. Jika memanggil tool, berikan jawaban sementara atau tunggu hasil]\n"
            "</final_answer>"
        )

    def format_prompt(self, user_input, long_term_context=None):
        """
        Constructs a structured internal prompt that encourages reasoning and tool use.
        """
        prompt = user_input
        if long_term_context:
            prompt = (
                f"Konteks Memori Jangka Panjang:\n{long_term_context}\n\n"
                f"Pertanyaan Pengguna: {user_input}"
            )

        return prompt + "\n" + self.tools_doc + self.reasoning_instruction

    def extract_tool_call(self, raw_response):
        """
        Extracts tool call JSON from the response.
        """
        match = re.search(r'<tool_call>(.*?)</tool_call>', raw_response, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1).strip())
            except json.JSONDecodeError:
                return {"error": "Invalid JSON in tool_call"}
        return None

    def format_tool_result(self, tool_name, result):
        """
        Formats the tool result to be fed back into the brain.
        """
        return (
            f"\nHasil dari eksekusi tool '{tool_name}':\n"
            f"```\n{result}\n```\n"
            "Berdasarkan hasil ini, berikan jawaban akhir (<final_answer>) kepada pengguna."
        )

    def extract_final_answer(self, raw_response):
        """
        Parses the raw LLM output to extract only the final answer.
        """
        match = re.search(r'<final_answer>(.*?)</final_answer>', raw_response, re.DOTALL)

        if match:
            return match.group(1).strip()

        # Fallback
        clean_response = re.sub(r'<reasoning>.*?</reasoning>', '', raw_response, flags=re.DOTALL)
        clean_response = re.sub(r'<tool_call>.*?</tool_call>', '', clean_response, flags=re.DOTALL)
        return clean_response.strip()
