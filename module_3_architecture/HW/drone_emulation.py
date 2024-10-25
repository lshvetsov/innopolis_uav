import time
import random
from drone_components import FlightController


def main():
    fc = FlightController()

    print("Взлетаем...")
    fc.take_off(3000)

    for remaining in range(3, 0, -1):
        print(f"Осталось {remaining} секунд...")
        time.sleep(1)

    print("Взлет произведен успешно!")
    print("--------------------------------------")
    print("Показания датчиков:")
    fc.read_sensor_data()

    target_altitude = 500

    for i in range(5):
        print(f"\n-------------Итерация {i}---------------")
        data = fc.read_sensor_data()
        current_altitude = data['altitude']

        print(f"Высоты: текущая - {current_altitude} м, целевая - {target_altitude} м.\n")

        current_speed = fc.get_speed()[0]

        if current_altitude < target_altitude:
            current_speed += random.randint(100, 500)
        elif current_altitude > target_altitude:
            current_speed -= random.randint(100, 500)
        else:
            print("Высота в пределах нормы, скорость не изменяем.")

        current_speed = max(min(current_speed, 8000), 1000)

        print(f"Устанавливаем скорость двигателей: {current_speed}")
        fc.control_speed(current_speed)
        time.sleep(1)


if __name__ == "__main__":
    main()
