import database as db

from utils import (
    request_input,
    print_invalid_input,
    print_invalid_option,
    get_max_min_index,
    is_index
)

def logged_in(uid, pwd, is_privilege):
    print('Now logged in, to log out type `logout`')

    while(True):
        print('Enter:')
        print('1 for Post a question')
        print('2 for Search posts')

        action = request_input()[0]

        if (action == "logout"):
            break

        # Post a Question
        elif (action == "1"):
            print("Post Question")
            title_text = input("Enter title: ")
            body_text = input("Enter body: ")
            post_success = db.post_question(title_text, body_text, uid)
            if post_success:
                print("Question successfully posted")
            else:
                print("Question failed to post")

            print('')

        # Search for posts
        elif (action == "2"):
            print("Enter keywords separated by a comma")
            keywords = request_input()
            results = db.search_posts(keywords)

            selected_index = -1
            i = 0
            print("Showing Results for keywords: " + str(keywords))
            print("Enter the index of the post excute action on that post")
            print('')

            min_i, max_i = get_max_min_index(results=results)
            print("index, pid, pdate, title, body, poster, keyword count, vote count, answer count")
            while(selected_index == -1):
                for row in results[min_i:max_i]:
                    str_ = ("{}: {}, {}, {}, {}, {}, {}, {}, {}").format(
                        i, row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]
                    )
                    print(str_)
                    i += 1
                print('')

                action = request_input()[0]
                if action == "more":
                    # Increment the min and max
                    min_i, max_i = get_max_min_index(
                        results=results,
                        old_min=min_i,
                        old_max= max_i
                    )
                elif is_index(action, results):
                    selected_index = int(action)
                else:
                    print_invalid_input()

            while(True):
                # Now have a post, can act on that post
                post = results[selected_index]
                pid = post[0]

                # We can check if that post was a question by checking answer count
                # (answer count is None if answer)
                is_question = True if post[7] is not None else False

                print('Selected post pid is:' + pid)
                print('To go back type `back`')
                print('')


                # Actions on a post
                if is_question:
                    print('3 for Post action-answer')
                print('4 for Post action-vote')
                if is_privilege:
                    print('Privileged Actions:')
                    print('5 for Post action-mark as accepted')
                    print('6 for Post action-give a badge')
                    print('7 for Post post action-add a tag')
                    print('8 for Post action-edit')

                action = request_input()[0]

                if (action == "back"):
                    break

                # Post action-answer
                elif (action == "3") and is_question:
                    print("Post Answer")
                    title_text = input("Enter title: ")
                    body_text = input("Enter body: ")
                    post_success = db.post_answer(title_text, body_text, uid, pid)
                    if post_success:
                        print("Answer successfully posted")
                    else:
                        print("Answer failed to post")

                    print('')

                # Post action-vote
                elif (action == "4"):
                    vote_success = db.post_vote(pid, uid)

                    if vote_success:
                        print("Vote successfully posted")
                    else:
                        print("Vote failed to post")
                    print('')

                # Post action-mark as accepted
                elif (action == "5") and is_privilege and not is_question:
                    question = db.get_question_of_answer(pid)

                    should_mark_accepted = True
                    if question is not None:
                        action = "1"
                        if question[1] is not None:
                            print('Replace current accepted answer?')
                            print('0 No')
                            print('1 Yes')
                            print('')

                            action = request_input()[0]

                        if action == "0":
                            print("The answer will not be marked as accepted")
                            should_mark_accepted = False
                    else:
                        print('Failed to mark the answer as accepted')
                        should_mark_accepted = False

                    if should_mark_accepted:
                        mark_accepted_success = db.mark_accepted(pid, question[0])

                        if mark_accepted_success:
                            print('The answer was marked accepted successfully')
                        else:
                            print('Failed to mark the answer as accepted')
                    print('')

                # Post action-give a badge
                elif (action == "6") and is_privilege:
                    pass

                # Post post action-add a tag
                elif (action == "7") and is_privilege:
                    pass

                # Post action-edit:
                elif (action == "8") and is_privilege:
                    pass

                else:
                    print_invalid_option()

        # Invalid selection
        else:
            print_invalid_option()