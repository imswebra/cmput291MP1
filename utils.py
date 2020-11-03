from sys import exit
from getpass import getpass


def split_and_strip(input_val):
    """Splits input on commas and strips away whitespace

    Returns:
        ([str]): The split input
    """

    return [x.strip() for x in str(input_val).split(',')]


def request_input(expected_len=0, logout_allowed=True, password=False):
    """Requests comma seperated input from user

    Args:
        expected_len (int): If specificed, this function will verify the input
            to have the number of args specicified by expected_len except in
            the case of a keyword. Passwords do not contribute to the number of
            args.
        logout_allowed (bool): Specifies whether "/logout" should be considered
            a valid keyword
        password (bool): Specifies whether the user should be prompted for a
            password after the regular input
    Returns:
        ([str]): The received input values
    """
    response = input('Input: ')
    values = split_and_strip(response)

    if values[0] == "/exit":
        exit(0)

    keywords = ["/back"]
    if logout_allowed:
        keywords += "/logout"

    if (expected_len > 0 and values[0] not in keywords
            and len(values) != expected_len):
        print_invalid_input((expected_len, len(values)))
        return None

    if password and values[0] not in keywords:
        password = getpass()
        values.append(password)

    print('')
    return values


def keyword_input_validate(str):
    """Validates input string for keywords

    Utility function to validate string from a manual input() call when using
    request_input isn't appropriate.

    Args:
        str (str): The string to validate
    Returns:
        (bool): Whether or not a keyword is found
        (bool): True if found keyword was "/logout", False otherwise
    """
    stripped = str.strip()
    if stripped == "/exit":
        exit(0)
    elif stripped == "/back":
        return True, False
    elif stripped == "/logout":
        return True, True
    return False, False


def print_invalid_input(len_tuple=None):
    """Prints an invalid input message

    Args:
        len_tuple ((expected # items, received # items)): If specified, invalid
        message will use the "Expected #, got #" form
    """
    if len_tuple:
        print("Invalid input, expected", len_tuple[0], "items, got", len_tuple[1])
    else:
        print("Input is invalid")


def print_options(options, skip_options=[]):
    """Prints the given options, skipping the skip_options if specified

    Args:
        options ([str]): List of options to print
        skip_options ([str]): List of options from options arg to skip
    """
    print("Enter:")
    for i, option in enumerate(options, 1):
        if option not in skip_options:
            print("  " + str(i), "to", option)


def print_invalid_option(max_option=None):
    """Prints an invalid option message

    Args:
        max_option (int): If specified, used for expect values usage hint
    """
    if max_option:
        print("Invalid option, expected option between 1 and", max_option)
    else:
        print("Invalid option")


def get_indices_range(results, old_min=-5, old_max=0):
    """Returns minimum and maximum indices for a range slice on results

    Utility function for showing a maximum of 5 results at a time. On first use,
    the caller should ignore the optional old_min and old_max parameters.
    Afterwards, the received min and max from the first use should be used for
    these optional parameters so they are incremented accordingly.

    Args:
        results ([results row]): The list of results
        old_min (int): The previous minimum index from this function
        old_max (int): The previous maximum index from this function
    Returns:
        (int): The minimum index for results range (inclusive)
        (int): The maximum index for results range (exclusive)

    """
    increment = 5
    new_min = old_min + increment
    new_max = min(old_max + increment, len(results))

    if len(results) > new_max:
        print("Type `more` to see more results")
    return new_min, new_max


def get_table_info(data, header, trunc_widths={}, index_start=0):
    """Returns table information for future printing with print_table

    The returned table is a copy of data with the elements stringified, every
    row given an index number, and the header inserted.

    Args:
        data ([data row]): A list of lists with equal sized inner lists
        header ([str]): A list of the headers for the table
        trunc_widths({column index:max width}): If specified, any column given
            by indices present in trunc_widths will have its stringified
            elements truncated to the max width.
        index_start (int): If specified, the row indicies will start at that
            value
    Returns:
        ([printable row]): The table
        ([int]): A list of the tables maximum character widths for each column
    """
    data_table = [[str(i), *stringify_list(row, trunc_widths)]
                  for i, row in enumerate(data, index_start)]
    data_table.insert(0, header)
    return data_table, get_column_widths(data_table)


def stringify_list(source_list, max_lengths={}):
    """Stringifies every element in source_list, and returns the new list

    Helper function for get_table_info.

    Args:
        source_list ([elements]): The list to be stringified
        max_lengths({i:max width}): If specified, any element at index i
            present in max_lengths will be truncated to max width.
    Returns:
        ([elements]): The stringified list
    """
    return [stringify(elem, max_lengths.get(i))
            for i, elem in enumerate(source_list)]


def stringify(obj, max_len=None):
    """Returns passed object as string, truncated at max_len

    Helper function for stringify_list.

    Args:
        obj (any): The object to be stringified
        max_len(int): If specified and > 3, the stringified object will be
            truncated with ellipses ('My senten...').
    Returns:
        (str): The stringified object. Returns "N/A" if the object was None.
    """
    return_str = str(obj) if obj is not None else "N/A"
    if max_len is not None and max_len > 3 and len(return_str) > max_len:
        return_str = return_str[:(max_len - 3)] + "..."
    return return_str


def get_column_widths(table):
    """Returns a list of maximum column string widths given a list of lists

    Helper function for get_table_info.

    Args:
        table ([row]): The table to check max widths. The inner lists (rows)
            are assumed to all be of equal size.
    Returns:
        ([int]): A list of the maximum character widths for each column
    """
    transposed_table = list(map(list, zip(*table)))
    return [max(len(str(s)) for s in row) for row in transposed_table]


def print_table(table, width_str, widths):
    """Pretty prints a table (list of lists)

    Args:
        table ([table row]): The table to be printed. The first row is assumed
            to be the header.
        width_str (str): A string containing empty placeholders with
            width specifications in the str.format() style ({:width}). Assumed
            to have equal number of placeholders as the size of widths.
        widths ([int]): A list of the tables maximum character widths for each
            column. Assumed to have equal size to width_str's number of
            placeholders.
    """
    print(width_str.format(*table[0]))
    print(width_str.format(*["-" * width for width in widths]))
    for row in table[1:]:
        print(width_str.format(*row))


def is_index(s, results):
    """Returns whether string s is an appropriate index into results

    Args:
        s (str): The string to check, assumed to be one-based instead of
            zero-based
        results ([results row]): The results to check
    Returns:
        (bool): True if the string is an index into results, False otherwise
    """
    try:
        if int(s) - 1 < len(results) and int(s) - 1 >= 0:
            return True
        else:
            return False
    except ValueError:
        return False
