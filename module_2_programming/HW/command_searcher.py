def bubble_sort(commands):
    """
    Sorts a list of commands based on priority and timestamp. Primary sorting by priority, secondary by timestamp.

    Arguments:
    commands - List of tuples, where each tuple should have three elements (command_name, priority, timestamp).
               Example format: [("command", 1, 20210101), ("command2", 2, 20210102)].

    Returns:
    List of tuples sorted first by priority and then by timestamp when priorities are equal.

    Raises:
    ValueError - If 'commands' is None or any tuple in the list does not have exactly three elements.
    """
    if commands is None:
        raise ValueError("The command list should not be None")

    print(f"Initial list of commands: {commands}")
    n = len(commands)
    for i in range(n):
        for j in range(0, n - i - 1):
            if len(commands[j]) < 3 or len(commands[j + 1]) < 3:
                raise ValueError("Each command must include all three elements: command_name, priority, and timestamp")

            current_priority, next_priority = commands[j][1], commands[j + 1][1]
            current_timestamp, next_timestamp = commands[j][2], commands[j + 1][2]
            if (current_priority > next_priority) or (
                    current_priority == next_priority and current_timestamp > next_timestamp):
                commands[j], commands[j + 1] = commands[j + 1], commands[j]
    print(f"Sorted list of commands: {commands}")
    return commands


def linear_search(commands, command_name):
    """
    Conducts a linear search for a command by name in a list of command tuples.

    Arguments:
    commands - List of command tuples, where each tuple should be structured as (command_name, priority, timestamp).
    command_name - A string representing the command's name to search for.

    Returns:
    The command tuple matching the command_name if found, otherwise None.

    Raises:
    ValueError - If 'commands' is None or any tuple in the list is incomplete (lacks three elements).
    """
    if commands is None:
        raise ValueError("The command list should not be None")

    for command in commands:
        if len(command) < 3:
            raise ValueError("Each command must include all three elements: command_name, priority, and timestamp")
        if command[0] == command_name:
            print(f"Chosen command: {command}")
            return command
    return None
