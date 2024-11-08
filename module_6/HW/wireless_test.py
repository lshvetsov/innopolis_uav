import speedtest_cli as speedtest
from bleak import BleakScanner, BleakClient
import asyncio
import random


class WirelessSignalTest:
    def __init__(self, wifi_ssid, bluetooth_device_name):
        self.wifi_ssid = wifi_ssid
        self.bluetooth_device_name = bluetooth_device_name

    def run_tests(self):
        print("Запуск проверки сигнала Wi-Fi...")
        self.check_wifi_signal()
        print("Запуск проверки сигнала Bluetooth...")
        asyncio.run(self.check_bluetooth_signal())
        print("Запуск проверки сигнала радиосвязи...")
        self.check_radio_signal()

    def check_wifi_signal(self):
        try:
            wifi_speed_test = speedtest.Speedtest()
            wifi_speed_test.get_best_server()

            download_speed = wifi_speed_test.download()
            upload_speed = wifi_speed_test.upload()
            ping = wifi_speed_test.results.ping

            print(f"Скорость загрузки Wi-Fi: {download_speed / 1_000_000:.2f} Мбит/с")
            print(f"Скорость выгрузки Wi-Fi: {upload_speed / 1_000_000:.2f} Мбит/с")
            print(f"Пинг Wi-Fi: {ping} мс")

            # Имитация проверки уровня сигнала в дБ
            signal_strength = random.randint(-80, -30)
            self.evaluate_wifi_signal(signal_strength)

        except Exception as e:
            print(f"Ошибка при проверке сигнала Wi-Fi: {str(e)}")

    def evaluate_wifi_signal(self, signal_strength):
        """Оценка качества Wi-Fi сигнала на основе уровня в дБ."""
        if signal_strength > -70:
            print("Wi-Fi сигнал хороший")
        elif signal_strength > -85:
            print("Wi-Fi сигнал удовлетворительный")
        else:
            print("Wi-Fi сигнал слабый")

    async def check_bluetooth_signal(self):
        try:
            print("Сканирование Bluetooth устройств...")
            nearby_devices = await BleakScanner.discover()
            print("Найденные Bluetooth устройства:")
            for device in nearby_devices:
                print(f" {device.address} - {device.name} (RSSI: {device.rssi})")

            # Проверка подключения к выбранному устройству
            device_found = next((device for device in nearby_devices if device.name == self.bluetooth_device_name),
                                None)
            if device_found:
                print(f"Пытаемся установить соединение с {device_found.name} (адрес: {device_found.address})")
                async with BleakClient(device_found) as client:
                    if client.is_connected:
                        print("Bluetooth подключение успешно!")
                        print(f"RSSI устройства: {device_found.rssi} дБ")
            else:
                print("Устройство Bluetooth не найдено.")
        except Exception as e:
            print(f"Ошибка при проверке сигнала Bluetooth: {str(e)}")

    def get_radio_signal_quality(self):
        """Имитация получения уровня радиосигнала."""
        signal_strength = random.randint(1, 100)
        if signal_strength >= 70:
            return "хороший"
        elif 40 <= signal_strength < 70:
            return "удовлетворительный"
        else:
            return "слабый"

    def check_radio_signal(self):
        """Проверка уровня сигнала радиосвязи."""
        print("Тест радиосвязи выполняется...")
        radio_signal_quality = self.get_radio_signal_quality()

        if radio_signal_quality == "хороший":
            print("Радиосвязь хорошая")
        elif radio_signal_quality == "удовлетворительный":
            print("Радиосвязь удовлетворительная")
        else:
            print("Радиосвязь слабая или отсутствует")


# Запуск тестирования
if __name__ == "__main__":
    wifi_ssid = 'SSID'  # SSID Wi-Fi
    bluetooth_device_name = 'STANMORE III [LE]'  # Название Bluetooth устройства
    tester = WirelessSignalTest(wifi_ssid, bluetooth_device_name)
    tester.run_tests()
