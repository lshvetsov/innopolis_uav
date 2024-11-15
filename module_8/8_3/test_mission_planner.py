import unittest
from unittest.mock import patch
from mission_planner import MissionPlanner


class TestMissionPlanner(unittest.TestCase):
    @patch('mission_planner.UAVControl')
    def setUp(self, mock_uav_control):
        self.connection_string = "tcp:127.0.0.1:5762"
        self.planner = MissionPlanner(self.connection_string)
        self.mock_uav = mock_uav_control.return_value

    def test_execute_mission_success(self):
        waypoints = [(52.0, 20.0, 100), (52.002, 20.003, 100), (52.005, 20.005, 100)]
        # Настроить моки
        self.mock_uav.get_telemetry.side_effect = [
            {'lat': 52.0, 'lon': 20.0, 'alt': 100},
            {'lat': 52.002, 'lon': 20.003, 'alt': 100},
            {'lat': 52.005, 'lon': 20.005, 'alt': 100}
        ]

        with patch('time.sleep'), patch('mission_planner.logger'):
            self.planner.execute_mission(waypoints)
            self.assertEqual(self.mock_uav.goto.call_count, len(waypoints))

    def test_execute_mission_failure(self):
        waypoints = [(52.0, 20.0, 100), (53.0, 21.0, 50)]
        # Настроить мок, чтобы телеметрия указывала на неудачное достижение второй точки
        self.mock_uav.get_telemetry.side_effect = [
            {'lat': 52.0, 'lon': 20.0, 'alt': 100},  # Первая точка достигнута
            None, None, None, None, None  # Вторая точка не достигнута
        ]

        with patch('time.sleep'), patch('mission_planner.logger') as mock_logger:
            with self.assertRaises(Exception) as context:
                self.planner.execute_mission(waypoints)

            self.assertTrue('Не удалось достичь точки' in str(context.exception))
            mock_logger.error.assert_called_with('Не удалось достичь точки 2')


if __name__ == '__main__':
    unittest.main()
