import time
from pynput import keyboard
from audio.recorder import AudioRecorder
from audio.transcriber import Transcriber
from brain.ollama_client import OllamaClient
from utils.executor import execute_command
from utils.ui import print_info, print_success, print_error, print_ai, confirm_execution
import config

class VoiceCoderApp:
    def __init__(self):
        self.recorder = AudioRecorder()
        self.transcriber = Transcriber(model_size=config.WHISPER_MODEL_SIZE)
        self.brain = OllamaClient(model=config.OLLAMA_MODEL)
        self.is_recording = False
        
        # Hotkey state
        self.current_keys = set()
        self.hotkey = {keyboard.Key.ctrl_l, keyboard.Key.alt_l, keyboard.KeyCode.from_char(config.HOTKEY_V)}
        
    def on_press(self, key):
        if key in self.hotkey:
            self.current_keys.add(key)
            if all(k in self.current_keys for k in self.hotkey):
                if not self.is_recording:
                    self.start_voice_command()

    def on_release(self, key):
        if key in self.current_keys:
            if all(k in self.current_keys for k in self.hotkey):
                if self.is_recording:
                    self.stop_voice_command()
            self.current_keys.remove(key)

    def start_voice_command(self):
        self.is_recording = True
        self.recorder.start_recording()
        print_info("Listening... (Release keys to stop)")

    def stop_voice_command(self):
        self.is_recording = False
        audio_data = self.recorder.stop_recording()
        
        if audio_data is None:
            print_error("No audio captured.")
            return

        print_info("Transcribing...")
        text = self.transcriber.transcribe(audio_data)
        
        if not text:
            print_error("Could not understand audio.")
            return
            
        print_success(f"You said: \"{text}\"")
        
        print_info("Thinking...")
        command = self.brain.generate_command(text)
        
        if not command:
            print_error("Failed to generate command.")
            return

        if confirm_execution(command):
            print_info(f"Executing: {command}")
            result = execute_command(command)
            print_ai(f"Output:\n{result}")
        else:
            print_info("Execution cancelled.")

    def run(self):
        print_success("VoiceCoder is active!")
        print_info("Press Ctrl + Alt + V to speak a command.")
        print_info("Press Ctrl + C to exit.")
        
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()

if __name__ == "__main__":
    try:
        app = VoiceCoderApp()
        app.run()
    except KeyboardInterrupt:
        print_info("Exiting...")
    except Exception as e:
        print_error(f"Fatal error: {e}")
