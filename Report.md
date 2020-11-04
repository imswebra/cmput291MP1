> I know this is markdown and not PDF. I'll convert it to PDF before submission - Eric

# CMPUT 291 Mini Project 1
Group Members:
- Mitchell Adam - `mbadam`
- Nayan Prakash - `nayan`
- Eric Claerhout - `claerhou`

## System Overview
> **TODO:** Update this as needed after refactors/filename changes\
> **TODO:** Finish this
Implemented in Python, CLI interface

General, high-level flow:
```
0. Initalization
1. main <-> login.login_or_signup()
2. main -> logged_in.logged_in()
3a. logged_in.logged_in() -> logged_in.post_question()
3b. logged_in.logged_in() <-> logged_in.search_select_posts()
    4. logged_in.logged_in() -> logged_in.post_action()
    5. logged_in.post_action() -> Individual post action functions
```

> The general overview of the system gives a high level introduction and may include a diagram showing the flow of data between different components; this can be useful for both users and developers of your application.

### User Guide
1. Initialize the database with `sqlite3 $DATABASE_NAME.db <sql/tables.sql`
2. If you wish you populate the database with a dataset do `sqlite3 $DATABASE_NAME.db <sql/$DATASET_NAME.sql`
3. Run the program with `python3 main.py $DATABASE_NAME.db`
4. From here, the program will prompt the user for input, allowing the user to execute the desired functionality of the program. Any changes made to the database through the program will be reflected in `$DATABASE_NAME.db`
5. At any point in the program's execution, `/exit` can be used to quit the program

## Software Design
> **TODO:** Update this as needed after refactors/filename changes\
> **TODO:** I feel like this needs more?

`main.py` handles the CLI arugments, and has only three other responsibilities: Initialize the database connection (via `database.py`), run the login routine (from `login.py`) and, after validation, pass the user information to the main execution loop of `logged_in.py`.

`login.py` contains code for the login routine, with it's main high level function being `login_or_signup()`. This function prompts the user if they would like to either signup or login and upon receiving user input, directs the user to either the `login()` or `signup()` sub-function. The `login()` sub-function prompts the user for the required login function and then makes a call to `login()` function within `database.py`. After a successful login, this sub-function will check if the logged in user is a privileged user by making a call to the `check_privilege()` function within `database.py`. Similarly, the `signup()` sub-function prompts the user for the required signup information and then makes a call to `sign_up()` function within `database.py`.

`logged_in.py` contains the code for the main execution loop of the program. `logged_in()` is the highest level function that prompts the user to either post a question or search for a post. These each have their own subfunctions (`post_question()` and `search_select_posts()`), and after a successful search and selection, the selected post pid is passed to the `post_action()` function. This function allows the user to select post-actions, all of which also have their own subfunctions. This nesting subfunction structure follows what would be expected from a menu structure for this program, and thus it facilitates the code for moving back up the menu tree.

`database.py` is somewhat standalone in contrast. It contains and abstracts away all of the SQL interaction code, and is thus referenced at all levels of the code. For the most part, the functions defined in this file have equivalents in `login.py` and `logged_in.py`; While those handle user input, errors, printing, and the navigation structure, the equivalents in `database.py` contain strictly the SQL calls, with some of the error handling being passed back up to the calling function. Examples of those equivalents are `login()`, `sign_up()`, `post_question()`, `search_posts()`, and all the various post-action functions.

`utils.py` is the only other python file, and contains helper utility functions.

## Differences in Design from Specification
1. The specification document says that for the "give a badge" post-action, the user must provide a badge name. The marking rubric later clarifies that this badge name must be valid in the sense that it already exists in badges table. Instead of taking a text input for this post-action, we opted to allow the user to select a badge from a list for an improved user-experience. This is implemented and functions much in the same way as selecting from search results.

## Testing Strategy
The testing strategy consisted of a combination of both unit tests for several of the key, low-level functions (namely functions within `database.py` and `utils.py`) as well as manual testing for areas that were frequently changed or had a high-likelihood of failure.

The unit tests were implemented to ensure that the low-level functions operated as expected. This was important because many of the higher-level functions relied on the proper execution of these low-level functions. The collection of unit tests is contained within `tests/` and tests can be run by calling `python3 -m unittest tests/$TEST_SUITE.py`. The test cases within `database_test.py` test the execution of many functions within `database.py`. Testing of functions within `database.py` that insert into the database was difficult and because of the difficulty to verify the underlying data after function calls, these functions were often extensively tested through manual testing instead of unit tests. The test cases within `utils_test.py` test the helper functions of `utils.py` that are utilized by many of the other functions of the program. Despite this, many of the functions within `utils.py` are used to print data in a readable manner and these functions were tested manually. Similarly, several functions within `utils.py` accept user input and validate the input and these functions were tested using manual testing.

The strategy employed to execute manual testing was to heavily test the most common areas for failure, such as user-input and SQL queries. The following test cases were developed.

Database Tests:
- test_count_keywords: ensure keywords are counted correctly
- test_connect: ensure connection to the DB
- test_generate_unique_key: ensure unique key is generated
- test_sign_up: ensure ability to sign up
- test_login: ensure ability to login
- test_check_privilege: ensure correct access of privileged users
- test_search_posts: ensure correct posts are returned upon search
- test_get_question_of_answer: ensure correct question is returned
- test_get_badges: ensure correct badges are returned
- test_case_insensitive_tag: ensure that tags are case insensitive

Additional Tests:
- test_split_and_strip: ensure that input is correctly parsed and striped
- test_keyword_input_validate: ensure that navigation keywords work
- test_get_indices_range: ensure that max 5 posts are shown at time
- test_stringify: ensure correct conversion to string
- test_is_index: ensure ability to identify out of range selections

>The testing strategy discusses your general strategy for testing, with the scenarios being tested, the coverage of your test cases and (if applicable) some statistics on the number of bugs found and the nature of those bugs.

## Group Work Strategy
The group work strategy between all the members was fairly loose and relaxed. We didn't formally split up the work into three sections; Generally, the team members worked on the project as they had time, working on what needed to be done at the time. We communicated and coordinated regularly as we each made updates to the project. The group members would consistently keep a tally of what work was completed and what work was still required to implement and group members were able to choose tasks to whittle down the necessary work.

### Member estimates and tasks
> **TODO:** Update this once everything has been finalized\
> **TODO:** Make repo public after submission deadline has passed

The full commit log can be viewed [here](https://github.com/imswebra/cmput291MP1/commits/master).

#### Mitchell
Time Estimate: ~10-14 hours

Tasks:
- Building the initial program structure and program flow
- Establish database connection
- Create SQL files for testing
- Develop utility functions
- Develop sql utility functions (generate unique key)
- Hide password
- Exit program
- Initial implementation of many of the required features:
    - Sign-up process
    - Login and logout
    - Search for question by keywords
    - Post a question
    - Vote post-action
    - Post action-Answer
    - Handle prviliged users

#### Nayan
Time Estimate: ~12-14 hours

Tasks:
- Develop sql utility functions (get_question_of_answer, check_has_case_insensitive_entry)
- Initial implementation of many of the required features:
    - Mark as accepted post-action
    - Add tag post-action
    - Edit post post-action
- Various bug fixes across codebase
- Adding of descriptive docstrings to functions
- Implementation of a unit testing framework

#### Eric
Time Estimate: ~12 hours

Tasks:
- Implementing the give a badge post-action
- Large code refactors, general code quality improvements
- Implementing/improving the menu and code flow with back and logout
- General product polish (User friendly prompts, visual consistency, error messages with usage hints, QoL improvements)
- Manual testing, bug fixing
- Writing design document
