import random


class DroneSensor:
    def __init__(self):
        self.altitude = 0
        self.temperature = 0
        self.battery_level = 100

    def read_sensors(self):
        self.altitude = random.randint(0, 1000)
        self.temperature = random.randint(-30, 40)
        self.battery_level = random.randint(0, 100)

        data = {
            "altitude": self.altitude,
            "temperature": self.temperature,
            "battery_level": self.battery_level
        }

        self.__show_data()
        return data

    def __show_data(self):
        data = (
            f"Показания датчиков:\n"
            f"Высота: {self.altitude}\n"
            f"Температура: {self.temperature}\n"
            f"Заряд батареи: {self.battery_level}\n\n"
        )
        print(data)


class DroneEngine:
    def __init__(self, number):
        self.number = number
        self.speed = 0
        self.temperature = 0

    def run_engine(self, speed):
        self.speed = speed
        self.temperature = random.randint(30, 40)
        self.__show_data()

    def set_speed(self, speed):
        self.speed = speed

        if speed > self.speed:
            self.temperature += random.randint(1, 5)
        else:
            self.temperature -= random.randint(1, 5)

        self.__show_data()

    def get_speed(self):
        return self.speed

    def __show_data(self):
        print(f"Данные двигателя {self.number}: Скорость вращения - {self.speed} об/мин, Температура двигателя - {self.temperature} °C")


class FlightController:
    def __init__(self):
        self.sensor = DroneSensor()
        self.engines = [DroneEngine(i+1) for i in range(4)]

    def read_sensor_data(self):
        return self.sensor.read_sensors()

    def take_off(self, speed):
        for i, engine in enumerate(self.engines, start=1):
            engine.run_engine(speed)

    def control_speed(self, speed):
        for engine in self.engines:
            engine.set_speed(speed)

    def get_speed(self):
        return tuple(engine.get_speed() for engine in self.engines)
