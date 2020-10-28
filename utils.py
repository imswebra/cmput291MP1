from sys import exit
from getpass import getpass


def split_and_strip(input_val):
    return [x.strip() for x in str(input_val).split(',')]


def request_input(expected_len=0, logout_allowed=True, password=False):
    '''Requests input from user.
    Takes three optional parameters.
    If expected_len is specificed, this function will handle error messages and
    and return none when the number inputs recieved does not match expected_len,
    except for when a keyword such as exit, back, or logout is input. Passwords
    do not contribute to the number of inputs count.
    Logout_allowed specifies whether "logout" should be considered a keyword.
    Password specifies whether the input should prompt for a password after the
    regular input.
    '''
    response = input('Input: ')
    values = split_and_strip(response)

    if values[0] == "exit":
        exit(0)

    if logout_allowed:
        keywords = {"back", "logout"}
    else:
        keywords = {"back"}

    if (expected_len > 0 and values[0] not in keywords
            and len(values) != expected_len):
        print_invalid_input((expected_len, len(values)))
        return None

    if password and values[0] not in keywords:
        password = getpass()
        values.append(password)

    print('')
    return values


def print_invalid_input(len_tuple=None):
    '''Prints an invalid input message.
    Takes optional tuple of the form (expected_num_items, received_num_items)
    for "Expected #, got #" style messages.
    '''
    if len_tuple:
        print("Invalid input, expected", len_tuple[0], "items, got", len_tuple[1])
    else:
        print("Input is invalid")


def print_invalid_option():
    print("Invalid option")


def get_max_min_index(results, old_min=None, old_max=None):
    increment = 5
    # First time
    if old_min is None:
        new_min = 0
        if len(results) > increment:
            new_max = increment
            print("Type `more` to see more result")
        else:
            new_max = len(results)
    # Not the first time
    else:
        new_min = old_max + 1
        if len(results) > old_max + increment:
            new_max = old_max + increment
            print("Type `more` to see more result")
        else:
            new_max = len(results)

    return new_min, new_max


def is_index(s, results):
    try:
        if int(s) < len(results):
            return True
        else:
            return False
    except ValueError:
        return False
