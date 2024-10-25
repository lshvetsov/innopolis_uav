import numpy as np

# Предположим, что у нас есть данные с барометра:
# - baro_data: Список значений атмосферного давления (hPa)
# - temp_data: Список значений температуры (градусы Цельсия)

def data_bar(baro_data, temp_data):
  """
  Обработка данных с барометра.

  Args:
    baro_data: Список значений атмосферного давления (hPa).
    temp_data: Список значений температуры (градусы Цельсия).

  Returns:
    Словарь с обработанными данными:
      - pressure: Среднее значение атмосферного давления (hPa).
      - altitude: Высота над уровнем моря (м).
  """

  # 1. Фильтрация данных (пример простой фильтрации среднего значения)
  pressure = np.mean(baro_data)

  # 2. Компенсация температуры (упрощенная формула)
  # (В реальных системах используются более точные формулы)
  temperature = np.mean(temp_data)
  pressure_compensated = pressure * (1 + 0.00367 * temperature / 100) # Коррекция на температуру

  # 3. Преобразование давления в высоту (упрощенная формула)
  # (В реальных системах используются более точные формулы)
  altitude = 44330 * (1 - (pressure_compensated / 1013.25)**0.1903)

  # Возвращение обработанных данных
  return {
    "pressure": pressure_compensated,
    "altitude": altitude
  }

# Пример использования
baro_data = [1000, 1002, 1001] # Данные с барометра (hPa)
temp_data = [20, 22, 21] # Данные с датчика температуры (градусы Цельсия)

data_bar_obj = data_bar(baro_data, temp_data)

print("Обработанные данные:")
print(f"Атмосферное давление: {data_bar_obj['pressure']:.2f} hPa")
print(f"Высота: {data_bar_obj['altitude']:.2f} м")
