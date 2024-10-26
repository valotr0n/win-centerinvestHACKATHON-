import random
import json
import pickle
import numpy as np


import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

from tensorflow.keras.models import load_model

# Загрузка необходимых ресурсов NLTK
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

# Инициализация лемматизатора и стоп-слов
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('russian'))

# Загрузка данных
try:
    with open("words.pkl", "rb") as f:
        words = pickle.load(f)
except FileNotFoundError:
    print("Файл words.pkl не найден. Убедитесь, что он находится в рабочей директории.")
    words = []

try:
    with open("classes.pkl", "rb") as f:
        classes = pickle.load(f)
except FileNotFoundError:
    print("Файл classes.pkl не найден. Убедитесь, что он находится в рабочей директории.")
    classes = []

# Загрузка intents
try:
    with open('intents.json', 'r', encoding='utf-8') as json_file:
        intents = json.load(json_file)
except FileNotFoundError:
    print("Файл intents.json не найден. Убедитесь, что он находится в рабочей директории.")
    intents = {"intents": []}

# Загрузка модели
try:
    model = load_model('chatbot_model.h5')
except FileNotFoundError:
    print("Файл chatbot_model.h5 не найден. Убедитесь, что он находится в рабочей директории.")
    model = None

def clean_up_sentence(sentence):
    """
    Разбивает предложение на слова, лемматизирует их и удаляет стоп-слова.
    """
    sentence_words = nltk.word_tokenize(sentence, language='russian')
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words if word.lower() not in stop_words]
    print(f"Токенизированные и лемматизированные слова: {sentence_words}")  # Отладка
    return sentence_words

def bow(sentence, words, show_details=False):
    """
    Преобразует предложение в мешок слов (bag of words).
    """
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
                if show_details:
                    print(f"Найдено в мешке: {w}")
    print(f"Мешок слов: {bag}")  # Отладка
    return np.array(bag)

def predict_class(sentence, model, words, classes):
    """
    Предсказывает класс (интент) для заданного предложения.
    """
    if model is None:
        print("Модель не загружена.")
        return []
    
    bow_vector = bow(sentence, words, show_details=True)
    res = model.predict(np.array([bow_vector]))[0]
    print(f"Предсказанные вероятности: {res}")  # Отладка
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": float(r[1])})
    print(f"Отфильтрованные и отсортированные результаты: {return_list}")  # Отладка
    return return_list

def get_response(intents_list, intents_json):
    """
    Возвращает ответ на основе предсказанного интента.
    """
    if not intents_list:
        return "Извините, я не понимаю вас."
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            return random.choice(i['responses'])
    return "Извините, я не понимаю вас."

def chatbot_response(user_input):
    """
    Генерирует ответ чат-бота на основе пользовательского ввода.
    """
    print(f"Вход от пользователя: {user_input}")  # Отладка
    ints = predict_class(user_input, model, words, classes)
    print(f"Предсказанные интенты: {ints}")  # Отладка
    res = get_response(ints, intents)
    print(f"Ответ бота: {res}")  # Отладка
    return res

if __name__ == "__main__":
    print("Бот: Привет! Я ваш чат-бот. Если хотите выйти, напишите 'пока', 'до свидания' или 'выход'.")
    while True:
        user_input = input("Вы: ")
        if user_input.lower() in ["пока", "до свидания", "выход"]:
            print("Бот: До свидания!")
            break
        response = chatbot_response(user_input)
        print(f"Бот: {response}")

    # Пример тестирования
    print("\n--- Тестирование с примерами предложений ---\n")
    test_sentences = [
        "Где общага",
        "Где находится общежитие?",
        "Стажировки",
        "Мне нужна помощь с арендой жилья.",
        "Как защитить свой банковский счёт?"
    ]

    for message in test_sentences:
        print(f"Вы: {message}")
        if model is not None:
            ints = predict_class(message, model, words, classes)
            res = get_response(ints, intents)
            print(f"Бот: {res}\n")
        else:
            print("Бот: Модель не загружена, поэтому ответить не могу.\n")
