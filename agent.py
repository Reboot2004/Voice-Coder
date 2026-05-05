import json
import time
from brain.ollama_client import OllamaClient
from utils.executor import execute_command
from utils.ui import print_info, print_success, print_error, print_ai, print_warning
import config

class VoiceAgent:
    def __init__(self, model=config.OLLAMA_MODEL):
        self.client = OllamaClient(model=model)
        self.history = []
        self.system_prompt = (
            "You are an autonomous terminal agent. You have access to the shell. "
            "When given a goal, you must think step-by-step and generate commands. "
            "After each command, you will receive the output. "
            "Use the output to decide your next move.\n\n"
            "Format your response as a JSON object with two fields:\n"
            "1. 'thought': Your reasoning about what to do next.\n"
            "2. 'command': The shell command to run, or 'DONE' if you have finished the task.\n\n"
            "Keep commands concise. If you need to read a file, use 'type' or 'cat'."
        )

    def run_task(self, initial_goal):
        print_success(f"Starting Agent Task: {initial_goal}")
        current_input = initial_goal
        self.history = [{"role": "system", "content": self.system_prompt}]
        
        max_steps = 5
        for step in range(max_steps):
            print_info(f"Step {step + 1}/{max_steps}...")
            
            # Prepare messages
            messages = self.history + [{"role": "user", "content": current_input}]
            
            # Get Agent Response (We'll use a raw generate call to get JSON)
            raw_response = self._get_json_response(messages)
            
            if not raw_response:
                print_error("Failed to get a valid response from the agent.")
                break
                
            thought = raw_response.get("thought", "Thinking...")
            command = raw_response.get("command", "DONE")
            
            print_ai(f"Thought: {thought}")
            
            if command == "DONE":
                print_success("Agent has completed the task.")
                break
                
            print_warning(f"Executing: {command}")
            output = execute_command(command)
            print_info(f"Output received ({len(output)} chars)")
            
            # Update history
            self.history.append({"role": "user", "content": current_input})
            self.history.append({"role": "assistant", "content": json.dumps(raw_response)})
            
            # Next input is the observation
            current_input = f"Command output: {output}"

        if step == max_steps - 1:
            print_warning("Agent reached maximum step limit.")

    def _get_json_response(self, messages):
        # Format the full conversation for Ollama
        prompt = ""
        for m in messages:
            role = m['role'].upper()
            content = m['content']
            prompt += f"{role}: {content}\n"
        prompt += "ASSISTANT (JSON):"

        payload = {
            "model": self.client.model,
            "prompt": prompt,
            "stream": False,
            "format": "json" # Ollama supports forced JSON output
        }
        
        try:
            response = requests.post(f"{self.client.base_url}/api/generate", json=payload)
            response.raise_for_status()
            res_json = response.json()
            return json.loads(res_json.get("response", "{}"))
        except Exception as e:
            print_error(f"Agent Logic Error: {e}")
            return None

# We need requests in agent.py too
import requests
