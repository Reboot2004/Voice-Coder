import subprocess
import os

def execute_command(command):
    """
    Executes a shell command and returns the output.
    """
    if not command or command.lower().startswith("error"):
        return "No valid command to execute."
    
    try:
        # Use shell=True for complex commands (pipes, etc) but be cautious
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        return result.stdout if result.stdout else "Command executed successfully (no output)."
    except subprocess.CalledProcessError as e:
        return f"Error executing command: {e.stderr}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"

if __name__ == "__main__":
    print(execute_command("dir"))
