import numpy as np


# Предположим, что у нас есть данные с гироскопа:
# - gyro_data: Список значений угловой скорости по осям X, Y, Z (град/с)

def data_giro(gyro_data, dt=0.01):
    """
  Обработка данных с гироскопа.

  Args:
    gyro_data: Список значений угловой скорости по осям X, Y, Z (град/с).
    dt: Интервал времени между измерениями (с).

  Returns:
    Словарь с обработанными данными:
      - angular_velocity: Список значений угловой скорости (град/с).
      - angle: Список значений углов поворота (град).
  """

    # 1. Фильтрация данных (пример простой фильтрации среднего значения)
    angular_velocity_x = np.mean(gyro_data[0])
    angular_velocity_y = np.mean(gyro_data[1])
    angular_velocity_z = np.mean(gyro_data[2])

    # 2. Расчет углов поворота (интегрирование угловой скорости)
    angle_x = angular_velocity_x * dt
    angle_y = angular_velocity_y * dt
    angle_z = angular_velocity_z * dt

    # Возвращение обработанных данных
    return {
        "angular_velocity": [angular_velocity_x, angular_velocity_y, angular_velocity_z],
        "angle": [angle_x, angle_y, angle_z]
    }


# Пример использования
gyro_data = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]  # Данные с гироскопа

data_giro_obj = data_giro(gyro_data)

print("Обработанные данные:")
print(f"Угловая скорость: {data_giro_obj['angular_velocity']}")
print(f"Углы поворота: {data_giro_obj['angle']}")
