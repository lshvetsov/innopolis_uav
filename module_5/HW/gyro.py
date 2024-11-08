import numpy as np
import matplotlib.pyplot as plt
from kalman import predict, update

# Функция для обработки данных с гироскопа
def data_giro(gyro_data, dt=0.01):
    angles = {"angle_x": [],
              "angle_y": [],
              "angle_z": []
              }
    # Начальные углы
    angle_x = 0
    angle_y = 0
    angle_z = 0
    # Интегрирование угловой скорости по всем пробам
    for i in range(len(gyro_data[0])):
        angle_x += gyro_data[0][i] * dt
        angle_y += gyro_data[1][i] * dt
        angle_z += gyro_data[2][i] * dt
        angles["angle_x"].append(angle_x)
        angles["angle_y"].append(angle_y)
        angles["angle_z"].append(angle_z)

    return angles


# Генерация тестовых проб данных с гироскопа
def generate_test_data(num_samples=100):
    # Генерация случайных данных угловой скорости
    gyro_data = [
        np.random.uniform(-10, 10, num_samples),  # Случайные значения по оси X
        np.random.uniform(-10, 10, num_samples),  # Случайные значения по оси Y
        np.random.uniform(-10, 10, num_samples)  # Случайные значения по оси Z
    ]
    return gyro_data


# Создание 3D графика
def plot_3d_data(angles):
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(angles['angle_x'], angles['angle_y'], angles['angle_z'], marker='o')
    ax.set_xlabel('Угол X (град)')
    ax.set_ylabel('Угол Y (град)')
    ax.set_zlabel('Угол Z (град)')
    ax.set_title('3D Visualization')
    plt.show()

# Приминение фильтра Калмана
def apply_kalman(angles):
    # Параметры фильтра Калмана
    dt = 0.01
    # Матрицы процессного шума (Q) и шума измерений (R)
    Q = np.array([[1, 0], [0, 1]]) * 0.001
    R = np.array([[0.1]])
    # Начальное состояние (угловая скорость и угловое положение)
    x_x = np.zeros((2, 1))
    x_y = np.zeros((2, 1))
    x_z = np.zeros((2, 1))
    # Ошибка ковариации
    P_x = np.eye(2)
    P_y = np.eye(2)
    P_z = np.eye(2)

    # Инициализация списков для хранения значений
    filtered_angles_x = []
    filtered_angles_y = []
    filtered_angles_z = []

    # Применение фильтра Калмана для каждой оси
    n_samples = len(angles['angle_x'])

    for i in range(n_samples):  # Обработка оси X
        z_x = np.array([[angles['angle_x'][i]]])
        x_x, P_x = predict(x_x, P_x, dt, Q)
        x_x, P_x = update(x_x, P_x, z_x, R)
        filtered_angles_x.append(x_x[0, 0])
        # Обработка оси Y
        z_y = np.array([[angles['angle_y'][i]]])
        x_y, P_y = predict(x_y, P_y, dt, Q)
        x_y, P_y = update(x_y, P_y, z_y, R)
        filtered_angles_y.append(x_y[0, 0])
        # Обработка оси Z
        z_z = np.array([[angles['angle_z'][i]]])
        x_z, P_z = predict(x_z, P_z, dt, Q)
        x_z, P_z = update(x_z, P_z, z_z, R)
        filtered_angles_z.append(x_z[0, 0])

    return {"angle_x": filtered_angles_x, "angle_y": filtered_angles_y, "angle_z": filtered_angles_z }


# Визуализация работы фильтра Калмана
def plot_kalman(angles, filtered_angles):
    plt.figure(figsize=(10, 6))
    # Угол по оси X
    plt.subplot(3, 1, 1)
    plt.plot(angles['angle_x'], color='red', label='Угол по оси X (без фильтра)')
    plt.plot(filtered_angles['angle_x'], color='blue', label='Угол по оси X (фильтр Калмана)')
    plt.ylabel('Угол X (рад)')
    plt.title('Фильтр Калмана для оси X')
    plt.legend()
    plt.grid(True)
    # Угол по оси Y
    plt.subplot(3, 1, 2)
    plt.plot(angles['angle_y'], color='red', label='Угол по оси Y (без фильтра)')
    plt.plot(filtered_angles['angle_y'], color='blue', label='Угол по оси Y (фильтр Калмана)')
    plt.ylabel('Угол Y (рад)')
    plt.title('Фильтр Калмана для оси Y')
    plt.legend()
    plt.grid(True)
    # Угол по оси Z
    plt.subplot(3, 1, 3)
    plt.plot(angles['angle_z'], color='red', label='Угол по оси Z (без фильтра)')
    plt.plot(filtered_angles['angle_z'], color='blue', label='Угол по оси Z (фильтр Калмана)')
    plt.ylabel('Угол Z (рад)')
    plt.title('Фильтр Калмана для оси Z')
    plt.legend()
    plt.grid(True)

    plt.xlabel('Время (пробы)')
    plt.tight_layout()
    plt.show()

# Пример реализации

num_samples = 20
gyro_data = generate_test_data(num_samples)  # Генерация тестовых данных
angles = data_giro(gyro_data)
# Обработка данных
print("Обработанные данные:")
print(f"Углы поворота по оси X: {angles['angle_x']}")
print(f"Углы поворота по оси Y: {angles['angle_y']}")
print(f"Углы поворота по оси Z: {angles['angle_z']}")
plot_3d_data(angles)

# Приминение фильтра Калмана

filtered_angles = apply_kalman(angles)
plot_kalman(angles, filtered_angles)
