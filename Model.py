from os import environ
from json import loads, dumps, JSONDecodeError
import ollama

from Config import Log


class Model:
    def __init__(self, verbose=False):
        self.conversation = [{
            'role': 'system',
            'content': (
                "Sei un assistente chatbot di nome BOB, progettato per fornire assistenza agli utenti riguardo alla spedizione "
                "dei loro pacchi. Rispondi in modo conciso e preciso, utilizzando le informazioni contenute nel JSON fornito "
                "dall'utente per identificare la posizione e lo stato del pacco. Se il JSON è vuoto o non pertinente, rispondi "
                "in modo naturale e colloquiale alla richiesta dell'utente, rimanendo sempre nel contesto dell'assistenza "
                "sulla spedizione dei pacchi. Se il JSON indica un cambiamento rispetto alla situazione precedente, segnala il progresso."
            )
        }]
        self.last_json = None
        self.verbose = verbose

    def extract_and_format_json(self, raw_content):
        try:
            start = raw_content.find('{')
            end = raw_content.rfind('}')

            if start == -1 or end == -1:
                raise ValueError("Il contenuto non contiene parentesi graffe valide.")

            json_snippet = raw_content[start:end + 1]

            formatted_json = loads(json_snippet)
            return formatted_json

        except JSONDecodeError:
            raise ValueError("Il contenuto non è un JSON valido dopo l'estrazione.") from None

    def analyze_images(self, image_path: str):
        pro = """
            The user provides an image. You should determine the information and respond in **valid JSON format** so inside the brackets.
            Use the following schema:
    
            {{
                "weather_conditions": "<weather_condition>"
            }}
    
            Where `<weather_condition>` must be a single word and **must** be one of the following: ['sunny', 'cloudy', 'snowy'].
    
            Respond **ONLY** with a valid **JSON** object. Do not add any explanation, text, or formatting outside of the JSON object.
        """

        messages = [
            {
                'role': 'user',
                'content': pro,
                'images': [image_path]
            }
        ]

        if self.verbose:
            print(Log.ok(pro))

        res = ollama.chat(
            model=environ['OLLAMA_IMG_MODEL'],
            messages=messages
        )

        try:
            json_output = res['message']['content'].strip()
            if json_output and json_output[0] == '[':
                json_output = json_output[1:].strip()
            json_output = self.extract_and_format_json(json_output)
            json_output = loads(dumps(json_output))

        except JSONDecodeError:
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

    def conversations(self, message, current_json):
        json_comparison_message = ""

        if self.last_json is not None:
            if current_json != self.last_json:
                json_comparison_message = "Il nuovo JSON indica un cambiamento rispetto allo stato precedente."

        self.last_json = current_json

        combined_message = (
            f"Messaggio utente: {message}\n"
            f"Dati correnti del pacco in JSON: {dumps(current_json, indent=2)}\n"
            f"{json_comparison_message}"
        )

        self.combined_chains(combined_message, "user")

        res = ollama.chat(
            model=environ["OLLAMA_CHAT_MODEL"],
            messages=self.conversation
        )

        self.combined_chains(res['message']['content'], "assistant")

        print(Log.ok(res['message']['content']))

    def get_conversation(self):
        return self.conversation