# # test_chatbot.py
# import json
#
# import nltk
# import numpy as np
# import pickle
# from pathlib import Path
#
# from tensorflow.keras.models import load_model
# from nltk.stem import SnowballStemmer
# BASE_DIR = Path(__file__).resolve().parent
#
# # Загрузка необходимых ресурсов NLTK
# nltk.download('punkt')
#
# # Инициализация стеммера
# stemmer = SnowballStemmer("russian")
#
# # Загрузка модели и данных
# try:
#     with open(str(BASE_DIR / 'words.pkl'), 'rb') as file:
#         words = pickle.load(file)
# except FileNotFoundError:
#     print("Файл words.pkl не найден. Убедитесь, что он находится в рабочей директории.")
#     words = []
#
# try:
#     with open(str(BASE_DIR / 'classes.pkl'), 'rb') as file:
#         classes = pickle.load(file)
# except FileNotFoundError:
#     print("Файл classes.pkl не найден. Убедитесь, что он находится в рабочей директории.")
#     classes = []
#
# # Загрузка intents
# try:
#     with open(str(BASE_DIR / 'intents.json'), 'r', encoding='utf-8') as file:
#         data = json.load(file)
# except FileNotFoundError:
#     print("Файл intents.json не найден. Убедитесь, что он находится в рабочей директории.")
#     intents = {"intents": []}
#
# # Загрузка модели
# try:
#     model = load_model(str(BASE_DIR / 'chatbot_model.h5'))
# except FileNotFoundError:
#     print("Файл chatbot_model.h5 не найден. Убедитесь, что он находится в рабочей директории.")
#     model = None
#
# with open(str(BASE_DIR / 'labels.pkl'), 'rb') as f:
#     labels = pickle.load(f)
#
#
# def preprocess_sentence(sentence):
#     # Токенизация и стемминг
#     sentence_words = nltk.word_tokenize(sentence.lower())
#     sentence_words = [stemmer.stem(word) for word in sentence_words if word.isalnum()]
#
#     # Создание мешка слов
#     bag = [0] * len(words)
#     for s in sentence_words:
#         for i, w in enumerate(words):
#             if w == s:
#                 bag[i] = 1
#     return np.array(bag)
#
#
# def get_response(prediction, intents_json):
#     # Получение индекса с наибольшей вероятностью
#     index = np.argmax(prediction)
#     tag = labels[index]
#
#     # Поиск ответа в JSON
#     for intent in intents_json['intents']:
#         if intent['tag'] == tag:
#             return np.random.choice(intent['responses'])
#         if 'sub_intents' in intent:
#             for sub_intent in intent['sub_intents']:
#                 if sub_intent['tag'] == tag:
#                     return np.random.choice(sub_intent['responses'])
#     return "Извините, я не понимаю ваш запрос."
#
#
# async def chat(message):
#     print("Начните общение с ботом (напишите 'выход' для завершения)")
#     while True:
#         if message.lower() == "выход":
#             return "До свидания"
#
#
#         bag = preprocess_sentence(message)
#         bag = np.expand_dims(bag, axis=0)
#
#         # Предсказание
#         prediction = model.predict(bag)[0]
#         response = get_response(prediction, data)
#
#         return response
#
