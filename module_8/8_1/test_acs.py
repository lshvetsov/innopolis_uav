import numpy as np
from acs import data_accel, generate_test_data, apply_kalman
from unittest.mock import patch


def test_data_accel():
    # Test data
    accel_data = [
        np.array([1, 2, 3]),
        np.array([4, 5, 6]),
        np.array([7, 8, 9])
    ]
    dt = 0.01
    expected_positions = {
        'pos_x': [0.01, 0.03, 0.06],
        'pos_y': [0.04, 0.09, 0.15],
        'pos_z': [0.07, 0.15, 0.24]
    }

    # Call the function
    positions = data_accel(accel_data, dt)

    # Check results using numpy's testing functions for array comparison
    np.testing.assert_array_almost_equal(positions['pos_x'], expected_positions['pos_x'])
    np.testing.assert_array_almost_equal(positions['pos_y'], expected_positions['pos_y'])
    np.testing.assert_array_almost_equal(positions['pos_z'], expected_positions['pos_z'])


def test_generate_test_data():
    num_samples = 10
    data = generate_test_data(num_samples)
    assert len(data[0]) == num_samples
    assert len(data[1]) == num_samples
    assert len(data[2]) == num_samples


@patch('acs.predict')
@patch('acs.update')
def test_apply_kalman(mock_update, mock_predict):
    # Setup mock return values
    mock_predict.return_value = (np.zeros((2, 1)), np.eye(2))
    mock_update.return_value = (np.zeros((2, 1)), np.eye(2))

    positions = {'pos_x': [0, 1, 2], 'pos_y': [0, 1, 2], 'pos_z': [0, 1, 2]}
    filtered_positions = apply_kalman(positions)

    # Assertions to check if Kalman filter is applied correctly
    assert len(filtered_positions['pos_x']) == 3
    assert len(filtered_positions['pos_y']) == 3
    assert len(filtered_positions['pos_z']) == 3
