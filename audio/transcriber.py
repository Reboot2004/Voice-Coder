from faster_whisper import WhisperModel
import os
import multiprocessing
from config import FORCE_CPU

class Transcriber:
    def __init__(self, model_size="distil-small.en", device="auto", compute_type="auto"):
        """
        model_size: "tiny", "base", "distil-small.en", "distil-medium.en"
        device: "cpu", "cuda", or "auto"
        compute_type: "int8", "float16", "int8_float16", or "auto"
        """
        # Auto-detect device
        if FORCE_CPU:
            device = "cpu"
        elif device == "auto":
            try:
                import ctranslate2
                device = "cuda" if ctranslate2.get_cuda_device_count() > 0 else "cpu"
            except:
                device = "cpu"
        
        # Optimization for local latency
        threads = 4
        self.model = None

        # Helper to verify if the model actually works
        def smoke_test(model):
            import numpy as np
            dummy = np.zeros(1600, dtype=np.float32)
            list(model.transcribe(dummy))
            return True

        # Try CUDA if available
        if device == "cuda":
            for ct in ["float16", "int8_float16", "int8"]:
                try:
                    print(f"Attempting CUDA ({ct})...")
                    m = WhisperModel(model_size, device="cuda", compute_type=ct, cpu_threads=threads, num_workers=1)
                    smoke_test(m)
                    self.model = m
                    print(f"✅ Success! Using CUDA ({ct})")
                    return
                except:
                    continue
            device = "cpu" # Fallback

        # CPU Mode
        try:
            print(f"Initializing on CPU (int8, Threads: {threads})...")
            m = WhisperModel(model_size, device="cpu", compute_type="int8", cpu_threads=threads, num_workers=1)
            smoke_test(m)
            self.model = m
            print(f"✅ Success! Using CPU with {model_size}")
        except Exception as e:
            raise RuntimeError(f"Could not initialize Whisper model: {e}")

    def transcribe(self, audio_data):
        if audio_data is None or len(audio_data) == 0:
            return ""

        segments, info = self.model.transcribe(audio_data, beam_size=5)
        text = " ".join([segment.text for segment in segments]).strip()
        return text
