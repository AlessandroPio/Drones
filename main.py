import os
from random import choice

from Config import Log
from Config import Config
from Model import Model
from Prolog import Prolog

Config()

model = Model()
prolog = Prolog()

while True:

    print("| -------------------------")
    print("| 1 for call the assistant |")
    print("| 2 analyze image          |")
    print("| 3 for exit the program   |")
    print("|--------------------------")
    print()

    while True:
        try:
            choice = int(input("->"))
        except ValueError:
            print(Log.fail("Response must be integer!"))
        finally:
            if type(choice) == int: break


    if choice == 1:
        while True:
            chat = input("Say something: ")
            if chat.lower() == "0":
                break
            model.conversations(chat)

    elif choice == 2:
        img = str(input("Input image -> "))
        json_output = model.analyze_images(os.environ['IMG_PATH'] + img, verbose=True)
        print(Log.header("JSON Format"))
        print(Log.warning(json_output)); print()
        print(Log.header("PROLOG"))
        print(Log.ok(prolog.json_to_prolog(json_output))); print()

    elif choice >= 3:
        break
