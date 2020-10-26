def split_and_strip(str_):
    return [x.strip() for x in str_.split(',')]


def request_input():
    print('')
    response =  input('Input: ')
    print('')

    return split_and_strip(response)

def print_invalid_input():
    print("Input is invalid")