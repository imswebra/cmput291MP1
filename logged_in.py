import database as db

from utils import (
    request_input,
    print_options,
    print_invalid_option,
    get_min_max_index,
    is_index
)


uid = None
is_privileged = None


def logged_in(uid_param, is_privileged_param):
    global uid
    uid = uid_param
    global is_privileged
    is_privileged = is_privileged_param

    print('Now logged in. To log out, type `logout` at anytime.')
    while (True):
        print_options(["Post a question", "Search posts"])

        action = request_input()[0]

        if (action == "logout"):
            return
        # Post a Question
        elif (action == "1"):
            post_question()
        # Search for posts
        elif (action == "2"):
            post, logout = search_select_posts()
            if logout:
                return
            if post is None:  # Back was used
                continue
            logout = post_action(post)
            if logout:
                return
        # Invalid selection
        else:
            print_invalid_option(max_option=2)


def post_question():
    print("Post Question")
    title_text = input("Enter title: ")
    body_text = input("Enter body: ")
    post_success = db.post_question(title_text, body_text, uid)
    if post_success:
        print("Question successfully posted")
    else:
        print("Question failed to post")
    print("")


def search_select_posts():
    # Search posts
    while (True):
        print("Enter keywords separated by a comma:")
        keywords = request_input()
        results = db.search_posts(keywords)

        # TODO: Handle back/logout here? Would limit keywords in the search but
        # we are handling exit, should we be consistent?

        if len(results) > 0:
            break
        print("No results found for keywords:", str(keywords), "\n")
        continue

    # List results
    print("Showing results for keywords", str(keywords))
    print("To go back, type `back`")
    print("Enter the index of the post to excute an action on that post:")
    min_i, max_i = get_min_max_index(results=results)
    print("")
    print_search_results(results, min_i, max_i)

    # Select posts
    while (True):
        action = request_input()[0]

        if action == "more":
            if len(results) <= max_i:
                print("No more results are available")
                continue

            # Increment the min and max
            min_i, max_i = get_min_max_index(
                results=results,
                old_min=min_i,
                old_max=max_i
            )
            print_search_results(results, min_i, max_i)
        elif action == "back":
            # Should go to main menu (post/search selection). If "continue"
            # is used, user will go back to keyword input and will be stuck
            return None, False
        elif action == "logout":
            return None, True
        elif is_index(action, results):
            return results[int(action)], False
        else:
            print_invalid_option(max_option=len(results))


def post_action(post):  # TODO: Refactor this
    while(True):
        # Now have a post, can act on that post
        pid = post[0]

        # We can check if that post was a question by checking answer count
        # (answer count is None if answer)
        is_question = True if post[7] is not None else False

        print("Selected post pid is:", pid)
        print("To go back, type `back`")

        pa_actions = ["Answer question", "Vote on post",
                      "Mark answer as accepted", "Give poster a badge",
                      "Add tag to post", "Edit post"]
        skip_actions = pa_actions[2:] if not is_privileged else []
        if is_question:
            skip_actions.append(pa_actions[2])
        else:
            skip_actions.append(pa_actions[0])
        print_options(pa_actions, skip_actions)

        action = request_input()[0]

        if action == "back":
            return False
        elif action == "logout":
            return True

        # Post action-answer
        elif (action == "1") and is_question:
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
        elif (action == "2"):
            vote_success = db.post_vote(pid, uid)

            if vote_success:
                print("Vote successfully posted")
            else:
                print("Vote failed to post")
            print('')

        # Post action-mark as accepted
        elif (action == "3") and is_privileged and not is_question:
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
        elif (action == "4") and is_privileged:
            pass

        # Post post action-add a tag
        elif (action == "5") and is_privileged:
            print('Add tag')
            tag = input('Enter a tag: ')
            add_tag_success = db.add_tag(pid, tag)

            if add_tag_success:
                print("Successfully added a tag")
            else:
                print("Failed to add a tag")
            print('')

        # Post action-edit:
        elif (action == "6") and is_privileged:
            print('Edit the title and/or body of a post')

            title = ""
            body = ""
            while title == "" and body == "":
                title = input('Enter new title (leave blank to keep old title): ')
                body = input('Enter new body (leave blank to keep old body): ')

                if title == "" and body == "":
                    print('Atleast one of title and body must be entered')
                print('')

            edit_post_success = db.edit_post(pid, title, body)

            if edit_post_success:
                print("Successfully editted the post")
            else:
                print("Failed to edit the post")
            print('')

        else:
            print_invalid_option()


def print_search_results(results, min_i, max_i):
    print("index, pid, pdate, title, body, poster, keyword count, vote count, answer count")
    for i, row in enumerate(results[min_i:max_i], min_i):
        print(("{}: {}, {}, {}, {}, {}, {}, {}, {}").format(i, *row))
    print("")
