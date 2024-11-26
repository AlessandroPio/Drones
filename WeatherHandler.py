from os import chdir, path
from os.path import isfile
from Config import Log, Config
from Model import Model
from PrologPY import PrologPY
from sys import argv
chdir(path.dirname(__file__))

model = Model(verbose=True)
log = Log()
prolog = PrologPY(log)
conf = Config()
input_ = argv[1]
path = "./DALI/Examples/basic/richiesta_img_" + argv[2] + ".txt"

def image_analysis_mode():
    img_name = "c.jpeg"

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

if input_ == 'vai':
    res = image_analysis_mode().strip("\"")
    # res = "weather_conditions(rainy)."
    with open(path, 'w') as file:
        file.write(":- dynamic weather_conditions/1.\n")
        file.write(f"{res}\n")
    print(f"File aggiornato con {res}")

exit(0)
