import database as db

from utils import (
    request_input,
    print_options,
    print_invalid_option
)


def login_or_signup():
    """The execution loop for a user to login or signup

    Returns:
        (str): The uid of the logged in user, None if login/signup failed
        (bool): True if user is priviledged, False if user is not priviledged,
            None if login/signup failed
    """
    print("To exit program type `/exit` at any point")
    print_options(["Login", "Sign-up"])

    while (True):
        action = request_input()[0]

        # Login
        if action == '1':
            return login()
        # Sign up
        elif action == '2':
            return signup(), False
        # Invalid selection
        else:
            print_invalid_option(max_option=2)


def login():
    """Allows user to login into an existing account

    Returns:
        (str): The uid of the logged in user, None if login failed
        (bool): True if user is priviledged, False if user is not priviledged,
            None if login failed
    """
    print("To return to the main screen, type `/back`")
    while (True):
        print("Enter: ID")

        # login_values will have len of 2 (1 + pass)
        login_values = request_input(expected_len=1, logout_allowed=False, password=True)
        if not login_values:
            continue

        if login_values[0] == "/back":
            return None, None

        # Attempt to login
        login_success = db.login(
            login_values[0], login_values[1]
        )
        if login_success:
            # Check if user is privileged
            is_privileged = db.check_privilege(login_values[0])
            return login_values[0], is_privileged
        else:
            print("Please try again")  # db.login handles some messaging before


def signup():
    """Allows user to sign up for a new account

    Returns:
        (str): The uid of the signed-up user, None if signup failed
    """
    print("Sign-up")
    print("To return to the main screen, type `/back`")
    while(True):
        print("Enter: ID, Name, City")
        # Sign_up_values will have len of 4 (3 + pass)
        sign_up_values = request_input(expected_len=3, logout_allowed=False, password=True)
        if not sign_up_values:
            continue

        if sign_up_values[0] == "/back":
            return None
        if len(sign_up_values[0]) > 4:
            print("ID must be less than 5 characters")
            continue

        # Attempt to sign up
        sign_up_success = db.sign_up(
            sign_up_values[0],
            sign_up_values[1],
            sign_up_values[2],
            sign_up_values[3]
        )

        if sign_up_success:
            return sign_up_values[0]
        else:
            print("Sign up failed, please try again")
