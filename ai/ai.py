import json
import numpy as np
import random
import nltk
import pickle
from nltk.stem import SnowballStemmer
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import SGD
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

# Загрузка необходимых ресурсов NLTK
nltk.download('punkt')

# Инициализация стеммера
stemmer = SnowballStemmer("russian")

# Загрузка датасета
with open('intents.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Парсинг данных
words = []
labels = []
docs = []
responses = {}
sub_intents = {}

for intent in data['intents']:
    label = intent['tag']
    labels.append(label)
    responses[label] = intent['responses']

    # Обработка основных паттернов
    for pattern in intent['patterns']:
        # Токенизация каждого паттерна
        tokens = nltk.word_tokenize(pattern.lower())
        words.extend(tokens)
        docs.append((tokens, label))

    # Обработка под-интентов
    if 'sub_intents' in intent:
        for sub_intent in intent['sub_intents']:
            sub_label = sub_intent['tag']
            labels.append(sub_label)
            responses[sub_label] = sub_intent['responses']
            for pattern in sub_intent['patterns']:
                tokens = nltk.word_tokenize(pattern.lower())
                words.extend(tokens)
                docs.append((tokens, sub_label))

# Предобработка слов
words = [stemmer.stem(w) for w in words if w.isalnum()]
words = sorted(list(set(words)))

labels = sorted(list(set(labels)))

# Создание обучающих данных
training = []
output_empty = [0] * len(labels)

for doc in docs:
    bag = []
    pattern_words = [stemmer.stem(word) for word in doc[0]]
    for w in words:
        bag.append(1) if w in pattern_words else bag.append(0)

    # Создание метки
    output_row = list(output_empty)
    output_row[labels.index(doc[1])] = 1
    training.append([bag, output_row])

# Перемешивание данных и разделение на X и y
random.shuffle(training)
training = np.array(training, dtype=object)

X = list(training[:, 0])
y = list(training[:, 1])

# Разделение на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Преобразование в numpy массивы
X_train = np.array(X_train)
X_test = np.array(X_test)
y_train = np.array(y_train)
y_test = np.array(y_test)

# Создание модели нейронной сети
model = Sequential()
model.add(Dense(128, input_shape=(len(words),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(labels), activation='softmax'))

# Компиляция модели
sgd = SGD(learning_rate=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

# Обучение модели
model.fit(X_train, y_train, epochs=200, batch_size=5, verbose=1)

# Оценка модели
loss, accuracy = model.evaluate(X_test, y_test)
print(f'Потери: {loss}, Точность: {accuracy}')

# Сохранение модели и данных
model.save('chatbot_model.h5')

with open('words.pkl', 'wb') as f:
    pickle.dump(words, f)

with open('labels.pkl', 'wb') as f:
    pickle.dump(labels, f)

print("Модель и данные успешно сохранены.")
