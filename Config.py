from os import environ

class Config:
    def __init__(self):
        print("Setting environment variables...")
        environ['IMG_PATH'] = './images/'
        environ['OLLAMA_IMG_MODEL'] = "moondream"
        environ['OLLAMA_CHAT_MODEL'] = "llama2"
        environ['DATABASE_FILES'] = ('["./DALI/Examples/basic/drone1.txt",'
                                        '"./DALI/Examples/basic/pianificatore.txt",'
                                        '"./DALI/Examples/basic/drone2.txt"]')
        print()
        print(environ['IMG_PATH'])
        print(environ['OLLAMA_IMG_MODEL'])
        print(environ['DATABASE_FILES'])
        print()
        print("Environment variables setted")

class Log:
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
