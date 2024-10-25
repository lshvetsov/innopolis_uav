import numpy as np


class PIDController:
    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.last_error = 0
        self.integral_error = 0

    def update(self, setpoint, current_value):
        error = setpoint - current_value

        # Пропорциональный компонент
        p_term = self.kp * error

        # Интегральный компонент
        self.integral_error += error
        i_term = self.ki * self.integral_error

        # Дифференциальный компонент
        d_term = self.kd * (error - self.last_error)
        self.last_error = error

        # Выходной сигнал
        output = p_term + i_term + d_term

        return output


# Пример использования
controller = PIDController(kp=0.5, ki=0.1, kd=0.05)
setpoint = 10  # Заданный угол тангажа
current_value = 5  # Текущий угол тангажа

output_signal = controller.update(setpoint, current_value)

print(f"Выходной сигнал: {output_signal}")
