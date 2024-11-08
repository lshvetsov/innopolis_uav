import numpy as np

class KalmanFilter:
    def __init__(self, state_matrix, control_matrix, observation_matrix, process_noise, measurement_noise):
        self.state_matrix = state_matrix
        self.control_matrix = control_matrix
        self.observation_matrix = observation_matrix
        self.process_noise = process_noise
        self.measurement_noise = measurement_noise

        self.state = np.zeros((state_matrix.shape[0], 1))
        self.covariance = np.eye(state_matrix.shape[0])

    def predict(self, control_input):
        # Предсказание состояния
        self.state = self.state_matrix @ self.state + self.control_matrix @ control_input
        self.covariance = self.state_matrix @ self.covariance @ self.state_matrix.T + self.process_noise

    def update(self, measurement):
        # Обновление состояния
        kalman_gain = self.covariance @ self.observation_matrix.T @ np.linalg.inv(
            self.observation_matrix @ self.covariance @ self.observation_matrix.T + self.measurement_noise)
        self.state = self.state + kalman_gain @ (measurement - self.observation_matrix @ self.state)
        self.covariance = (np.eye(self.state_matrix.shape[0]) - kalman_gain @ self.observation_matrix) @ self.covariance

        return self.state


# Пример использования:
state_matrix = np.array([[1, 0.1], [0, 1]])  # Матрица перехода состояния
control_matrix = np.array([[0.1], [0]])  # Матрица управления
observation_matrix = np.array([[1, 0]])  # Матрица наблюдения
process_noise = np.array([[0.01, 0], [0, 0.01]])  # Шум процесса
measurement_noise = np.array([[0.1]])  # Шум измерения

kalman_filter = KalmanFilter(state_matrix, control_matrix, observation_matrix, process_noise, measurement_noise)

# Симуляция:
for i in range(10):
    control_input = np.array([[0.5]])  # Управляющее воздействие
    kalman_filter.predict(control_input)

    measurement = np.array([[2.5]])  # Измерение
    state = kalman_filter.update(measurement)

    print(f"Шаг {i + 1}: Оценка состояния: {state}")
