from command_searcher import bubble_sort, linear_search


def test_success_bubble_sort():
    # Test sorting when priorities and timestamps require reordering
    commands = [("start", 2, 20210102), ("stop", 1, 20210101), ("pause", 2, 20210101)]
    assert bubble_sort(commands) == [("stop", 1, 20210101), ("pause", 2, 20210101),
                                     ("start", 2, 20210102)], "Should sort by priority and then timestamp."


def test_bubble_sort_empty():
    # Test sorting when the commands list is empty
    assert bubble_sort([]) == [], "Should handle empty list."


def test_bubble_sort_None_input():
    # Test sorting raises an error when the input is None
    try:
        bubble_sort(None)
    except ValueError as e:
        assert str(e) == "The command list should not be None"


def test_bubble_sort_incomplete_command():
    # Test sorting when one or more commands do not have all required elements
    commands = [("start", 2), ("stop", 1, 20210101)]
    try:
        bubble_sort(commands)
    except ValueError as e:
        assert str(e) == "Each command must include all three elements: command_name, priority, and timestamp"


def test_linear_search_found():
    # Test searching for a command that exists in the list
    commands = [("start", 1, 20210201), ("stop", 2, 20210202)]
    assert linear_search(commands, "stop") == ("stop", 2, 20210202), "Should find the command stop."


def test_linear_search_not_found():
    # Test searching for a command that does not exist in the list
    commands = [("start", 1, 20210201)]
    assert linear_search(commands, "pause") is None, "Should return None when the command is not found."


def test_linear_search_None_input():
    # Test searching raises an error when the command list is None
    try:
        linear_search(None, "stop")
    except ValueError as e:
        assert str(e) == "The command list should not be None"


def test_linear_search_incomplete_command():
    # Test searching along a list with an incomplete command
    commands = [("start", 1)]
    try:
        linear_search(commands, "start")
    except ValueError as e:
        assert str(e) == "Each command must include all three elements: command_name, priority, and timestamp"


def run_all_tests():
    # Run all test cases
    test_success_bubble_sort()
    test_bubble_sort_empty()
    test_bubble_sort_None_input()
    test_bubble_sort_incomplete_command()
    test_linear_search_found()
    test_linear_search_not_found()
    test_linear_search_None_input()
    test_linear_search_incomplete_command()
    print("All tests passed successfully.")


# Execute the test suite
if __name__ == "__main__":
    run_all_tests()
