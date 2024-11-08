import time
import pandas as pd
from tabulate import tabulate


class SensorData:

    def init(self):
        self.ax = 0.0  # Данные акселерометра
        self.ay = 0.0  # Данные акселерометра
        self.az = 0.0  # Данные акселерометра
        self.gx = 0.0  # Данные гироскопа
        self.gy = 0.0  # Данные гироскопа
        self.gz = 0.0  # Данные гироскопа
        self.altitude = 0.0  # Высота от барометра
        self.latitude = 0.0  # Данные GPS
        self.longitude = 0.0  # Данные GPS
        self.magX = 0.0  # Данные магнитометра
        self.magY = 0.0  # Данные магнитометра
        self.magZ = 0.0  # Данные магнитометра
        self.laserDistance = 0.0  # Расстояние от лазерного дальномера
        self.lidarDistance = 0.0  # Расстояние от LiDAR

    def to_dict(self): return {
        'ax': self.ax,
        'ay': self.ay,
        'az': self.az,
        'gx': self.gx,
        'gy': self.gy,
        'gz': self.gz,
        'altitude': self.altitude,
        'latitude': self.latitude, 'longitude': self.longitude, 'magX': self.magX, 'magY': self.magY, 'magZ': self.magZ,
        'laserDistance': self.laserDistance, 'lidarDistance': self.lidarDistance
    }


class Protocol:
    def initialize(self):
        pass

    def read_data(self):
        pass


class UART(Protocol):
    def initialize(self):
        print("Инициализация UART")

    def read_data(self):
        print("Чтение данных через UART")
        return (1.1, 1.2, 1.3)


class I2C(Protocol):
    def initialize(self):
        print("Инициализация I2C")

    def read_data(self):
        print("Чтение данных через I2C")
        return (2.1, 2.2, 2.3)


class SPI(Protocol):
    def initialize(self):
        print("Инициализация SPI")

    def read_data(self):
        print("Чтение данных через SPI")
        return (3.1, 3.2, 3.3)


class Sensor:
    def __init__(self, protocol: Protocol):
        self.protocol = protocol
        self.protocol.initialize()

    def read_data(self):
        return self.protocol.read_data()


class AccelerometerGyroscope(Sensor):
    def read_data(self):
        print("Чтение данных с акселерометра и гироскопа")
        return (1.0, 1.0, 1.0, 0.1, 0.1, 0.1)


class Barometer(Sensor):
    def read_data(self):
        print("Чтение данных с барометра")
        return 100.0  # Высота может выбираться в зависимости от сценария


class GPSModule(Sensor):
    def read_data(self):
        print("Чтение данных с GPS")
        return (45.0, 30.0)  # Координаты могут выбираться по сценарию


class Magnetometer(Sensor):
    def read_data(self):
        print("Чтение данных с магнитометра")
        return (0.1, 0.2, 0.3)


class DistanceSensor(Sensor):
    def get_distance(self):
        raise NotImplementedError("Must override get_distance")


class LaserRangeFinder(DistanceSensor):
    def read_data(self):
        print("Чтение данных с лазерного дальномера")

    def get_distance(self):
        return 10.0  # Расстояние может выбираться по сценарию


class LiDAR(DistanceSensor):
    def read_data(self):
        print("Чтение данных с LiDAR")

    def get_distance(self):
        return 15.0  # Расстояние может выбираться по сценарию


class DroneSystem:  # Здесь можно указать протоколы по сценарию.
    def __init__(self):
        self.sensor_data = SensorData()
        # Инициализация сенсоров с выбором протокола
        self.accelerometer = AccelerometerGyroscope(UART())
        self.barometer = Barometer(UART())
        self.gps = GPSModule(I2C())
        self.magnetometer = Magnetometer(SPI())
        self.laser_range_finder = LaserRangeFinder(UART())
        self.lidar = LiDAR(I2C())

    def loop(self):
        # Чтение данных с сенсоров
        ax, ay, az, gx, gy, gz = self.accelerometer.read_data()
        self.sensor_data.ax = ax
        self.sensor_data.ay = ay
        self.sensor_data.az = az
        self.sensor_data.gx = gx
        self.sensor_data.gy = gy
        self.sensor_data.gz = gz

        self.sensor_data.altitude = self.barometer.read_data()
        self.sensor_data.latitude, self.sensor_data.longitude = self.gps.read_data()
        self.sensor_data.magX, self.sensor_data.magY, self.sensor_data.magZ = self.magnetometer.read_data()
        self.laser_range_finder.read_data()
        self.sensor_data.laserDistance = self.laser_range_finder.get_distance()

        self.lidar.read_data()
        self.sensor_data.lidarDistance = self.lidar.get_distance()

        # Отображение данных в таблице
        self.display_data()
        time.sleep(2)  # Задержка между итерациями

    def display_data(self):
        data_dict = self.sensor_data.to_dict()
        df = pd.DataFrame([data_dict])
        print(tabulate(df, headers='keys', tablefmt='pretty'))


if __name__ == "__main__":
    drone_system = DroneSystem()
    # Запускаем цикл тестирования на 3 итерации
    for _ in range(3):
        drone_system.loop()
