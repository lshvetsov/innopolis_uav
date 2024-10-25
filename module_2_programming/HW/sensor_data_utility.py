# Function: sort_records_by_time
# Description:
#   Sorts a list of record dictionaries by the 'time' key.
#   If a record lacks the 'time' key or records is None, it raises ValueError.
# Parameters:
#   records (list of dicts): The list of records to sort.
# Returns:
#   List[dict]: The list of records sorted by the 'time'.
def sort_records_by_time(records):
    if not records:
        raise ValueError("Input list is None or empty")
    if any('time' not in record for record in records):
        raise ValueError("All records must have a 'time' key")
    return sorted(records, key=lambda record: record['time'])


# Function: filter_records_data
# Description:
#   Filters a list of record dictionaries based on a specified parameter and value.
#   Useful for identifying records that match particular characteristics.
# Parameters:
#   records (list of dicts): The list of records to filter.
#   parameter (str): The dictionary key to use for filtering.
#   value (any): The value to match for the given parameter.
# Returns:
#   list[dict]: List of records where the specified parameter matches the given value.
def filter_records_data(records, parameter, value):
    records = [record for record in records if record.get(parameter) == value]
    print(f"Filtered records: {records}")
    return records
