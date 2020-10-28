from sys import exit
from getpass import getpass


def split_and_strip(input_val):
    return [x.strip() for x in str(input_val).split(',')]


def request_input(password=False):
    response = input('Input: ')
    values = split_and_strip(response)

    if values[0] == "exit":
        exit(0)

    keywords = {"back", "logout"}

    if password and values[0] not in keywords:
        password = getpass()
        values.append(password)

    print('')
    return values


def print_invalid_input():
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
