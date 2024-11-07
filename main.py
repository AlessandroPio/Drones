import json
import os

from faiss.contrib.ivf_tools import permute_invlists

from Config import Config
from Model import Model
from Prolog import Prolog

Config()

model = Model()
prolog = Prolog()

"""
json_output = model.analyze_images(os.environ['IMG_PATH'] + "k.jpg", verbose=True)
print("-----")
print(json_output); print()
json_output = json.loads(json_output)
print(json_output)
print("-----")
print()
print(prolog.json_to_prolog(json_output))

"""

while True:
    chat = input("Qualcosa: ")
    if chat.lower() == "n":
        break
    model.conversations(chat)

# Visualizza la conversazione completa alla fine
print("\nConversazione completa:")
for chat in model.get_conversation():
    print(chat)
