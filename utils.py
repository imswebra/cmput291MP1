from sys import exit

def split_and_strip(input_val):
    return [x.strip() for x in str(input_val).split(',')]


def request_input():
    response =  input('Input: ')
    print('')
    values = split_and_strip(response)

    if values[0] == "exit":
        exit()

    return values

def print_invalid_input():
    print("Input is invalid")

def print_invalid_option():
    print("Invalid option")