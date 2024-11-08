import smbus2
import time
from pymavlink import mavutil

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

# Создание объекта pymavlink
pymavlink_connection = pymavlink_connection = mavutil.mavlink_connection(
    "udpin:localhost:14550",
    source_system=255,
    source_component=1
)

while True:
    # Чтение данных с барометра
    pressure = read_pressure()

    # Создание сообщения pymavlink для барометра
    msg = pymavlink_connection.mav.scaled_pressure_send(
        int(time.time() * 1e3),  # time_boot_ms
        pressure,  # атмосферное давление в гектопаскалях (hPa)
        0,  # давление дифференциальное (не используется)
        0 * 100  # температура в градусах Цельсия * 100
    )

    # Отправка сообщения pymavlink
    pymavlink_connection.send(msg)

    # Задержка
    time.sleep(0.1)


