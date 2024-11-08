import smbus2
import time
from pymavlink import mavutil

# Адрес I2C-гироскопа
I2C_ADDR = 0x68

# Инициализация шины I2C
bus = smbus2.SMBus(1)

# Чтение данных с гироскопа
def read_gyro():
  # Чтение данных с регистров гироскопа
  x_gyro = bus.read_byte_data(I2C_ADDR, 0x00)
  y_gyro = bus.read_byte_data(I2C_ADDR, 0x02)
  z_gyro = bus.read_byte_data(I2C_ADDR, 0x04)

  # Преобразование данных в градусы в секунду
  x_gyro = x_gyro * 0.0175 # 1 LSB = 0.0175 град/сек
  y_gyro = y_gyro * 0.0175
  z_gyro = z_gyro * 0.0175

  return x_gyro, y_gyro, z_gyro

# Создание объекта pymavlink
pymavlink_connection = mavutil.mavlink_connection(
  "udpin:localhost:14550",
  source_system=255,
  source_component=1
)

while True:
  # Чтение данных с гироскопа
  x_gyro, y_gyro, z_gyro = read_gyro()

  # Создание сообщения pymavlink для гироскопа
  msg = pymavlink_connection.mav.highres_imu_send(
    int(time.time() * 1e6),  # time_usec
    x_gyro,  # xgyro
    y_gyro,  # ygyro
    z_gyro,  # zgyro
    0, 0, 0,  # акселерометрные данные не используются
    0, 0, 0,  # магнетометр не используется
    0,  # атмосферное давление не используется
    0,  # высота не используется
    0,  # температура не используется
    0   # Маска поля, показывающая, какие другие поля действительны
  )

  # Отправка сообщения pymavlink
  pymavlink_connection.send(msg)

  # Задержка
  time.sleep(0.01)

