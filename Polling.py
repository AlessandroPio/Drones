from os.path import isfile, exists
from time import sleep
from hashlib import md5
from Config import Log, Config
from Model import Model
from PrologPY import PrologPY

model = Model(verbose=True)
log = Log()
prolog = PrologPY(log)
conf = Config()

def calculate_file_hash(file_path):
    with open(file_path, 'rb') as file:
        content = file.read()
    return md5(content).hexdigest()


def read_weather_condition(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            if "weather_conditions" in line:
                start = line.find('(') + 1
                end = line.find(')')
                if start != -1 and end != -1:
                    return line[start:end].strip('"')
    return None


def remove_quotes_in_conditions(file_path):
    updated_lines = []
    with open(file_path, 'r') as file:
        for line in file:
            if "weather_conditions" in line:
                start = line.find('(') + 1
                end = line.find(')')
                if start != -1 and end != -1:
                    condition = line[start:end].strip('"')
                    line = f"weather_conditions({condition}).\n"
            updated_lines.append(line)

    with open(file_path, 'w') as file:
        file.writelines(updated_lines)


def image_analysis_mode():
    img_name = "c.jpeg"
    if img_name == "0":
        return

    img_path = './images/' + img_name
    if not isfile(img_path):
        print(log.fail("Immagine non trovata!"))
        return

    json_output = model.analyze_images(img_path)
    print(log.header("Formato JSON"))
    print(log.warning(json_output))
    print()
    print(log.header("Prolog"))
    print(log.ok(prolog.json_to_prolog(json_output)))
    print()
    return prolog.json_to_prolog(json_output)


def update_weather_condition(file_path, new_condition):
    with open(file_path, 'w') as file:
        file.write(":- dynamic weather_conditions/1.\n")
        file.write(f"{new_condition}.\n")
    print(f"File aggiornato con {new_condition}")


def monitor_file(file_path):
    if not exists(file_path):
        print(f"Errore: il file '{file_path}' non esiste.")
        return

    print(f"Monitoraggio del file: {file_path}")
    last_hash = calculate_file_hash(file_path)

    while True:
        sleep(1)  # polling ogni secondo
        current_hash = calculate_file_hash(file_path)

        if current_hash != last_hash:
            print(f"Il file {file_path} è stato modificato da un processo esterno.")
            last_hash = current_hash

            remove_quotes_in_conditions(file_path)

            condition = read_weather_condition(file_path)
            print(f"Valore corrente di weather_conditions: {condition}")

            if condition == "required":
                print("Eseguo operazioni per 'required'...")
                res = image_analysis_mode()
                sleep(2)
                print("Operazione completata.")

                update_weather_condition(file_path, res)

            elif condition == "completed":
                print("Nessuna operazione necessaria. Stato già 'completed'.")
