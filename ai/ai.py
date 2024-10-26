import random
import json
import pickle
import numpy as np

import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM, Embedding
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.regularizers import l2
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

from sklearn.model_selection import train_test_split

import tensorflow as tf
import matplotlib.pyplot as plt

import os

# Загрузка необходимых ресурсов NLTK
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

# Инициализация лемматизатора и стоп-слов
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('russian'))

# -------------- Предобработка и Подготовка Данных --------------

# Проверка наличия файла 'intents.json'
if not os.path.exists('intents.json'):
    raise FileNotFoundError("Файл 'intents.json' не найден в текущей директории.")

# Загрузка данных из intents.json
with open('intents.json', 'r', encoding='utf-8') as json_file:
    intents = json.load(json_file)

# Проверка содержимого intents
print(json.dumps(intents, indent=4, ensure_ascii=False))

# Инициализация списков
words = []
classes = []
documents = []
ignore_letters = ['?', '!', '.', ',']

# Обработка данных из intents
for intent in intents['intents']:
    for pattern in intent['patterns']:
        word_list = nltk.word_tokenize(pattern, language='russian')  # Добавлен параметр language='russian'
        words.extend(word_list)
        documents.append((word_list, intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

# Лемматизация и удаление дубликатов, стоп-слов
words = [lemmatizer.lemmatize(word.lower()) 
         for word in words 
         if word not in ignore_letters and word.lower() not in stop_words]
words = sorted(set(words))

classes = sorted(set(classes))

# Сохранение словаря слов и классов
pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(classes, open('classes.pkl', 'wb'))

# Создание обучающего набора данных
training = []
output_empty = [0] * len(classes)

for document in documents:
    bag = []
    word_patterns = document[0]
    word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]
    for word in words:
        bag.append(1) if word in word_patterns else bag.append(0)

    output_row = list(output_empty)
    output_row[classes.index(document[1])] = 1
    training.append([bag, output_row])

# Перемешивание данных
random.shuffle(training)

# Проверка длины bag и output_row
for idx, pair in enumerate(training):
    bag, output_row = pair
    if len(bag) != len(words):
        print(f"Ошибка в bag на позиции {idx}: длина {len(bag)} не равна {len(words)}")
    if len(output_row) != len(classes):
        print(f"Ошибка в output_row на позиции {idx}: длина {len(output_row)} не равна {len(classes)}")

# Разделение на признаки и метки
train_x = []
train_y = []

for pair in training:
    train_x.append(pair[0])
    train_y.append(pair[1])

train_x = np.array(train_x)
train_y = np.array(train_y)

# Проверка формы данных
print(f"train_x shape: {train_x.shape}")
print(f"train_y shape: {train_y.shape}")

# -------------- Построение и Обучение Модели --------------

#Создание модели нейронной сети с использованием Embedding и LSTM
# model = Sequential()
# model.add(Embedding(input_dim=len(words), output_dim=128, input_length=len(train_x[0]))) ХУЕТА ПОЛНАЯ ХЗ ПОЧ
# model.add(LSTM(128, return_sequences=True))
# model.add(Dropout(0.5))
# model.add(LSTM(64))
# model.add(Dropout(0.5))
# model.add(Dense(len(train_y[0]), activation='softmax'))


model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]), ), activation='relu',
                kernel_regularizer=l2(1e-6)))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu', kernel_regularizer=l2(1e-6)))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))





# Создание оптимизатора SGD
sgd = SGD(
    learning_rate=0.01,
    momentum=0.9,
    nesterov=True,
    name='SGD'
)

# Проверка версии TensorFlow для поддержки jit_compile
print(f"TensorFlow version: {tf.__version__}")

# Компиляция модели
if tf.__version__ >= '2.12':
    # Компиляция с jit_compile
    model.compile(
        loss='categorical_crossentropy',
        optimizer=sgd,
        metrics=['accuracy'],
        jit_compile=True
    )
else:
    # Компиляция без jit_compile
    model.compile(
        loss='categorical_crossentropy',
        optimizer=sgd,
        metrics=['accuracy']
    )

# Определение колбеков
early_stop = EarlyStopping(
    monitor='val_loss',
    patience=10,
    restore_best_weights=True
)
# Используйте расширение .keras или укажите save_format='h5'
checkpoint = ModelCheckpoint(
    'best_chatbot_model.keras', 
    monitor='val_loss', 
    save_best_only=True
)
# Если хотите сохранить в формате .h5
# checkpoint = ModelCheckpoint(
#     'best_chatbot_model.h5', 
#     monitor='val_loss', 
#     save_best_only=True, 
#     save_format='h5'
# )

# Обучение модели с использованием колбеков
# hist = model.fit(
#     train_x, train_y,
#     epochs=200,
#     batch_size=5,
#     verbose=1,
#     validation_data=(test_x, test_y),
#     callbacks=[early_stop, checkpoint]
# )
hist = model.fit(train_x, train_y, epochs=200, batch_size=5, verbose=1)

early_stop = EarlyStopping(
    monitor='val_loss',
    patience=20,  # Увеличено с 10 до 20
    restore_best_weights=True
)
# Сохранение модели
model.save('chatbot_model.h5')  # Можно также сохранить в формате .keras
print('Модель успешно обучена и сохранена как \'chatbot_model.h5\'')

# Визуализация истории обучения
plt.figure(figsize=(12, 4))

# Визуализация потерь
plt.subplot(1, 2, 1)
plt.plot(hist.history['loss'], label='train_loss')
plt.plot(hist.history['val_loss'], label='val_loss')
plt.title('Потери во время обучения')
plt.xlabel('Эпоха')
plt.ylabel('Потеря')
plt.legend()

# Визуализация точности
plt.subplot(1, 2, 2)
plt.plot(hist.history['accuracy'], label='train_accuracy')
plt.plot(hist.history['val_accuracy'], label='val_accuracy')
plt.title('Точность во время обучения')
plt.xlabel('Эпоха')
plt.ylabel('Точность')
plt.legend()

plt.show()
