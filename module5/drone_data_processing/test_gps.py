import serial
import time
import mavlink
import pynmea2

# Параметры порта и скорости передачи данных
PORT = "/dev/ttyAMA0"
BAUDRATE = 9600

# Создание объекта для порта
ser = serial.Serial(PORT, BAUDRATE)

# Создание объекта mavlink
mavlink_connection = mavlink.MAVLink(file_descriptor=0, srcSystem=255, srcComponent=1)

while True:
  # Чтение данных от GPS-модуля
  data = ser.readline().decode('ascii')

  # Парсинг данных с помощью pynmea2
  msg = pynmea2.parse(data)

  # Проверка, что получена корректная информация
  if isinstance(msg, pynmea2.types.GGA):
    # Извлечение координат
    latitude = msg.latitude
    longitude = msg.longitude
    altitude = msg.altitude

    # Преобразование координат в десятичные градусы
    latitude_decimal = latitude[0] + (latitude[1] / 60.0)
    longitude_decimal = longitude[0] + (longitude[1] / 60.0)

    # Создание сообщения MAVLink для GPS
    msg = mavlink.MAVLink_global_position_int_t(
      time_usec=int(time.time() * 1e6),
      lat=int(latitude_decimal * 1e7),
      lon=int(longitude_decimal * 1e7),
      alt=int(altitude * 1000) # Высота в миллиметрах
    )

    # Отправка сообщения MAVLink
    mavlink_connection.send(msg)

  time.sleep(0.1)

