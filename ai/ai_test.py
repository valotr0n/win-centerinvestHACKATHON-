# test_chatbot.py
import json

import nltk
import numpy as np
import pickle
from tensorflow.keras.models import load_model
from nltk.stem import SnowballStemmer

# Загрузка необходимых ресурсов NLTK
nltk.download('punkt')

# Инициализация стеммера
stemmer = SnowballStemmer("russian")

# Загрузка модели и данных
model = load_model('chatbot_model.h5')

with open('words.pkl', 'rb') as f:
    words = pickle.load(f)

with open('labels.pkl', 'rb') as f:
    labels = pickle.load(f)

with open('intents.json', 'r', encoding='utf-8') as file:
    data = json.load(file)


def preprocess_sentence(sentence):
    # Токенизация и стемминг
    sentence_words = nltk.word_tokenize(sentence.lower())
    sentence_words = [stemmer.stem(word) for word in sentence_words if word.isalnum()]

    # Создание мешка слов
    bag = [0] * len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
    return np.array(bag)


def get_response(prediction, intents_json):
    # Получение индекса с наибольшей вероятностью
    index = np.argmax(prediction)
    tag = labels[index]

    # Поиск ответа в JSON
    for intent in intents_json['intents']:
        if intent['tag'] == tag:
            return np.random.choice(intent['responses'])
        if 'sub_intents' in intent:
            for sub_intent in intent['sub_intents']:
                if sub_intent['tag'] == tag:
                    return np.random.choice(sub_intent['responses'])
    return "Извините, я не понимаю ваш запрос."


def chat():
    print("Начните общение с ботом (напишите 'выход' для завершения)")
    while True:
        message = input("Вы: ")
        if message.lower() == "выход":
            print("Бот: До свидания!")
            break

        bag = preprocess_sentence(message)
        bag = np.expand_dims(bag, axis=0)

        # Предсказание
        prediction = model.predict(bag)[0]
        response = get_response(prediction, data)

        print(f"Бот: {response}")


if __name__ == "__main__":
    chat()
