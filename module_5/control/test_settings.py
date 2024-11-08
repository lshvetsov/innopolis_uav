import matplotlib.pyplot as plt

# Данные логов, хранящиеся в списке
data = [
  [0.0, 10.0, 0.0],
  [0.1, 10.1, 0.1],
  [0.2, 10.2, 0.2],
  [0.3, 10.3, 0.3],
  [0.4, 10.4, 0.4],
  [0.5, 10.5, 0.5],
  [0.6, 10.3, 0.3],
  [0.7, 10.7, 0.7],
  [0.8, 10.8, 0.8],
  [0.9, 10.9, 0.9],
  [1.0, 11.0, 1.0],
]

# Разделение данных на столбцы
time = [row[0] for row in data]
altitude = [row[1] for row in data]
pitch = [row[2] for row in data]

# Построение графика высоты
plt.figure()
plt.plot(time, altitude)
plt.xlabel("Время (с)")
plt.ylabel("Высота (м)")
plt.title("Высота дрона")

# Построение графика угла тангажа
plt.figure()
plt.plot(time, pitch)
plt.xlabel("Время (с)")
plt.ylabel("Угол тангажа (град)")
plt.title("Угол тангажа дрона")

plt.show()
