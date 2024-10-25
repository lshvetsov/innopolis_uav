import smbus2
import time
import mavlink

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

# Создание объекта mavlink
mavlink_connection = mavlink.MAVLink(file_descriptor=0, srcSystem=255, srcComponent=1)

while True:
  # Чтение данных с гироскопа
  x_gyro, y_gyro, z_gyro = read_gyro()

  # Создание сообщения MAVLink для гироскопа
  msg = mavlink.MAVLink_sensor_gyro_float_t(
    time_usec=int(time.time() * 1e6),
    xgyro=x_gyro,
    ygyro=y_gyro,
    zgyro=z_gyro
  )

  # Отправка сообщения MAVLink
  mavlink_connection.send(msg)

  # Задержка
  time.sleep(0.01)

