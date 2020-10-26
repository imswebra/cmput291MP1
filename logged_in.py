import database as db

from utils import (
    request_input,
    print_invalid_input,
    print_invalid_option
)

def logged_in(uid, pwd, is_privilege):
    print('Now logged in, to log out type `logout`')

    while(True):
        print('Enter:')
        print('1 for Post a question')
        print('2 for Search posts')
        print('3 for Post action-answer')
        print('4 for Post action-vote')
        if is_privilege:
            print('Privileged Actions:')
            print('5 for Post action-mark as accepted')
            print('6 for Post action-give a badge')
            print('7 for Post post action-add a tag')
            print('8 for Post action-edit')

        #TODO: I realized after reading the actions that
        # its not gonna be a menu like this (just 1 and 2)
        # and then 2 will have a bunch more

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
            print("Enter keywords separated by a comma")
            keywords = request_input()
            results = db.search_posts(keywords)
            print(results)

        # Post action-answer
        elif (action == "3"):
            pass

        # Post action-vote
        elif (action == "4"):
            pass

        # Post action-mark as accepted
        elif (action == "5"):
            pass

        # Post action-give a badge
        elif (action == "6"):
            pass

        # Post post action-add a tag
        elif (action == "7"):
            pass

        #Post action-edit:
        elif (action == "8"):
            pass

        # Invalid selection
        else:
            print_invalid_option()