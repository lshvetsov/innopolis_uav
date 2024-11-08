import numpy as np
import matplotlib.pyplot as plt
from kalman import predict, update


# Функция для генерации случайных данных барометра
def generate_barometer_data(num_samples=15):
    # Генерация случайных значений давления (в гектопаскалях) и высоты (в метрах)
    pressure = np.random.uniform(950, 1050, num_samples)  # Давление
    altitude = np.random.uniform(0, 5000, num_samples)  # Высота
    return pressure, altitude


def plot_3d_data(pressure, altitude):
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(altitude, pressure, zs=0, zdir='z', marker='o', linestyle='-', color='orange')
    ax.set_xlabel('Высота (метры)')
    ax.set_ylabel('Давление (гПа)')
    ax.set_zlabel('Наблюдения')
    ax.set_title('3D Визуализация')
    plt.show()

# Приминение фильтра Калмана
def apply_kalman(baro_data):
    # Параметры фильтра Калмана
    dt = 1.0
    # Матрицы процессного шума (Q) и шума измерений (R)
    Q = np.array([[1, 0], [0, 1]]) * 0.001
    R = np.array([[0.1]])
    # Начальное состояние (угловая скорость и угловое положение)
    x_pres = np.zeros((2, 1))
    x_alt = np.zeros((2, 1))
    # Ошибка ковариации
    P_pres = np.eye(2)
    P_alt = np.eye(2)

    # Инициализация списков для хранения значений
    filtered_pressure = []
    filtered_altitude = []

    # Применение фильтра Калмана для каждой оси
    n_samples = len(baro_data['pressure'])

    for i in range(n_samples):
        # Обработка давления
        z_pres = np.array([[baro_data['pressure'][i]]])
        x_pres, P_pres = predict(x_pres, P_pres, dt, Q)
        x_pres, P_pres = update(x_pres, P_pres, z_pres, R)
        filtered_pressure.append(x_pres[0, 0])
        # Обработка высоты
        z_alt = np.array([[baro_data['altitude'][i]]])
        x_alt, P_alt = predict(x_alt, P_alt, dt, Q)
        x_alt, P_alt = update(x_alt, P_alt, z_alt, R)
        filtered_altitude.append(x_alt[0, 0])

    return {"pressure": filtered_pressure, "altitude": filtered_altitude }


# Визуализация работы фильтра Калмана
def plot_kalman(gps_data, filtered_gps_data):
    plt.figure(figsize=(10, 6))
    # Давление
    plt.subplot(3, 1, 1)
    plt.plot(gps_data['pressure'], color='red', label='Давление (без фильтра)')
    plt.plot(filtered_gps_data['pressure'], color='blue', label='Давление (фильтр Калмана)')
    plt.ylabel('Давление (гПА)')
    plt.title('Фильтр Калмана для Давления')
    plt.legend()
    plt.grid(True)
    # Высота
    plt.subplot(3, 1, 3)
    plt.plot(gps_data['altitude'], color='red', label='Высота (без фильтра)')
    plt.plot(filtered_gps_data['altitude'], color='blue', label='Высота(фильтр Калмана)')
    plt.ylabel('Высота (м)')
    plt.title('Фильтр Калмана для высоты')
    plt.legend()
    plt.grid(True)

    plt.xlabel('Время (пробы)')
    plt.tight_layout()
    plt.show()


# Пример реализации
num_samples = 15
pressure, altitude = generate_barometer_data(num_samples)
print("Сгенерированные данные:")
print(f"Давление: {pressure}")
print(f"Высота: {altitude}")
plot_3d_data(pressure, altitude)

baro_data = {"pressure": pressure, "altitude": altitude}

filtered_baro_data = apply_kalman(baro_data)
plot_kalman(baro_data, filtered_baro_data)
