import time
from pynput import keyboard
from audio.recorder import AudioRecorder
from audio.transcriber import Transcriber
from agent import VoiceAgent
from utils.ui import print_info, print_success, print_error, print_ai
import config

class VoiceAgentApp:
    def __init__(self):
        self.recorder = AudioRecorder()
        self.transcriber = Transcriber(model_size=config.WHISPER_MODEL_SIZE)
        self.agent = VoiceAgent(model=config.OLLAMA_MODEL)
        self.is_recording = False
        
        # Hotkey state
        self.current_keys = set()
        self.hotkey = {keyboard.Key.ctrl_l, keyboard.Key.alt_l, keyboard.KeyCode.from_char(config.HOTKEY_V)}
        
    def on_press(self, key):
        if key in self.hotkey:
            self.current_keys.add(key)
            if all(k in self.current_keys for k in self.hotkey):
                if not self.is_recording:
                    self.is_recording = True
                    self.recorder.start_recording()
                    print_info("Listening for AGENT task... (Release keys to start)")

    def on_release(self, key):
        if key in self.current_keys:
            if all(k in self.current_keys for k in self.hotkey):
                if self.is_recording:
                    self.is_recording = False
                    self.handle_agent_goal()
            self.current_keys.remove(key)

    def handle_agent_goal(self):
        audio_data = self.recorder.stop_recording()
        if audio_data is None:
            print_error("No audio captured.")
            return

        print_info("Transcribing Goal...")
        goal = self.transcriber.transcribe(audio_data)
        
        if not goal:
            print_error("Could not understand goal.")
            return
            
        print_success(f"Goal set: \"{goal}\"")
        
        # Start the autonomous loop
        try:
            self.agent.run_task(goal)
        except Exception as e:
            print_error(f"Agent Loop Failed: {e}")

    def run(self):
        print_success("--- AGENT MODE ACTIVE ---")
        print_info("Hold Ctrl + Alt + V to give the Agent a task.")
        print_info("Example: 'Create a test.py file and run it to see if it works'")
        
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()

if __name__ == "__main__":
    app = VoiceAgentApp()
    app.run()
