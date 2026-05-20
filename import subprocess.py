import subprocess
import time
import requests
import os

MODEL_NAME = "mistral"

def start_ollama_server():
    try:
        requests.get("http://127.0.0.1:11434")
        print("Ollama server already running.")
    except:
        print("Starting Ollama server...")
        
        subprocess.Popen(
            ["ollama", "serve"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            shell=True
        )

        time.sleep(5)

def run_model():
    print(f"Starting model: {MODEL_NAME}")
    
    subprocess.run(
        ["ollama", "run", MODEL_NAME],
        shell=True
    )

if __name__ == "__main__":
    start_ollama_server()
    run_model()