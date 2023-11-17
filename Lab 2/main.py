# Local
import cv2
import numpy as np


def bernsen_thresholding(image, e=15, r=15):
    # Копирование изображения для обработки
    processed_image = np.copy(image)

    # Итерация по каждому квадрату
    half_r = r // 2
    for x in range(half_r, image.shape[1] - half_r):
        for y in range(half_r, image.shape[0] - half_r):
            # Получение яркостей пикселей в пределах квадрата
            pixel_values = []
            for i in range(x - half_r, x + half_r + 1):
                for j in range(y - half_r, y + half_r + 1):
                    pixel_values.append(image[j, i])

            # Вычисление наименьшего и наибольшего уровня яркости
            jlow = np.min(pixel_values)
            jhigh = np.max(pixel_values)

            # Вычисление порога
            threshold = (jhigh - jlow) / 2

            # Пороговая обработка пикселя
            if threshold <= e:
                processed_image[y, x] = 0  # Замена пикселя на черный
            else:
                processed_image[y, x] = 255  # Замена пикселя на белый

    return processed_image


def niblack_thresholding(image, r=15, k=-0.2):
    # Копирование изображения для обработки
    processed_image = np.copy(image)

    # Итерация по каждому пикселю
    half_r = r // 2
    for x in range(half_r, image.shape[1] - half_r):
        for y in range(half_r, image.shape[0] - half_r):
            # Получение локальной окрестности
            neighborhood = image[y - half_r:y + half_r + 1, x - half_r:x + half_r + 1]

            # Вычисление среднего и среднеквадратического отклонения
            mean_value = np.mean(neighborhood)
            std_deviation = np.std(neighborhood)

            # Вычисление порога
            threshold = mean_value + k * std_deviation

            # Пороговая обработка пикселя
            if image[y, x] <= threshold:
                processed_image[y, x] = 0  # Замена пикселя на черный
            else:
                processed_image[y, x] = 255  # Замена пикселя на белый

    return processed_image

def gaussian_filter(image):
    # Применение фильтра Гаусса с ядром размера 5х5 со стандартным отклонением 0
    filtered_image = cv2.GaussianBlur(image, (5, 5), 0)

    return filtered_image


# # Загрузка изображения с помощью OpenCV
# image = cv2.imread('img.png', cv2.IMREAD_GRAYSCALE)
#
# # Применение адаптивной пороговой обработки
# processed_image = laplacian_filter(image)
#
# # Сохранение обработанного изображения с помощью OpenCV
# cv2.imwrite('processed_image_laplacian.png', processed_image)
import tkinter as tk
from tkinter import filedialog
import os

def select_input_directory():
    input_directory = filedialog.askdirectory(title="Select Input Directory")
    input_entry.delete(0, tk.END)
    input_entry.insert(0, input_directory)

def select_output_directory():
    output_directory = filedialog.askdirectory(title="Select Output Directory")
    output_entry.delete(0, tk.END)
    output_entry.insert(0, output_directory)

def process_images():
    input_directory = input_entry.get().replace('/', '\\')
    output_directory = output_entry.get().replace('/', '\\')

    methods = [
        bernsen_thresholding,
        niblack_thresholding,
        gaussian_filter
    ]

    for method in methods:
        method_output_directory = os.path.join(output_directory, method.__name__)
        os.makedirs(method_output_directory, exist_ok=True)

        image_files = os.listdir(input_directory)
        for image_file in image_files:
            print(image_file)
            if image_file.endswith('.png') or image_file.endswith('.jpg'):
                image_path = os.path.join(input_directory, image_file)
                print(image_path)
                image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

                # Процесс обработки изображения с использованием выбранного метода
                processed_image = method(image)

                output_image_path = os.path.join(method_output_directory, image_file)
                cv2.imwrite(output_image_path, processed_image)
        print(method.__name__, " Completed\n")

    print("Processing complete!")

# Создание графического интерфейса
root = tk.Tk()

# Кнопка 1 - выбор директории с исходными изображениями в формате PNG
button1 = tk.Button(root, text="Select Input Directory", command=select_input_directory)
button1.pack()

# Поле ввода для отображения выбранной директории
input_entry = tk.Entry(root)
input_entry.pack()

# Кнопка 2 - выбор директории для сохранения обработанных изображений
button2 = tk.Button(root, text="Select Output Directory", command=select_output_directory)
button2.pack()

# Поле ввода для отображения выбранной директории
output_entry = tk.Entry(root)
output_entry.pack()

# Кнопка 3 - обработка изображений
button3 = tk.Button(root, text="Process Images", command=process_images)
button3.pack()

root.mainloop()

