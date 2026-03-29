class ShortTermMemory:
    """
    Manages the short-term conversation history for the AI brain.
    """
    def __init__(self, max_turns=10):
        self.max_turns = max_turns
        self.history = []

    def add_turn(self, role, content):
        """
        Adds a single message to the conversation history.
        Role should be 'user' or 'model'.
        """
        self.history.append({"role": role, "parts": [content]})

        # Maintain context window size (2 messages per turn: user and model)
        # max_turns * 2 ensures we keep the specified number of back-and-forth exchanges
        if len(self.history) > self.max_turns * 2:
            self.history = self.history[-(self.max_turns * 2):]

    def get_history(self):
        """
        Returns the conversation history in a format compatible with Gemini API.
        """
        return self.history

    def clear(self):
        """
        Clears all conversation history.
        """
        self.history = []
