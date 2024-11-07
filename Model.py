import ollama
import json

class Model:
    def __init__(self):
        # Imposta il contesto iniziale per la conversazione
        self.conversation = [{
            'role': 'system',
            'content': "Sei un chatbot di nome ROB ideato per conversare. Dai risposte brevissime e rispondi in **italiano**."
        }]

    def analyze_images(self, image_path: str, verbose=False):
        pro = """
        The user provides an image. You should determine the information and output as JSON.
        Use the following schema:

        {
            "objects_detected": a list of objects visible in the image,
            "scene_description": a short description of the scene in 2-3 words of the given image,
            "weather_conditions": which describes the weather in a single word
        }

        Respond ONLY in this JSON format, without explanations or additional.
        """

        messages = [
            {
                'role': 'user',
                'content': pro,
                'images': [image_path]
            }
        ]

        if verbose:
            print(pro)

        # Chiamata al modello per analizzare l'immagine
        res = ollama.chat(
            model="moondream",
            messages=messages
        )

        # Parsing JSON e gestione degli errori
        try:
            json_output = json.loads(res['message']['content'])
        except json.JSONDecodeError:
            print("Errore: La risposta non è in formato JSON.")
            return None

        return json_output

    def get_value(self, response, key):
        # Ritorna il valore specificato dal JSON di risposta, se esiste
        return response.get(key, "Key not found")

    def combined_chains(self, message, role):
        # Aggiunge un messaggio alla conversazione persistente
        self.conversation.append(
            {
                'role': role,
                'content': message
            }
        )

    def conversations(self, message):
        # Aggiungi il messaggio dell'utente alla conversazione
        self.combined_chains(message, "user")

        # Debug per tracciare il contesto passato al modello
        print("Contesto della conversazione prima della chiamata:", self.conversation)

        # Chiamata al modello con la conversazione completa come contesto
        res = ollama.chat(
            model="llama2",
            messages=self.conversation
        )

        # Aggiungi la risposta dell'assistente alla conversazione
        self.combined_chains(res['message']['content'], "assistant")

        # Stampa la risposta dell'assistente
        print(res['message']['content'])

    def get_conversation(self):
        # Ritorna la conversazione completa come lista
        return self.conversation