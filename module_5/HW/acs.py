import numpy as np
import matplotlib.pyplot as plt
from kalman import predict, update


# Функция для обработки данных с акселерометра
def data_accel(accel_data, dt=0.01):
    positions = {"pos_x": [], "pos_y": [], "pos_z": []}
    # Начальные позиции
    pos_x = 0
    pos_y = 0
    pos_z = 0
    # Интегрирование ускорения по всем пробам
    for i in range(len(accel_data[0])):
        pos_x += accel_data[0][i] * dt
        pos_y += accel_data[1][i] * dt
        pos_z += accel_data[2][i] * dt

        positions["pos_x"].append(pos_x)
        positions["pos_y"].append(pos_y)
        positions["pos_z"].append(pos_z)

    return positions


# Генерация случайных тестовых данных с акселерометра
def generate_test_data(num_samples=45):
    # Генерация случайных данных ускорения
    accel_data = [
        np.random.uniform(-10, 10, num_samples),  # Случайные значения по оси X
        np.random.uniform(-10, 10, num_samples),  # Случайные значения по оси Y
        np.random.uniform(-10, 10, num_samples)  # Случайные значения по оси Z
    ]
    return accel_data


def plot_3d_data(positions):
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(positions['pos_x'], positions['pos_y'], positions['pos_z'], marker='o')
    ax.set_xlabel('Позиция X')
    ax.set_ylabel('Позиция Y')
    ax.set_zlabel('Позиция Z')
    ax.set_title('3D Визуализация')
    plt.show()


def apply_kalman(positions):
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
    filtered_positions_x = []
    filtered_positions_y = []
    filtered_positions_z = []

    # Применение фильтра Калмана для каждой оси
    n_samples = len(positions['pos_x'])

    for i in range(n_samples):  # Обработка оси X
        z_x = np.array([[positions['pos_x'][i]]])
        x_x, P_x = predict(x_x, P_x, dt, Q)
        x_x, P_x = update(x_x, P_x, z_x, R)
        filtered_positions_x.append(x_x[0, 0])
        # Обработка оси Y
        z_y = np.array([[positions['pos_y'][i]]])
        x_y, P_y = predict(x_y, P_y, dt, Q)
        x_y, P_y = update(x_y, P_y, z_y, R)
        filtered_positions_y.append(x_y[0, 0])
        # Обработка оси Z
        z_z = np.array([[positions['pos_z'][i]]])
        x_z, P_z = predict(x_z, P_z, dt, Q)
        x_z, P_z = update(x_z, P_z, z_z, R)
        filtered_positions_z.append(x_z[0, 0])

    return {"pos_x": filtered_positions_x, "pos_y": filtered_positions_y, "pos_z": filtered_positions_z}


# Визуализация работы фильтра Калмана
def plot_kalman(positions, filtered_positions):
    plt.figure(figsize=(10, 6))
    # Позиция по оси X
    plt.subplot(3, 1, 1)
    plt.plot(positions['pos_x'], color='red', label='Позиция по оси X (без фильтра)')
    plt.plot(filtered_positions['pos_x'], color='blue', label='Позиция по оси X (фильтр Калмана)')
    plt.ylabel('Позиция X (м)')
    plt.title('Фильтр Калмана для оси X')
    plt.legend()
    plt.grid(True)
    # Позиция по оси Y
    plt.subplot(3, 1, 2)
    plt.plot(positions['pos_y'], color='red', label='Позиция по оси Y (без фильтра)')
    plt.plot(filtered_positions['pos_y'], color='blue', label='Позиция по оси Y (фильтр Калмана)')
    plt.ylabel('Позиция Y (м)')
    plt.title('Фильтр Калмана для оси Y')
    plt.legend()
    plt.grid(True)
    # Позиция по оси Z
    plt.subplot(3, 1, 3)
    plt.plot(positions['pos_z'], color='red', label='Позиция по оси Z (без фильтра)')
    plt.plot(filtered_positions['pos_z'], color='blue', label='Позиция по оси Z (фильтр Калмана)')
    plt.ylabel('Позиция Z (м)')
    plt.title('Фильтр Калмана для оси Z')
    plt.legend()
    plt.grid(True)

    plt.xlabel('Время (пробы)')
    plt.tight_layout()
    plt.show()


# Пример реализации

num_samples = 30

accel_data = generate_test_data(num_samples)
positions = data_accel(accel_data)
print("Обработанные данные:")
print(f"Позиции по оси X: {positions['pos_x']}")
print(f"Позиции по оси Y: {positions['pos_y']}")
print(f"Позиции по оси Z: {positions['pos_z']}")
plot_3d_data(positions)

# Приминение фильтра Калмана

filtered_positions = apply_kalman(positions)
plot_kalman(positions, filtered_positions)
