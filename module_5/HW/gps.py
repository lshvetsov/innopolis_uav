import numpy as np
import matplotlib.pyplot as plt
from kalman import predict, update


# Функция для генерации случайных GPS данных
def generate_gps_data(num_samples=25):
    # Генерация случайных широты, долготы и высоты
    latitudes = np.random.uniform(-90, 90, num_samples)  # Широта
    longitudes = np.random.uniform(-180, 180, num_samples)  # Долгота
    altitudes = np.random.uniform(0, 5000, num_samples)  # Высота в метрах
    return latitudes, longitudes, altitudes


def plot_3d_data(latitudes, longitudes, altitudes):
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(longitudes, latitudes, altitudes, marker='o', linestyle='-', color='orange')
    ax.set_xlabel('Долгота')
    ax.set_ylabel('Широта')
    ax.set_zlabel('Высота (метры)')
    ax.set_title('3D Визуализация')
    plt.show()

# Приминение фильтра Калмана
def apply_kalman(gps_data):
    # Параметры фильтра Калмана
    dt = 1.0
    # Матрицы процессного шума (Q) и шума измерений (R)
    Q = np.array([[1, 0], [0, 1]]) * 0.001
    R = np.array([[0.1]])
    # Начальное состояние (угловая скорость и угловое положение)
    x_lat = np.zeros((2, 1))
    x_lon = np.zeros((2, 1))
    x_alt = np.zeros((2, 1))
    # Ошибка ковариации
    P_lat = np.eye(2)
    P_lon = np.eye(2)
    P_alt = np.eye(2)

    # Инициализация списков для хранения значений
    filtered_latitudes = []
    filtered_longitudes = []
    filtered_altitudes = []

    # Применение фильтра Калмана для каждой оси
    n_samples = len(gps_data['latitudes'])

    for i in range(n_samples):
        # Обработка широты
        z_lat = np.array([[gps_data['latitudes'][i]]])
        x_lat, P_lat = predict(x_lat, P_lat, dt, Q)
        x_lat, P_lat = update(x_lat, P_lat, z_lat, R)
        filtered_latitudes.append(x_lat[0, 0])
        # Обработка долготы
        z_lon = np.array([[gps_data['longitudes'][i]]])
        x_lon, P_lon = predict(x_lon, P_lon, dt, Q)
        x_lon, P_lon = update(x_lon, P_lon, z_lon, R)
        filtered_longitudes.append(x_lon[0, 0])
        # Обработка высоты
        z_alt = np.array([[gps_data['altitudes'][i]]])
        x_alt, P_alt = predict(x_alt, P_alt, dt, Q)
        x_alt, P_alt = update(x_alt, P_alt, z_alt, R)
        filtered_altitudes.append(x_alt[0, 0])

    return {"latitudes": filtered_latitudes, "longitudes": filtered_longitudes, "altitudes": filtered_altitudes }


# Визуализация работы фильтра Калмана
def plot_kalman(gps_data, filtered_gps_data):
    plt.figure(figsize=(10, 6))
    # Широта
    plt.subplot(3, 1, 1)
    plt.plot(gps_data['latitudes'], color='red', label='Широта (без фильтра)')
    plt.plot(filtered_gps_data['latitudes'], color='blue', label='Широта (фильтр Калмана)')
    plt.ylabel('Широта (град)')
    plt.title('Фильтр Калмана для широты')
    plt.legend()
    plt.grid(True)
    # Долгота
    plt.subplot(3, 1, 2)
    plt.plot(gps_data['longitudes'], color='red', label='Долгота (без фильтра)')
    plt.plot(filtered_gps_data['longitudes'], color='blue', label='Долгота (фильтр Калмана)')
    plt.ylabel('Долгота (град)')
    plt.title('Фильтр Калмана долготы')
    plt.legend()
    plt.grid(True)
    # Высота
    plt.subplot(3, 1, 3)
    plt.plot(gps_data['altitudes'], color='red', label='Высота (без фильтра)')
    plt.plot(filtered_gps_data['altitudes'], color='blue', label='Высота(фильтр Калмана)')
    plt.ylabel('Высота (град)')
    plt.title('Фильтр Калмана для высоты')
    plt.legend()
    plt.grid(True)

    plt.xlabel('Время (пробы)')
    plt.tight_layout()
    plt.show()

# Пример реализации
num_samples = 25
latitudes, longitudes, altitudes = generate_gps_data(num_samples)
print("Сгенерированные данные:")
print(f"Широты: {latitudes}")
print(f"Долготы: {longitudes}")
print(f"Высоты: {altitudes}")
plot_3d_data(latitudes, longitudes, altitudes)

# Приминение фильтра Калмана

gps_data = {"latitudes": latitudes, "longitudes": longitudes, "altitudes": altitudes}

filtered_gps_data = apply_kalman(gps_data)
plot_kalman(gps_data, filtered_gps_data)
