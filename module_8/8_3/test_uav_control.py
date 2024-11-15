import unittest
from unittest.mock import Mock, patch
import uav_control
import pymavlink.mavutil as mavutil


class TestUAVControl(unittest.TestCase):
    def setUp(self):
        connection_string = "tcp:127.0.0.1:5762"
        self.patcher = patch('pymavlink.mavutil.mavlink_connection')
        self.addCleanup(self.patcher.stop)
        self.mock_master = self.patcher.start()

        self.mock_master.return_value.wait_heartbeat.return_value = None
        self.uav = uav_control.UAVControl(connection_string)

    def test_connection_successful(self):
        with patch('pymavlink.mavutil.mavlink_connection') as mock_conn:
            mock_conn.return_value = self.mock_master
            uav_control.UAVControl("tcp:127.0.0.1:5762")
            mock_conn.assert_called_with("tcp:127.0.0.1:5762")

    def test_arm(self):
        self.uav.arm()
        self.mock_master.return_value.arducopter_arm.assert_called_once()
        self.mock_master.return_value.motors_armed_wait.assert_called_once()

    def test_disarm(self):
        self.uav.disarm()
        self.mock_master.return_value.arducopter_disarm.assert_called_once()
        self.mock_master.return_value.motors_disarmed_wait.assert_called_once()

    def test_takeoff(self):
        positive_altitude = 10
        mock_return_value = Mock(lat=520000000, lon=200000000)

        with patch.object(self.uav, 'set_mode') as mock_set_mode, \
                patch.object(self.uav.master, 'recv_match', new_callable=Mock, return_value=mock_return_value) as mock_recv_match, \
                patch.object(self.uav.master.mav, 'command_long_send') as mock_command_long_send, \
                patch.object(self.uav, 'wait_command_ack', return_value=True) as mock_wait_command_ack:

            self.uav.takeoff(positive_altitude)

            mock_set_mode.assert_called_once_with('GUIDED')
            mock_recv_match.assert_called_once_with(type='GLOBAL_POSITION_INT', blocking=True, timeout=5)
            mock_command_long_send.assert_called_once()
            mock_wait_command_ack.assert_called_once_with(mavutil.mavlink.MAV_CMD_NAV_TAKEOFF)

    def test_takeoff_negative_altitude(self):
        negative_altitude = -5
        with self.assertRaises(ValueError):
            self.uav.takeoff(negative_altitude)

    def test_set_mode(self):
        valid_mode = "GUIDED"
        self.mock_master.return_value.mode_mapping.return_value = {"GUIDED": 4}

        self.uav.set_mode(valid_mode)
        self.mock_master.return_value.set_mode.assert_called_with(4)

    def test_set_mode_invalid(self):
        invalid_mode = "INVALID_MODE"
        self.mock_master.return_value.mode_mapping.return_value = {"GUIDED": 4}

        with self.assertRaises(ValueError):
            self.uav.set_mode(invalid_mode)

    def test_get_telemetry(self):
        self.mock_master.return_value.recv_match.return_value = Mock(get_type=lambda: 'GLOBAL_POSITION_INT',
                                                                     lat=520000000, lon=200000000, alt=10000)
        telemetry = self.uav.get_telemetry()

        self.assertIsNotNone(telemetry)
        self.assertDictEqual(telemetry, {'lat': 52.0, 'lon': 20.0, 'alt': 10.0})

    def test_wait_command_ack(self):
        self.mock_master.return_value.recv_match.return_value = Mock(command=mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
                                                                     result=mavutil.mavlink.MAV_RESULT_ACCEPTED)
        result = self.uav.wait_command_ack(mavutil.mavlink.MAV_CMD_NAV_TAKEOFF)
        self.assertTrue(result)

    def test_goto(self):
        lat, lon, alt = 52.0, 20.0, 10.0
        with patch.object(self.uav, 'wait_command_ack', return_value=True) as mock_wait_ack:
            self.uav.goto(lat, lon, alt)

            self.mock_master.return_value.mav.mission_item_send.assert_called_once_with(
                self.mock_master.return_value.target_system,
                self.mock_master.return_value.target_component,
                0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
                mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
                0, 1, 0, 0, 0, 0, lat, lon, alt
            )

            mock_wait_ack.assert_called_once()

            args, kwargs = self.mock_master.return_value.mav.mission_item_send.call_args
            self.assertEqual(args[3], mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT)
            self.assertEqual(args[4], mavutil.mavlink.MAV_CMD_NAV_WAYPOINT)
            self.assertEqual(args[13], alt)
            self.assertEqual(args[11], lat)
            self.assertEqual(args[12], lon)


if __name__ == '__main__':
    unittest.main()
