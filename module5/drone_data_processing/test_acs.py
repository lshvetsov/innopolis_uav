import smbus2
import time
import mavlink

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

# Создание объекта mavlink
mavlink_connection = mavlink.MAVLink(file_descriptor=0, srcSystem=255, srcComponent=1)

while True:
  # Чтение данных с акселерометра
  x_accel, y_accel, z_accel = read_accel()

  # Создание сообщения MAVLink для акселерометра
  msg = mavlink.MAVLink_sensor_accel_float_t(
    time_usec=int(time.time() * 1e6),
    xacc=x_accel,
    yacc=y_accel,
    zacc=z_accel
  )

  # Отправка сообщения MAVLink
  mavlink_connection.send(msg)

  # Задержка
  time.sleep(0.01)

