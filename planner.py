import re

class PlannerLayer:
    """
    Handles the internal planning and multi-step thinking process for the AI system.
    This layer helps the AI break down complex requests into actionable steps.
    """

    def __init__(self):
        self.planner_instruction = """
### TAHAPAN PERENCANAAN & EKSEKUSI ###
Sebelum memberikan jawaban akhir, Anda wajib mengikuti tahapan internal berikut:

1. <intent_analysis>: Analisis mendalam tentang apa yang sebenarnya diinginkan pengguna.
2. <plan>: Susun rencana langkah-demi-langkah (ordered list) untuk menyelesaikan permintaan.
3. <step_execution>: Jalankan rencana tersebut secara internal. Tentukan pemikiran logis dan apakah perlu memanggil tool di sini.
"""

    def get_instruction(self):
        """
        Returns the planning instructions to be included in the prompt.
        """
        return self.planner_instruction

    def extract_plan(self, raw_response):
        """
        Extracts the generated plan from the raw response.
        """
        match = re.search(r'<plan>(.*?)</plan>', raw_response, re.DOTALL)
        if match:
            return match.group(1).strip()
        return None
