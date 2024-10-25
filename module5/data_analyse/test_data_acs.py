import numpy as np


# Предположим, что у нас есть данные с акселерометра:
# - accel_data: Список значений ускорения по осям X, Y, Z (g)

def data_acs(accel_data):
    """
  Обработка данных с акселерометра.

  Args:
    accel_data: Список значений ускорения по осям X, Y, Z (g).

  Returns:
    Словарь с обработанными данными:
      - acceleration: Список значений ускорения (g).
      - inclination: Список углов наклона по осям X, Y (град).
  """

    # 1. Фильтрация данных (пример простой фильтрации среднего значения)
    acceleration_x = np.mean(accel_data[0])
    acceleration_y = np.mean(accel_data[1])
    acceleration_z = np.mean(accel_data[2])

    # 2. Расчет углов наклона (упрощенная формула)
    inclination_x = np.arctan(acceleration_x / np.sqrt(acceleration_y ** 2 + acceleration_z ** 2)) * 180 / np.pi
    inclination_y = np.arctan(acceleration_y / np.sqrt(acceleration_x ** 2 + acceleration_z ** 2)) * 180 / np.pi

    # Возвращение обработанных данных
    return {
        "acceleration": [acceleration_x, acceleration_y, acceleration_z],
        "inclination": [inclination_x, inclination_y]
    }


# Пример использования
accel_data = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]  # Данные с акселерометра

data_acs_obj = data_acs(accel_data)

print("Обработанные данные:")
print(f"Ускорение: {data_acs_obj['acceleration']}")
print(f"Углы наклона: {data_acs_obj['inclination']}")
