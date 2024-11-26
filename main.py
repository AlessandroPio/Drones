import json
import os

from Config import Log, Config
from Model import Model
from PrologPY import PrologPY
from DroneMissionManager import DroneMissionManager

Config()
model = Model()
log = Log()
prolog = PrologPY(log)

def display_menu():
    print("| -------------------------")
    print("| 1. Avvia l'assistente    |")
    print("| 2. Analizza immagine     |")
    print("| 3. Esci dal programma    |")
    print("| -------------------------\n")

def assistant_mode():
    print(Log.ok("Ciao! Sono BOB, il tuo assistente personale per tracciare le spedizioni dei pacchi."))
    while True:
        id_missione = input("Inserisci l'ID della missione (o digita 0 per tornare al menu): ")
        if id_missione == "0":
            break
        manager = DroneMissionManager(json.loads(os.environ['DATABASE_FILES']))
        info = manager.run(id_missione)  # per ricordarmelo

        if not info:
            print(log.fail("\nID missione non valido. Vuoi riprovare? (y/n)"))
            retry = input("-> ").lower()
            if retry != "y":
                break
        else:
            print(log.header("\nDettagli della missione:"))
            print(log.ok(info))
            while True:
                user_input = input("\nChiedimi qualcosa (digita 0 per uscire): ")
                if user_input == "0":
                    break
                model.conversations(user_input, info)
                info = manager.run(id_missione)

def image_analysis_mode():
    img_name = input("Inserisci il nome dell'immagine da analizzare (o digita 0 per tornare al menu): ")
    if img_name == "0":
        return

    img_path = os.path.join(os.environ.get('IMG_PATH', ''), img_name)
    if not os.path.isfile(img_path):
        print(log.fail("Immagine non trovata!"))
        return

    json_output = model.analyze_images(img_path)
    print(log.header("Formato JSON"))
    print(log.warning(json_output)); print()
    print(log.header("Prolog"))
    print(log.ok(prolog.json_to_prolog(json_output))); print()

def main():
    while True:
        display_menu()
        try:
            user_choice = int(input("Seleziona un'opzione: "))
        except ValueError:
            print(log.fail("La risposta deve essere un numero intero!"))
            continue

        if user_choice == 1:
            assistant_mode()
        elif user_choice == 2:
            image_analysis_mode()
        elif user_choice == 3:
            print(log.header("Arrivederci"))
            break
        else:
            print(log.fail("Opzione non valida. Riprova"))

if __name__ == "__main__":
    main()