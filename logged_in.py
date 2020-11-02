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


def print_search_results(results, min_i, max_i):
    print("index, pid, pdate, title, body, poster, keyword count, vote count, answer count")
    for i, row in enumerate(results[min_i:max_i], min_i):
        print(("{}: {}, {}, {}, {}, {}, {}, {}, {}").format(i, *row))
    print("")


def post_action(post):
    # Get post info
    pid = post[0]
    # Checking answer count to determine post type
    is_question = True if post[7] is not None else False

    # Setup post action options
    pa_actions = ["Answer question", "Vote on post",
                  "Mark answer as accepted", "Give poster a badge",
                  "Add tag to post", "Edit post"]
    skip_actions = pa_actions[2:] if not is_privileged else []
    if is_question:
        skip_actions.append(pa_actions[2])
    else:
        skip_actions.append(pa_actions[0])

    while(True):
        print("Selected post pid is:", pid)
        print("To go back, type `back`")
        print_options(pa_actions, skip_actions)
        action = request_input()[0]

        if action == "back":
            return False
        elif action == "logout":
            return True
        # Post action-answer
        elif (action == "1") and is_question:
            post_answer(pid)
        # Post action-vote
        elif (action == "2"):
            post_vote(pid)
        # Post action-mark as accepted
        elif (action == "3") and is_privileged and not is_question:
            mark_as_accepted(pid)
        # Post action-give a badge
        elif (action == "4") and is_privileged:
            logout = give_badge(post[4])
            if logout:
                return True
        # Post post action-add a tag
        elif (action == "5") and is_privileged:
            add_tag(pid)
        # Post action-edit:
        elif (action == "6") and is_privileged:
            edit_post(pid)
        # Invalid selection
        else:
            print_invalid_option()
        print("")


def post_answer(pid):
    print("Post Answer")
    title_text = input("Enter title: ")
    body_text = input("Enter body: ")
    post_success = db.post_answer(title_text, body_text, uid, pid)
    if post_success:
        print("Answer successfully posted")
    else:
        print("Answer failed to post")


def post_vote(pid):
    vote_success = db.post_vote(pid, uid)
    if vote_success:
        print("Vote successfully posted")
    else:
        print("Vote failed to post")


def mark_as_accepted(pid):
    question = db.get_question_of_answer(pid)
    if question is None:
        print("Failed to find the question of this answer")
        return

    if question[1] is not None:
        if question[1] == pid:
            print("This answer is already marked as accepted")
            return

        print("Mark answer as accepted")
        print("The answer's question already has an accepted answer.")
        print_options(["Cancel and go back", "Replace current accepted answer"])
        while True:
            action = request_input()[0]
            if action == "1":
                print("The operation was cancelled")
                return
            elif action == "2":
                break
            else:
                print_invalid_option(2)

    mark_accepted_success = db.mark_accepted(pid, question[0])
    if mark_accepted_success:
        print("The answer was successfully marked as accepted")
    else:
        print("Failed to mark the answer as accepted")


def give_badge(poster_uid):
    results = db.get_badges()
    if results is None:
        print("Failed to retrieve list of badges")
        return

    print("Give poster a badge")
    print("Choose a badge to give to the user:")
    print("To go back, type `back`")
    min_i, max_i = get_min_max_index(results=results)
    print("")
    print_badges(results, min_i, max_i)

    # Select badge
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
            print_badges(results, min_i, max_i)
        elif action == "back":
            return False
        elif action == "logout":
            return True
        elif is_index(action, results):
            break
        else:
            print_invalid_option(max_option=len(results))

    give_badge_success = db.give_badge(poster_uid, results[int(action)][0])
    if give_badge_success:
        print("The badge was successfully given to the poster")
    else:
        print("Failed to give the badge to the poster")
    return False


def print_badges(results, min_i, max_i):
    print("index, name, type")
    for i, row in enumerate(results[min_i:max_i], min_i):
        print(("{}: {}, {}").format(i, *row))
    print("")


def add_tag(pid):
    print('Add tag')
    tag = input('Enter a tag: ')
    add_tag_success = db.add_tag(pid, tag)

    if add_tag_success:
        print("Successfully added a tag")
    else:
        print("Failed to add a tag")


def edit_post(pid):
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
