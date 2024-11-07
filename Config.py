import os

class Config:
    def __init__(self):
        print("Setting environment variables...")
        os.environ['IMG_PATH'] = './images/'
        os.environ['OLLAMA_IMG_MODEL'] = "moondream"
        print()
        print(os.environ['IMG_PATH'])
        print(os.environ['OLLAMA_IMG_MODEL'])
        print()
        print("Environment variables setted")
