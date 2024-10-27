from fuzzywuzzy import fuzz
from pathlib import Path
import json

from keras.src.utils.io_utils import print_msg

import app.ml.module.config as config
import random

BASE_DIR = Path(__file__).resolve().parent


#
# with open(str(BASE_DIR / 'intents.json'), 'r', encoding='utf-8') as file:
#         data = json.load(file)
#
# # print(data)
# a = set()
# all_keys = []
# for intent in data['intents']:
#         a = {(intent['tag']): (intent['patterns'])}
#         for sub_intent in intent['sub_intents']:
#             b = {(sub_intent['tag']): (sub_intent['patterns'])}
#         all_keys.append((a,b))
# print(all_keys)




def getUserMessage(text: str):
    cmd = recognize_cmd(filter_cmd(text), 1)
    if cmd['cmd'] not in config.VA_CMD_DICT.keys():
        response = ("Что?")
    else:
        response = (execute_cmd(cmd['cmd']))
    return response


def filter_cmd(raw_voice: str):  # Убирает служебные слова
    cmd = raw_voice
    for x in config.VA_ALIAS:
        cmd = cmd.replace(x, "").strip()

    for x in config.VA_TBR:
        cmd = cmd.replace(x, "").strip()

    return cmd


def recognize_cmd(cmd: str, quantity):  # Sravnivaet slova
    rc = {'cmd': '', 'percent': 0}
    if quantity == 1:
        for c, v in config.VA_CMD_DICT.items():

            for x in v:
                vrt = fuzz.token_sort_ratio(cmd, x)
                if vrt > rc['percent'] and vrt >= 60:
                    rc['cmd'] = c
                    rc['percent'] = vrt

        return rc
    else:
        cmd = cmd.lower()
        result = []
        key_words = []
        for x, y in config.VA_CMD_DICT.items():
            for i in y:
                if (i[:len(cmd)]) == cmd:
                    new_value = i.title().replace(' ', '_')
                    result.append(f"<li onclick=selectInput({[new_value]})>{i.title()}</li>")
                    key_words.append(y)
        return result, key_words


def execute_cmd(cmd: str):  # Ответ
    if cmd == 'help':
        return "Я умею: произносить время, рассказывать анекдоты"
    elif cmd == 'ctime':
        now = 'datetime.datetime.now()'
        if len(str(now.minute)) == 1:
            minute = '0' + str(now.minute)
        else:
            minute = now.minute
        return f"Сейчас {now.hour}:{minute}"
    elif cmd == 'joke':
        return random.choice(config.VA_CMD_RESP['joke'])
    elif cmd in ('right now', 'schedule tomorrow', 'schedule all', 'schedule today'):
        return 'get_lessons(cmd)'
    else:
        return config.VA_CMD_RESP[cmd]



def results_box(text):
    if len(text) >= 2:
        text_to_display, key_words = recognize_cmd(filter_cmd(text), 3)
        try:
            if len(text_to_display) <= 3:
                return text_to_display
        except:
            pass


