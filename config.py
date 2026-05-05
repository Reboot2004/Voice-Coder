import os

# --- Hardware Settings ---
# Set to True to skip CUDA checks entirely and run on CPU
FORCE_CPU = True

# --- Model Settings ---
# Whisper model: "distil-small.en" (Fast & Accurate), "distil-medium.en"
WHISPER_MODEL_SIZE = "distil-small.en"

# Ollama model for logic: "llama3", "codellama", "phi3"
OLLAMA_MODEL = "llama3"

# --- Hotkey Settings ---
# Default: Ctrl + Alt + V
HOTKEY_V = 'v'
