import sounddevice as sd
import numpy as np
import queue
import sys

class AudioRecorder:
    def __init__(self, sample_rate=16000, channels=1):
        self.sample_rate = sample_rate
        self.channels = channels
        self.audio_queue = queue.Queue()
        self.recording = False
        self.stream = None

    def _callback(self, indata, frames, time, status):
        if status:
            print(status, file=sys.stderr)
        if self.recording:
            self.audio_queue.put(indata.copy())

    def start_recording(self):
        if not self.recording:
            self.recording = True
            self.audio_queue = queue.Queue()
            self.stream = sd.InputStream(
                samplerate=self.sample_rate,
                channels=self.channels,
                callback=self._callback
            )
            self.stream.start()
            print("Recording started...")

    def stop_recording(self):
        if self.recording:
            self.recording = False
            if self.stream:
                self.stream.stop()
                self.stream.close()
            print("Recording stopped.")
            
            # Combine all chunks into one numpy array
            chunks = []
            while not self.audio_queue.empty():
                chunks.append(self.audio_queue.get())
            
            if not chunks:
                return None
            
            return np.concatenate(chunks, axis=0).flatten()

if __name__ == "__main__":
    # Test recording
    import time
    recorder = AudioRecorder()
    recorder.start_recording()
    time.sleep(3)
    audio_data = recorder.stop_recording()
    print(f"Recorded {len(audio_data)} samples.")
