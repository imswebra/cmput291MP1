from sys import exit
from getpass import getpass


def split_and_strip(input_val):
    return [x.strip() for x in str(input_val).split(',')]


def request_input(password=False):
    response =  input('Input: ')
    values = split_and_strip(response)

    if values[0] == "exit":
        exit()

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