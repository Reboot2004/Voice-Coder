import sys
import os
# Add current dir to path to import local modules
sys.path.append(os.getcwd())

from brain.ollama_client import OllamaClient
from colorama import Fore, Style, init
import config

init()

def simulate_command(user_voice_input):
    client = OllamaClient(model=config.OLLAMA_MODEL)
    
    print(f"\n{Fore.CYAN}--- SIMULATION START ---{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Voice Input:{Style.RESET_ALL} \"{user_voice_input}\"")
    
    print(f"{Fore.BLUE}Thinking...{Style.RESET_ALL}")
    command = client.generate_command(user_voice_input)
    
    print(f"{Fore.GREEN}System Understood:{Style.RESET_ALL} (Model: {config.OLLAMA_MODEL})")
    print(f"{Fore.WHITE}{Style.BRIGHT}{command}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}--- SIMULATION END ---{Style.RESET_ALL}")

if __name__ == "__main__":
    test_commands = [
        "Create a folder named backup and copy all python files into it",
        "Show me the current date and time",
        "Initialize a new git repository and make the first commit called initial commit"
    ]
    
    for cmd in test_commands:
        simulate_command(cmd)
