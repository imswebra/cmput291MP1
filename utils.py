from sys import exit
from getpass import getpass


def split_and_strip(input_val):
    """Splits input on commas and strips away whitespace"""
    return [x.strip() for x in str(input_val).split(',')]


def request_input(expected_len=0, logout_allowed=True, password=False):
    """Requests input from user.
    Takes three optional parameters.
    If expected_len is specificed, this function will handle error messages and
    and return none when the number inputs recieved does not match expected_len,
    except for when a keyword such as exit, back, or logout is input. Passwords
    do not contribute to the number of inputs count.
    Logout_allowed specifies whether "logout" should be considered a keyword.
    Password specifies whether the input should prompt for a password after the
    regular input.
    """
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
    """Prints an invalid input message.
    Takes optional tuple of the form (expected_num_items, received_num_items)
    for "Expected #, got #" style messages.
    """
    if len_tuple:
        print("Invalid input, expected", len_tuple[0], "items, got", len_tuple[1])
    else:
        print("Input is invalid")


def print_options(options, skip_options=[]):
    """Prints the given options, skipping the skip_options"""
    print("Enter:")
    for i, option in enumerate(options, 1):
        if option not in skip_options:
            print("  " + str(i), "to", option)


def print_invalid_option(max_option=None):
    """Prints an invalid option message.
    If max_option specified, prints message with usage hint.
    """
    if max_option:
        print("Invalid option, expected option between 1 and", max_option)
    else:
        print("Invalid option")


def get_indices_range(results, old_min=-5, old_max=0):
    """Returns minimum and maximum indices for a range slice on results
    Utility function for showing a maximum of 5 results at a time. On first
    use, the caller should ignore the optional old_min and old_max parameters.
    Afterwards, the results from the first use should be used for these
    optional parameters so they are incremented accordingly.
    """
    increment = 5
    new_min = old_min + increment
    new_max = min(old_max + increment, len(results))

    if len(results) > new_max:
        print("Type `more` to see more results")
    return new_min, new_max


def get_table_info(data, header, trunc_widths={}, index_start=0):
    """Returns table information for future printing with print_table
    The data parameter is expected to be a table (list of lists). A copy of
    this table is generated with the elements stringified, and every row given
    an index number. The header is also inserted at the top of this table.
    This table copy and a list of all the columns' max widths are returned.
    If trunc_widths is specified, it is expected to be a dictionary of the form
    column index:max width. Any column index present in trunc_widths with have
    its stringified elements truncated to the max width.
    If index_start is specified, the row indicies will that at that value.
    """
    data_table = [[str(i), *stringify_list(row, trunc_widths)]
                  for i, row in enumerate(data, index_start)]
    data_table.insert(0, header)
    return data_table, get_column_widths(data_table)


def stringify_list(source_list, max_lengths={}):
    """Stringifies every element in source_list, and returns the new list
    If max_lengths is specified, it is expected to be a dictionary of the form
    index:max_length. For any index, max_length pairs in max_lengths, the
    stringified source_list[index] will be truncated to max_length.

    Helper function for get_table_info
    """
    return [stringify(elem, max_lengths.get(i))
            for i, elem in enumerate(source_list)]


def stringify(obj, max_len=None):
    """Returns passed object as string
    If obj is None, returns 'N/A'
    If max_len is specified and > 3, the stringified object will be truncated
    with ellipses ('My senten...')

    Helper function for stringify_list
    """
    return_str = str(obj) if obj is not None else "N/A"
    if max_len is not None and max_len > 3 and len(return_str) > max_len:
        return_str = return_str[:(max_len - 3)] + "..."
    return return_str


def get_column_widths(table):
    """Returns a list of maximum column string widths given a list of lists
    Assumes the size of the inner lists (rows) to all be equal.

    Helper function for get_table_info
    """
    # Assumes table rows are of equal size
    transposed_table = list(map(list, zip(*table)))
    return [max(len(str(s)) for s in row) for row in transposed_table]


def print_table(table, width_str, widths):
    """Pretty prints a table (list of lists)
    width_str is expected to be a string containing empty placeholders with
    width specifications in the str.format() style ({:width}). widths is an
    list containing those width specification values.
    Assumes the first row of the table is the header, and width_str has equal
    width specifications as the size of widths
    """
    print(width_str.format(*table[0]))
    print(width_str.format(*["-" * width for width in widths]))
    for row in table[1:]:
        print(width_str.format(*row))


def is_index(s, results):
    """Returns true if s is an index of results"""
    try:
        if int(s) < len(results):
            return True
        else:
            return False
    except ValueError:
        return False
