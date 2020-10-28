import database as db

from utils import (
    request_input,
    print_invalid_option
)


def login_or_signup():
    print('To exit program type `exit` at any point')
    print('Enter:')
    print('1 for Login')
    print('2 for Sign-up')

    while (True):
        action = request_input()[0]

        # Login
        if action == '1':
            return login()
        # Sign up
        elif action == '2':
            return signup()
        # Invalid selection
        else:
            print_invalid_option(max_option=2)


def login():
    print("To return to main screen type `back`")
    print("Enter: Id")
    while (True):
        # login_values will have len of 2 (1 + pass)
        login_values = request_input(expected_len=1, logout_allowed=False, password=True)
        if not login_values:
            continue

        if login_values[0] == "back":
            return False, None, None, None

        # Attempt to login
        login_success = db.login(
            login_values[0], login_values[1]
        )
        if login_success:
            # Check if user is privileged
            is_privileged = db.check_privilege(login_values[0])
            return True, login_values[0], login_values[1], is_privileged
        else:
            print("Login failed, please try again")


def signup():
    print("To return to main screen type `back`")
    print("Enter: Id, Name, City")
    while(True):
        # Sign_up_values will have len of 4 (3 + pass)
        sign_up_values = request_input(expected_len=3, logout_allowed=False, password=True)
        if not sign_up_values:
            continue

        if sign_up_values[0] == "back":
            return False, None, None, None

        # Attempt to sign up
        sign_up_success = db.sign_up(
            sign_up_values[0],
            sign_up_values[1],
            sign_up_values[2],
            sign_up_values[3]
        )

        if sign_up_success:
            return True, sign_up_values[0], sign_up_values[3], False
        else:
            print("Sign up failed, please try again")
