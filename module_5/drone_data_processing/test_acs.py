import smbus2
import time
from pymavlink import mavutil

# Адрес I2C-акселерометра
I2C_ADDR = 0x1E

# Инициализация шины I2C
bus = smbus2.SMBus(1)

# Чтение данных с акселерометра
def read_accel():
  # Чтение данных с регистров акселерометра
  x_accel = bus.read_byte_data(I2C_ADDR, 0x01)
  y_accel = bus.read_byte_data(I2C_ADDR, 0x03)
  z_accel = bus.read_byte_data(I2C_ADDR, 0x05)

  # Преобразование данных в g (гравитационные ускорения)
  x_accel = x_accel * 0.0078 # 1 LSB = 0.0078 g
  y_accel = y_accel * 0.0078
  z_accel = z_accel * 0.0078

  return x_accel, y_accel, z_accel

# Создание объекта pymavlink
pymavlink_connection = mavutil.mavlink_connection(
  "udpin:localhost:14550",
  source_system=255,
  source_component=1
)

while True:
  # Чтение данных с акселерометра
  x_accel, y_accel, z_accel = read_accel()

  # Создание сообщения pymavlink для акселерометра
  msg = pymavlink_connection.mav.highres_imu_send(
    int(time.time() * 1e6),  # time_usec
    0, 0, 0,  # гироскопические данные не используются
    x_accel,
    y_accel,
    z_accel,
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

