import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.datasets import cifar10
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Dropout, Conv2D, MaxPooling2D
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing import image
import os

classes = ['самолет', 'автомобиль', 'птица', 'кот', 'олень', 'собака', 'лягушка', 'лошадь', 'корабль', 'грузовик']

batch_size = 128
nb_classes = 10
nb_epoch = 25

(X_train, y_train), (X_test, y_test) = cifar10.load_data()
X_train = X_train.astype('float32') / 255.0
X_test = X_test.astype('float32') / 255.0
Y_train = to_categorical(y_train, nb_classes)
Y_test = to_categorical(y_test, nb_classes)

model = Sequential([
    Conv2D(32, (3, 3), padding='same', activation='relu', input_shape=(32, 32, 3)),
    Conv2D(32, (3, 3), padding='same', activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),
    Dropout(0.25),
    Conv2D(64, (3, 3), padding='same', activation='relu'),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),
    Dropout(0.25),
    Flatten(),
    Dense(512, activation='relu'),
    Dropout(0.5),
    Dense(nb_classes, activation='softmax')
])

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

history = model.fit(X_train, Y_train,
                    batch_size=batch_size,
                    epochs=nb_epoch,
                    validation_split=0.1,
                    shuffle=True,
                    verbose=2)

scores = model.evaluate(X_test, Y_test, verbose=0)
print("Точность на тестовых данных: %.2f%%" % (scores[1] * 100))

plt.plot(history.history['accuracy'], label='Тренировка')
plt.plot(history.history['val_accuracy'], label='Валидация')
plt.xlabel('Эпоха')
plt.ylabel('Точность')
plt.legend()
plt.show()

img_path = 'plane.jpg'
if not os.path.exists(img_path):
    print(f"Файл {img_path} не найден!")
else:
    img = image.load_img(img_path, target_size=(32, 32))
    plt.imshow(img)
    plt.title("Загруженное изображение")
    plt.axis('off')
    plt.show()

    x = image.img_to_array(img) / 255.0
    x = np.expand_dims(x, axis=0)
    prediction = model.predict(x)
    predicted_class = np.argmax(prediction)
    print("Распознанный объект:", classes[predicted_class])
