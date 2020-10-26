
from sys import argv
import database as db

from utils import (
    split_and_strip,
    request_input,
    print_invalid_input,
    print_invalid_option
)

def logged_in(uid, pwd):
    print('Now logged in, to log out please type `logout`')
    while(True):
        print('Enter:')
        print('1 for Post a Question')
        print('2 for Search Posts')
        print('3 for Post action-Answer')
        print('4 for Post action-Vote')
        action = request_input()[0]

        if (action == "logout"):
            break

        # Post a Question
        elif (action == "1"):
            print('Enter: title text,body text ')
            response = request_input()
            if len(response) == 2:
                post_success = db.post_question(response[0], response[1], uid)
                if post_success:
                    print("Question successfully posted")
                else:
                    print("Question failed to post")

            else:
                print_invalid_input()


        # Search for posts
        elif (action == "2"):
            pass
        # Post action-answer
        elif (action == "3"):
            pass

        # Post action-vote
        elif (action == "4"):
            pass

def login():
    print('To exit program enter `exit` at any point')
    print('Enter:')
    print('1 for Login')
    print('2 for Sign-up')
    while (True):
        action = request_input()[0]

        #Login
        if action == '1':
            print("To return to main screen enter `back`")
            print('Enter: Id, password')
            while(True):
                login_values = request_input() #TODO: Should not show password
                if login_values[0] == "back":
                    return False, None, None

                if len(login_values) == 2:
                    # Attempt to login
                    login_success = db.login(
                        login_values[0], login_values[1]
                    )
                    if login_success:
                        # Check if user is privileged
                        is_privileged = db.check_privilege(login_values[0])
                        return True, login_values[0], login_values[1]
                    else:
                        print("Login failed, please try again")
                else:
                    print_invalid_input()


        #Sign up
        elif action == '2':
            print("To return to main screen enter `back`")
            print('Enter: Id, Name, City, Password')
            while(True):
                sign_up_values = request_input() #TODO: Should not show password
                if sign_up_values[0] == "back":
                    return False, None, None

                if len(sign_up_values) == 4:
                    # Attempt to sign up
                    sign_up_success = db.sign_up(
                        sign_up_values[0],
                        sign_up_values[1],
                        sign_up_values[2],
                        sign_up_values[3]
                    )

                    if sign_up_success:
                        return True, sign_up_values[0], sign_up_values[3]
                    else:
                        print("Sign up failed, please try again")
                else:
                    print_invalid_input()
        else:
            print_invalid_option()


if __name__ == '__main__':
    db_name = argv[1]
    is_connected = db.connect(db_name)

    while(is_connected):
        is_logged_in, uid, pwd = login()
        if is_logged_in:
            logged_in(uid, pwd)
