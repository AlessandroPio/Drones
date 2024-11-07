import os

class Config:
    def __init__(self):
        print("Setting environment variables...")
        os.environ['IMG_PATH'] = './images/'
        os.environ['OLLAMA_IMG_MODEL'] = "moondream"
        os.environ['OLLAMA_CHAT_MODEL'] = "llama2"
        print()
        print(os.environ['IMG_PATH'])
        print(os.environ['OLLAMA_IMG_MODEL'])
        print()
        print("Environment variables setted")


class Log:
    # COLORS
    HEADER = '\033[95m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    @staticmethod
    def ok(message):
        return f"{Log.OKGREEN}{message}{Log.ENDC}"

    @staticmethod
    def warning(message):
        return f"{Log.WARNING}{message}{Log.ENDC}"

    @staticmethod
    def fail(message):
        return f"{Log.FAIL}{message}{Log.ENDC}"

    @staticmethod
    def header(message):
        return f"{Log.HEADER}{message}{Log.ENDC}"
