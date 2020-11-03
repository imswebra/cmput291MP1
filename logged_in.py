import database as db

from utils import (
    request_input,
    keyword_input_validate,
    print_options,
    print_invalid_option,
    get_indices_range,
    get_table_info,
    print_table,
    is_index
)


uid = None
is_privileged = None


def logged_in(uid_param, is_privileged_param):
    global uid
    uid = uid_param
    global is_privileged
    is_privileged = is_privileged_param

    print("Now logged in. To log out, type `/logout` at anytime.")
    print("In any submenu or input, type `/back` to return up a level.")
    while (True):
        print_options(["Post a question", "Search posts"])

        action = request_input()[0]

        logout = None
        if action == "/back":
            print("Already at the top-level menu. To logout, type `/logout`.")
        elif (action == "/logout"):
            logout = True
        # Post a Question
        elif (action == "1"):
            logout = post_question()
            print("")
        # Search for posts
        elif (action == "2"):
            post, logout = search_select_posts()
            if not logout and post is not None:
                logout = post_action(post)
        # Invalid selection
        else:
            print_invalid_option(max_option=2)

        if logout:
            return


def post_question():
    print("Post Question")
    title_text = input("Enter title: ")
    to_return, return_val = keyword_input_validate(title_text)
    if to_return:
        return return_val

    body_text = input("Enter body: ")
    to_return, return_val = keyword_input_validate(body_text)
    if to_return:
        return return_val

    post_success = db.post_question(title_text, body_text, uid)
    if post_success:
        print("Question successfully posted")
    else:
        print("Question failed to post")


def search_select_posts():
    # Search posts
    while (True):
        print("Enter keywords separated by a comma:")
        keywords = request_input()
        if keywords[0] == "/back":
            return None, False
        elif keywords[0] == "/logout":
            return None, True

        results = db.search_posts(keywords)
        if len(results) > 0:
            break
        print("No results found for keywords:", str(keywords), "\n")
        continue

    # List results
    print("Showing results for keywords", str(keywords))
    print("Enter the index of the post to excute an action on that post:")
    min_i, max_i = get_indices_range(results=results)
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
            min_i, max_i = get_indices_range(
                results=results,
                old_min=min_i,
                old_max=max_i
            )
            print_search_results(results, min_i, max_i)
        elif action == "/back":
            return None, False
        elif action == "/logout":
            return None, True
        elif is_index(action, results):
            # Note: User input index starts at 1
            return results[int(action) - 1], False
        else:
            print_invalid_option(max_option=len(results))


def print_search_results(results, min_i, max_i):
    # Get table
    max_widths = {2: 20, 3: 30}  # title and body (index 2 and 3) before index
    header = ["i", "pid", "pdate", "title", "body", "poster",
              "# keywords", "votes", "answers"]
    table, widths = get_table_info(results[min_i:max_i], header,
                                   trunc_widths=max_widths,
                                   index_start=min_i + 1)  # Start indices at 1

    # Generate width string
    # Right-aligned index, 5 left-aligned columns, 3 right-aligned columns
    width_str = "{{:>{}}}  " + "{{:{}}}  " * 5 + "{{:>{}}}  " * 2 + "{{:>{}}}"
    width_str = width_str.format(*widths)

    # Print the table
    print_table(table, width_str, widths)
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
        print_options(pa_actions, skip_actions)
        action = request_input()[0]

        logout = None
        if action == "/back":
            return
        elif action == "/logout":
            logout = True
        # Post action-answer
        elif (action == "1") and is_question:
            logout = post_answer(pid)
        # Post action-vote
        elif (action == "2"):
            post_vote(pid)
        # Post action-mark as accepted
        elif (action == "3") and is_privileged and not is_question:
            logout = mark_as_accepted(pid)
        # Post action-give a badge
        elif (action == "4") and is_privileged:
            logout = give_badge(post[4])
            if logout:
                return True
        # Post post action-add a tag
        elif (action == "5") and is_privileged:
            logout = add_tag(pid)
        # Post action-edit:
        elif (action == "6") and is_privileged:
            logout = edit_post(pid)
        # Invalid selection
        else:
            print_invalid_option()

        if logout:  # Either True, False or None
            return True
        print("")


def post_answer(pid):
    print("Post Answer")
    title_text = input("Enter title: ")
    to_return, return_val = keyword_input_validate(title_text)
    if to_return:
        return return_val

    body_text = input("Enter body: ")
    to_return, return_val = keyword_input_validate(body_text)
    if to_return:
        return return_val

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
            if action == "/logout":
                return True
            if action == "1" or action == "/back":
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
    min_i, max_i = get_indices_range(results=results)
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
            min_i, max_i = get_indices_range(
                results=results,
                old_min=min_i,
                old_max=max_i
            )
            print_badges(results, min_i, max_i)
        elif action == "/back":
            return
        elif action == "/logout":
            return True
        elif is_index(action, results):
            break
        else:
            print_invalid_option(max_option=len(results))

    # Note: User input index starts at 1
    give_badge_success = db.give_badge(poster_uid, results[int(action) - 1][0])
    if give_badge_success:
        print("The badge was successfully given to the poster")
    else:
        print("Failed to give the badge to the poster")


def print_badges(results, min_i, max_i):
    # Get table
    header = ["i", "name", "type"]
    table, widths = get_table_info(results[min_i:max_i], header,
                                   index_start=min_i + 1)  # Start indices at 1

    # Print the table
    width_str = "{{:>{}}}  {{:{}}}  {{:{}}}".format(*widths)
    print_table(table, width_str, widths)
    print("")


def add_tag(pid):
    print('Add tag')
    tag = input('Enter a tag: ')
    to_return, return_val = keyword_input_validate(tag)
    if to_return:
        return return_val

    add_tag_success = db.add_tag(pid, tag)
    if add_tag_success:
        print("Tag successfully added")
    else:
        print("Failed to add a tag")


def edit_post(pid):
    print('Edit the title and/or body of a post')

    title = ""
    body = ""
    while title == "" and body == "":
        title = input('Enter new title (leave blank to keep old title): ')
        to_return, return_val = keyword_input_validate(title)
        if to_return:
            return return_val

        body = input('Enter new body (leave blank to keep old body): ')
        to_return, return_val = keyword_input_validate(title)
        if to_return:
            return return_val

        if title == "" and body == "":
            print("At least one of title or body must be entered")
        print('')

    edit_post_success = db.edit_post(pid, title, body)

    if edit_post_success:
        print("Successfully editted the post")
    else:
        print("Failed to edit the post")
