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
        p_term= self.kp * error
        # Интегральный компонент
        self.integral_error += error
        i_term= self.ki * self.integral_error
        # Дифференциальный компонент
        d_term= self.kd * (error - self.last_error)
        self.last_error = error
        # Выходной сигнал
        output = p_term + i_term +d_term
        return output


controller = PIDController (kp=0.7, ki=0.15, kd=0.03) # Mожно задать свои значения
setpoint = 20 # Можно задать свой "Заданный угол" тангажа
current_value = 12 # Можно задать свой "Текущий угол" тангажа
output_signal = controller.update (setpoint, current_value)
print (f"Bыxодной сигнал: {output_signal}")
