import os

import ollama
import json

from Config import Log


class Model:
    def __init__(self):
        self.conversation = [{
            'role': 'system',
            'content': "Sei un chatbot di nome ROB ideato per conversare. Dai risposte brevissime e continua la conversazione nel linguaggio **italiano**."
        }]

    def analyze_images(self, image_path: str, verbose=False):
        pro = """
        The user provides an image. You should determine the information and output as JSON.
        Use the following schema:

        {{
            "objects_detected": a list of objects visible in the image,
            "scene_description": a short description of the scene in 2-3 words of the given image,
            "weather_conditions": which describes the weather in a single word
        }}

        Respond **ONLY** in this **JSON** format, without explanations or additional.
        """

        messages = [
            {
                'role': 'user',
                'content': pro,
                'images': [image_path]
            }
        ]

        if verbose:
            print(Log.ok(pro))

        res = ollama.chat(
            model=os.environ['OLLAMA_IMG_MODEL'],
            messages=messages
        )

        try:
            json_output = res['message']['content'].strip()
            if json_output and json_output[0] == '[':
                json_output = json_output[1:].strip()

            json_output = json.loads(json_output)
        except json.JSONDecodeError:
            print(Log.fail("Error: Response is not valid JSON!"))
            print(Log.warning(res['message']['content']))
            exit(1)

        return json_output

    def get_value(self, response, key):
        return response.get(key, "Key not found")

    def combined_chains(self, message, role):
        self.conversation.append(
            {
                'role': role,
                'content': message
            }
        )

    def conversations(self, message):
        self.combined_chains(message, "user")

        res = ollama.chat(
            model=os.environ["OLLAMA_CHAT_MODEL"],
            messages=self.conversation
        )

        self.combined_chains(res['message']['content'], "assistant")

        print(Log.ok(res['message']['content']))

    def get_conversation(self):
        return self.conversation