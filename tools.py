import os
import subprocess
import json
from duckduckgo_search import DDGS

class ToolExecutor:
    """
    Registry and executor for AI tools with safety boundaries.
    """
    def __init__(self, ltm, sandbox_dir="sandbox"):
        self.sandbox_dir = sandbox_dir
        if not os.path.exists(self.sandbox_dir):
            os.makedirs(self.sandbox_dir)

        self.ltm = ltm
        self.command_whitelist = ["ls", "pwd", "python", "pip"]

    def _get_sandbox_path(self, path):
        """Ensures the path is within the sandbox."""
        normalized = os.path.normpath(path)
        if normalized.startswith("..") or os.path.isabs(normalized):
            abs_sandbox = os.path.abspath(self.sandbox_dir)
            abs_path = os.path.abspath(os.path.join(self.sandbox_dir, normalized) if not os.path.isabs(normalized) else normalized)
            if not abs_path.startswith(abs_sandbox):
                raise PermissionError(f"Access to path '{path}' is denied (outside sandbox).")
            return abs_path
        return os.path.join(self.sandbox_dir, normalized)

    def web_search(self, query):
        """Searches the web and returns text-only results."""
        try:
            with DDGS() as ddgs:
                results = [r['body'] for r in ddgs.text(query, max_results=5)]
                return "\n---\n".join(results)
        except Exception as e:
            return f"Error during web search: {str(e)}"

    def read_file(self, file_path):
        """Reads a file from the sandbox."""
        try:
            full_path = self._get_sandbox_path(file_path)
            if not os.path.exists(full_path):
                return f"Error: File '{file_path}' not found."
            with open(full_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            return f"Error reading file: {str(e)}"

    def write_file(self, file_path, content):
        """Writes content to a file in the sandbox."""
        try:
            full_path = self._get_sandbox_path(file_path)
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)
            return f"Successfully wrote to '{file_path}'."
        except Exception as e:
            return f"Error writing file: {str(e)}"

    def list_directory(self, directory_path="."):
        """Lists files in a sandbox directory."""
        try:
            full_path = self._get_sandbox_path(directory_path)
            if not os.path.isdir(full_path):
                return f"Error: '{directory_path}' is not a directory."
            return "\n".join(os.listdir(full_path))
        except Exception as e:
            return f"Error listing directory: {str(e)}"

    def run_command(self, command):
        """Runs a whitelisted command securely."""
        try:
            cmd_parts = command.split()
            if not cmd_parts:
                return "Error: Perintah kosong."

            base_cmd = cmd_parts[0]

            # Strict whitelist check
            is_whitelisted = False
            if base_cmd in ["ls", "pwd"]:
                is_whitelisted = True
            elif base_cmd == "python" and len(cmd_parts) > 1:
                # Basic protection: ensure no obvious piping/redirection characters
                if all(char not in command for char in [";", "&", "|", ">", "<"]):
                    is_whitelisted = True
            elif base_cmd == "pip" and len(cmd_parts) == 2 and cmd_parts[1] == "list":
                is_whitelisted = True

            if not is_whitelisted:
                return f"Error: Command '{command}' is not whitelisted or contains forbidden characters."

            # Execute with shell=False to prevent shell injection
            result = subprocess.run(
                cmd_parts,
                shell=False,
                capture_output=True,
                text=True,
                cwd=os.path.abspath(self.sandbox_dir),
                timeout=10
            )
            return f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        except subprocess.TimeoutExpired:
            return "Error: Command timed out."
        except FileNotFoundError:
            return f"Error: Command '{base_cmd}' not found."
        except Exception as e:
            return f"Error running command: {str(e)}"

    def write_memory(self, fact, importance=5):
        """Saves a fact to long-term memory with importance score."""
        try:
            res = self.ltm.add_memory(fact, importance=importance)
            if res == "Success":
                return f"Fact recorded (importance: {importance}): '{fact}'"
            return res # Discarded message
        except Exception as e:
            return f"Error writing to memory: {str(e)}"

    def execute(self, tool_name, params):
        """Dispatches tool execution."""
        tools_map = {
            "web_search": self.web_search,
            "read_file": self.read_file,
            "write_file": self.write_file,
            "list_directory": self.list_directory,
            "run_command": self.run_command,
            "write_memory": self.write_memory
        }

        if tool_name not in tools_map:
            return f"Error: Tool '{tool_name}' not found."

        try:
            return tools_map[tool_name](**params)
        except TypeError as e:
            return f"Error: Invalid parameters for tool '{tool_name}': {str(e)}"
        except Exception as e:
            return f"Error executing tool '{tool_name}': {str(e)}"
