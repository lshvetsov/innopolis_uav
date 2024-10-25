import smbus2
import time
import mavlink

# Адрес I2C-барометра
I2C_ADDR = 0x76

# Инициализация шины I2C
bus = smbus2.SMBus(1)

# Чтение данных с барометра
def read_pressure():
    # Чтение данных с регистров барометра
    pressure_data = bus.read_i2c_block_data(I2C_ADDR, 0xF4, 3)
    pressure = (pressure_data[0] << 16) | (pressure_data[1] << 8) | pressure_data[2]

    # Преобразование данных в гектопаскали (hPa)
    pressure = pressure * 0.01  

    return pressure

# Создание объекта mavlink
mavlink_connection = mavlink.MAVLink(file_descriptor=0, srcSystem=255, srcComponent=1)

while True:
    # Чтение данных с барометра
    pressure = read_pressure()

    # Создание сообщения MAVLink для барометра
    msg = mavlink.MAVLink_sensor_baro_t(
        time_usec=int(time.time() * 1e6),
        baro=pressure
    )

    # Отправка сообщения MAVLink
    mavlink_connection.send(msg)

    # Задержка
    time.sleep(0.1)


