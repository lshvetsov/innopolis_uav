import numpy as np


def predict(x, P, dt, Q):
    A = np.array([[1, dt], [0, 1]])  # Матрица перехода состояния
    x = A @ x
    P = A @ P @ A.T + Q
    return x, P


def update(x, P, z, R):
    H = np.array([[1, 0]])  # Наблюдательная матрица
    y = z - H @ x  # Ошибка измерения
    S = H @ P @ H.T + R  # Ковариация ошибки
    K = P @ H.T @ np.linalg.inv(S)  # Фильтр Калмана
    x = x + K @ y  # Обновление состояния системы
    P = (np.eye(2) - K @ H) @ P  # Обновление ковариации
    return x, P
