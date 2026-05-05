import requests
import json

class OllamaClient:
    def __init__(self, model="llama3", base_url="http://localhost:11434"):
        self.model = model
        self.base_url = base_url
        self.system_prompt = (
            "You are a terminal coding assistant. You receive natural language instructions "
            "and must translate them into the most likely shell command or code snippet. "
            "Output ONLY the command or code, no explanation, no markdown backticks, "
            "unless specifically asked for a code block. If multiple steps are needed, "
            "separate them with && for shell commands."
        )

    def generate_command(self, user_input):
        payload = {
            "model": self.model,
            "prompt": f"{self.system_prompt}\n\nUser: {user_input}\nAssistant:",
            "stream": False
        }
        
        try:
            response = requests.post(f"{self.base_url}/api/generate", json=payload)
            response.raise_for_status()
            result = response.json()
            return result.get("response", "").strip()
        except Exception as e:
            return f"Error connecting to Ollama: {str(e)}"

if __name__ == "__main__":
    client = OllamaClient()
    cmd = client.generate_command("List all files in the current directory and sort by size")
    print(f"Generated command: {cmd}")
