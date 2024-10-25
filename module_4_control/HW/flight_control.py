import numpy as np
import matplotlib.pyplot as plt


class PID:
    def __init__(self, kp, ki, kd, dt):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.dt = dt
        self.prev_error = 0
        self.integral = 0

    def update(self, setpoint, measured_value):
        error = setpoint - measured_value  # Значение ошибки
        self.integral += error * self.dt
        derivative = (error - self.prev_error) / self.dt

        output = (self.kp * error) + (self.ki * self.integral) + (self.kd * derivative)  # Выходной сигнал

        self.prev_error = error
        return output


class Drone:
    def __init__(self, mass):
        self.mass = mass
        self.height = 120  # Можно задать свою текущую высоту
        self.velocity = 10  # Можно задать свою текущую скорость по вертикали
        self.gyro_angle = 0  # угол гироскопа, определяющий наклон
        self.thrust = 20  # тяга
        self.gravity = 9.81  # м/с^2, ускорение свободного падения

    def update(self, thrust):
        # Обновление вертикальной скорости
        self.thrust = thrust
        self.velocity += (self.thrust / self.mass - self.gravity) * dt
        self.height += self.velocity * dt

    def set_gyro_angle(self, angle):
        self.gyro_angle = angle


class Sensor:
    def __init__(self):
        self.gps_position = np.array([0.0, 0.0])  # [x, y] self.altimeter = 0.0 # высота
        self.gyroscope = 0.0  # угол наклона

    def update(self, drone):
        # Обновление данных сенсоров на основе состояния БЛА
        self.altimeter = drone.height
        self.gyroscope = drone.gyro_angle


def test_drone_controller(setpoint_height, mass, dt, total_time):
    num_steps = int(total_time / dt)
    drone = Drone(mass)
    pid = PID(kp=1.5, ki=0.1, kd=0.05, dt=dt)
    heights = np.zeros(num_steps)
    thrusts = np.zeros(num_steps)
    for step in range(num_steps):
        thrust = pid.update(setpoint_height, drone.height)
        thrusts[step] = thrust
        drone.update(thrust)
        heights[step] = drone.height
    return heights, thrusts


# test 1

height_pid = PID(kp=1.8, ki=0.15, kd=0.04, dt=0.1)  # PID-регулятор для высоты
course_pid = PID(kp=0.75, ki=0.09, kd=0.06, dt=0.1)  # PID-регулятор для курсового угла
drone = Drone(mass=1.5)  # Можно задать свою массу БЛА в кг
sensor = Sensor()

time_end = 60  # Можно задать своё время моделирования в секундах
dt = 0.15  # Можно задать свой шаг моделирования
num_steps = int(time_end / dt)
heights = np.zeros(num_steps)
altitudes = np.zeros(num_steps)
setpoint_height = 30  # Можно задать свою запрашиваемую высоту в метрах
setpoint_course = 3  # Можно задать свой запрашиваемый угол

for step in range(num_steps):
    sensor.update(drone)
    thrust = height_pid.update(setpoint_height, sensor.altimeter)
    drone.update(thrust)
    heights[step] = drone.height

plt.figure(figsize=(12, 6))
plt.plot(np.arange(num_steps) * dt, heights, label='Высота (м)')
plt.axhline(y=setpoint_height, color='r', linestyle='--', label='Запрашиваемая высота')
plt.title('Тест 1: Управление высотой БЛА с использованием PID-регулятора')
plt.xlabel('Время (с)')
plt.ylabel('Высота (м)')
plt.show()

# test 2

dt = 0.1  # шаг времени
total_time = 50  # общее время теста в секундах
setpoint_height = 10  # запрашиваемая высота в метрах (заданная)
mass = 1.5  # масса БЛА в кг
heights, thrusts = test_drone_controller(setpoint_height, mass, dt, total_time)

plt.figure(figsize=(12, 6))
plt.plot(np.arange(len(heights)) * dt, heights, label='Высота (м)')
plt.axhline(y=setpoint_height, color='r', linestyle='--', label='Запрашиваемая высота')
plt.title('Тест 2: Тестирование управления высотой БЛА')
plt.xlabel('Время (с)')
plt.ylabel('Высота (м)')
plt.legend()
plt.grid()

plt.show()

plt.figure(figsize=(12, 6))
plt.plot(np.arange(len(thrusts)) * dt, thrusts, label='Тяга (Н)', color='orange')
plt.title('Тест2: Используемая тяга БЛА')
plt.xlabel('Время (с)')
plt.ylabel('Тяга (Н)')
plt.legend()
plt.grid()

plt.tight_layout()
plt.show()
