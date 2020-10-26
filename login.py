import database as db

from utils import (
    request_input,
    print_invalid_input,
    print_invalid_option
)

def login():
    print('To exit program type `exit` at any point')
    print('Enter:')
    print('1 for Login')
    print('2 for Sign-up')

    while (True):
        action = request_input()[0]

        #Login
        if action == '1':
            print("To return to main screen type `back`")
            print('Enter: Id, password')
            while(True):
                login_values = request_input() #TODO: Should not show password
                if login_values[0] == "back":
                    return False, None, None, None

                if len(login_values) == 2:
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
                else:
                    print_invalid_input()


        #Sign up
        elif action == '2':
            print("To return to main screen type `back`")
            print('Enter: Id, Name, City, Password')
            while(True):
                sign_up_values = request_input() #TODO: Should not show password
                if sign_up_values[0] == "back":
                    return False, None, None, None

                if len(sign_up_values) == 4:
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
                else:
                    print_invalid_input()

        # Invalid selection
        else:
            print_invalid_option()