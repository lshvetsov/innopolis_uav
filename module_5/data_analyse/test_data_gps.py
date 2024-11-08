import time

def data_gps(gps_data):
 """
 Обработка данных с GPS без использования pynmea2.

 Args:
  gps_data: Строка данных в формате NMEA.

 Returns:
  Словарь с обработанными данными:
   - latitude: Широта (градусы).
   - longitude: Долгота (градусы).
   - altitude: Высота (метры).
   - speed: Скорость (м/с).
   - timestamp: Время (секунды с начала эпохи).
 """

 try:
  # Разделение строки NMEA по запятым
  data_parts = gps_data.split(",")

  # Извлечение информации из частей строки
  if data_parts[0] == "$GPGGA": # Обработка данных GGA
   timestamp_str = data_parts[1] + ",2023,04,12" # Добавлена дата (2023-04-12)
   timestamp = time.strptime(timestamp_str, "%H%M%S.%f,%Y,%m,%d") # Указан формат даты
   latitude = float(data_parts[2])
   latitude_direction = data_parts[3]
   longitude = float(data_parts[4])
   longitude_direction = data_parts[5]
   altitude = float(data_parts[9])

   # Преобразование широты и долготы в десятичные градусы
   latitude_decimal = latitude // 100 + (latitude % 100) / 60
   longitude_decimal = longitude // 100 + (longitude % 100) / 60

   # Корректировка знака широты и долготы
   if latitude_direction == "S":
    latitude_decimal *= -1
   if longitude_direction == "W":
    longitude_decimal *= -1

   # Скорость не доступна в GGA
   speed = None 

   # Преобразование времени в секунды с начала эпохи
   timestamp_seconds = time.mktime(timestamp)

   # Возвращение обработанных данных
   return {
    "latitude": latitude_decimal,
    "longitude": longitude_decimal,
    "altitude": altitude,
    "speed": speed,
    "timestamp": timestamp_seconds
   }
  else:
   return None

 except Exception as e:
  print("Ошибка при обработке данных GPS:", e)
  return None

# Пример использования
gps_data = "$GPGGA,082459.468,41.6168,N,41.6363,E,1,08,0.9,12.7,M,33.2,M,,*59"


data_gps_obj = data_gps(gps_data)

if data_gps_obj: # Проверка, что data_gps_obj не None
 print("Обработанные данные:")
 print(f"Широта: {data_gps_obj['latitude']}")
 print(f"Долгота: {data_gps_obj['longitude']}")
 print(f"Высота: {data_gps_obj['altitude']}")
 print(f"Скорость: {data_gps_obj['speed']}")
 print(f"Время: {data_gps_obj['timestamp']}")
else:
 print("Некорректные данные GPS.")

