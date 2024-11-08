import serial
import time
from pymavlink import mavutil
import pynmea2

# Параметры порта и скорости передачи данных
PORT = "/dev/ttyAMA0"
BAUDRATE = 9600

# Создание объекта для порта
ser = serial.Serial(PORT, BAUDRATE)

# Создание объекта pymavlink
pymavlink_connection = pymavlink_connection = mavutil.mavlink_connection(
  "udpin:localhost:14550",
  source_system=255,
  source_component=1
)

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

    # Создание сообщения pymavlink для GPS
    msg = pymavlink_connection.mav.global_position_int_send(
      int(time.time() * 1e6),  # time_usec
      latitude_decimal * 1e7,  # latitude в градусах * 1e7
      longitude_decimal * 1e7,  # longitude в градусах * 1e7
      altitude * 1000,  # altitude в метрах * 1000
      0,  # relative altitude в метрах * 1000
      0, 0, 0,  # скорость не используется
      0  # heading не используется
    )

    # Отправка сообщения pymavlink
    pymavlink_connection.send(msg)

  time.sleep(0.1)

