from fuzzywuzzy import fuzz
from pathlib import Path
import json


BASE_DIR = Path(__file__).resolve().parent



with open(str(BASE_DIR / 'intents.json'), 'r', encoding='utf-8') as file:
        data = json.load(file)

# print(data)
a = set()
all_keys = []
for intent in data['intents']:
        a = {(intent['tag']): (intent['patterns'])}
        for sub_intent in intent['sub_intents']:
            b = {(sub_intent['tag']): (sub_intent['patterns'])}
        all_keys.append((a,b))
print(all_keys)
