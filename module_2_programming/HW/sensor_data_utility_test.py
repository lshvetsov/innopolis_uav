from sensor_data_utility import sort_records_by_time, filter_records_data


# Test cases
def test_sort_by_time():
    # Test to verify that sorting by time works correctly
    records = [
        {"time": "2021-09-03 12:00:00", "latitude": 34.15},
        {"time": "2021-09-01 12:10:00", "latitude": 34.05},
        {"time": "2021-09-02 12:20:00", "latitude": 34.06}
    ]
    sorted_records = sort_records_by_time(records)
    assert sorted_records[0]["time"] == "2021-09-01 12:10:00", "Should sort by time, earliest first."


def test_sort_by_time_several():
    # Test to verify that sorting by time works correctly
    records = [
        {"time": "2021-09-03 12:00:00", "latitude": 34.15},
        {"time": "2021-09-01 12:10:00", "latitude": 34.05},
        {"time": "2021-09-02 12:20:00", "latitude": 34.05}
    ]
    sorted_records = sort_records_by_time(records)
    assert len(sorted_records) == 2


def test_missing_time_field():
    # Test to ensure error is raised when 'time' field is missing
    records = [
        {"latitude": 34.15},  # Missing 'time'
        {"time": "2021-09-01 12:10:00", "latitude": 34.05}
    ]
    try:
        sort_records_by_time(records)
    except ValueError as e:
        assert str(e) == "All records must have a 'time' key", "Should raise ValueError for missing time key"


def test_null_input():
    # Test to ensure error is raised when input is None
    try:
        sort_records_by_time(None)
    except ValueError as e:
        assert str(e) == "Input list is None or empty", "Should raise ValueError for None input"


def test_filter_records_by_altitude():
    # Test to verify that filtering by 'altitude' works correctly
    records = [
        {"time": "2021-09-01 12:00:00", "latitude": 34.05, "altitude": 300},
        {"time": "2021-09-02 12:10:00", "latitude": 34.06, "altitude": 350},
        {"time": "2021-09-03 12:20:00", "latitude": 34.07, "altitude": 300}
    ]
    filtered_records = filter_records_data(records, "altitude", 300)
    assert len(filtered_records) == 2, "Should filter records by altitude, expecting two entries of altitude 300."


def test_filter_records_missing_parameter():
    # Test to ensure functionality with missing parameter
    records = [
        {"time": "2021-09-01", "latitude": 34.05},  # Missing 'altitude'
        {"time": "2021-09-02", "latitude": 34.06, "altitude": 300}
    ]
    filtered_records = filter_records_data(records, "altitude", 300)
    assert len(filtered_records) == 1, "Should handle missing parameter gracefully."


def test_filter_records_none_input():
    # Test to ensure behavior with None input
    try:
        filter_records_data(None, "altitude", 300)
    except TypeError:
        print("Handled None input correctly via exception.")
    except Exception as e:
        assert False, f"Unexpected error type: {type(e)} when handling None input."


def test_filter_records_nonexistent_value():
    # Test filtering for a nonexistent value
    records = [
        {"time": "2021-09-01", "altitude": 200},
        {"time": "2021-09-02", "altitude": 250}
    ]
    filtered_records = filter_records_data(records, "altitude", 300)
    assert len(filtered_records) == 0, "Should return an empty list for a nonexistent value."


def run_all_tests():
    test_sort_by_time()
    test_missing_time_field()
    test_null_input()
    test_filter_records_by_altitude()
    test_filter_records_missing_parameter()
    test_filter_records_none_input()
    test_filter_records_nonexistent_value()
    print("All tests passed successfully.")


# Running tests
if __name__ == "__main__":
    run_all_tests()
