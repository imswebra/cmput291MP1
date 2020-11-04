> I know this is markdown and not PDF. I'll convert it to PDF before submission - Eric

# CMPUT 291 Mini Project 1
Group Members:
- Mitchell Adam - `mbadam`
- Nayan Prakash - `nayan`
- Eric Claerhout - `claerhou`

## System Overview
The system was implemented in Python without any external libraries, and uses a CLI interface for user interaction.

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

At each of the end-points in this high-level flow, a call to a function in `database.py` allows us to insert into, query, or otherwise interact with the database. Because of this, the flow above more closely describes the flow of user interaction of the program.

> The general overview of the system gives a high level introduction and may include a diagram showing the flow of data between different components; this can be useful for both users and developers of your application.

### User Guide
1. Initialize the database with `sqlite3 $DATABASE_NAME.db <sql/tables.sql`
2. If you wish you populate the database with a dataset do `sqlite3 $DATABASE_NAME.db <sql/$DATASET_NAME.sql`
3. Run the program with `python3 main.py $DATABASE_NAME.db`
4. From here, the program will prompt the user for input, allowing the user to execute the desired functionality of the program. Any changes made to the database through the program will be reflected in `$DATABASE_NAME.db`
5. At any point in the program's execution where input is requested, `/exit` can be used to quit the program and `/back` can be used to return to a previous menu. Once logged-in, `/logout` can be also be used at any point to return to the login/sign-up menu.

## Software Design
`main.py` handles the CLI arugments, and has only three other responsibilities: Initialize the database connection (via `database.py`), run the login routine (from `login.py`) and, after validation, pass the user information to the main execution loop of `logged_in.py`.

`login.py` contains code for the login routine, with it's main high level function being `login_or_signup()`. This function prompts the user if they would like to either sign-up or login, and upon receiving user input, directs the user to either the `login()` or `signup()` sub-function. The `login()` sub-function prompts the user for the required login details and then makes a call to the `login()` function within `database.py`. After a successful login, this sub-function will also check if the logged-in user is a privileged user by making a call to the `check_privilege()` function within `database.py`. Similarly, the `signup()` sub-function prompts the user for the required sign-up information and then makes a call to the `sign_up()` function within `database.py`.

`logged_in.py` contains the code for the main execution loop of the program. `logged_in()` is the highest level function that prompts the user to either post a question or search for a post, and accordingly calls the appropriate subfunction (`post_question()` or `search_select_posts()`). After a question is posted, the user is returned to this top-level menu, but after a successful search and selection, the selected post pid is passed to the `post_action()` function. This function allows the user to select post-actions, all of which also have their own subfunctions. This nesting subfunction structure follows what would be expected from a menu structure for this program, and thus it facilitates allowing the code to move back up the menu tree.

`database.py` is somewhat standalone in contrast. It contains and abstracts away all of the SQL interaction code, and is thus referenced at all levels of the program. For the most part, the functions defined in this file have equivalents in `login.py` and `logged_in.py`; While those handle user input, errors, printing, and the navigation structure, the equivalents in `database.py` contain strictly the SQL calls, with some of the error handling being passed back up to the calling function. Examples of those equivalents are `login()`, `sign_up()`, `post_question()`, `search_posts()`, and all the various post-action functions.

`utils.py` is the only other python file, and contains helper utility functions. These functions are used for tasks such as input parsing, error messaging and print formatting. This allows easy reuse of common functionality, keeping other files clean.

## Differences in Design from Specification
1. The specification document says that for the "give a badge" post-action, the user must provide a badge name. The marking rubric later clarifies that this badge name must be valid in the sense that it already exists in badges table. Instead of taking a text input for this post-action, we opted to allow the user to select a badge from a list for an improved user-experience. This is implemented and functions much in the same way as selecting from search results.

## Testing Strategy
The testing strategy consisted of a combination of both unit tests for several of the key, low-level functions (namely functions within `database.py` and `utils.py`) as well as extensive manual testing for the higher-level areas that were frequently changed or had a high-likelihood of failure.

Unit tests were implemented to ensure that the low-level functions operated as expected. Given their frequent use by the higher-level functions, this automated testing was incredibly important. The collection of unit tests is contained within the `tests/` directory, and tests can be run by calling `python3 -m unittest tests/$TEST_SUITE.py` from the root directory. The test cases within `database_test.py` test the execution of many functions within `database.py`. The test cases within `utils_test.py` test the some of the helper functions of `utils.py`, with a focus on
the functions that perform validation and string manupilation. Many of the functions within `utils.py` were better suited for manual testing, as they either take user input or they pretty-print data.

The following unit test cases were developed:

Database Tests:
- test_count_keywords: ensure keywords are counted correctly
- test_connect: ensure connection to the DB
- test_generate_unique_key: ensure unique key is generated
- test_sign_up: ensure ability to sign up
- test_login: ensure ability to login
- test_check_privilege: ensure correct access of privileged users
- test_post_question: ensure ability to post new questions
- test_search_posts: ensure correct posts are returned upon search
- test_post_answer: ensure ability to post new answers
- test_post_vote: ensure ability to vote on posts
- test_get_question_of_answer: ensure correct question is returned
- test_mark_accepted: ensure ability to mark answers as accepted
- test_get_badges: ensure correct badges are returned
- test_give_badge: ensure ability to give a user a badge
- test_add_tag: ensure ability to give a post a new tag
- test_edit_post: ensure ability to edit the title and body of a post
- test_case_insensitive_tag: ensure that tags are case insensitive

Utility Function Tests:
- test_split_and_strip: ensure that input is correctly parsed and striped
- test_keyword_input_validate: ensure that navigation keywords work
- test_get_indices_range: ensure that max 5 posts are shown at time
- test_stringify: ensure correct conversion to string
- test_is_index: ensure ability to identify out of range selections

The strategy employed to execute manual testing was to heavily test the most common areas for failure, such as user input and SQL queries. Schema and data files were developed for manual testing. An SQL database was created with data that specifically addressed the project requirements and corresponding edge cases. This allowed for quick and easy testing during development. It was also easy to quickly add new data to the database as further testing was required. Additionally, SQL queries were tested outside of the python programming environment. This allowed us to test that the queries returned results that were expected. After ensuring that the queries returned the expected values, we then implemented these queries into our program which ensured that we were querying for the correct data.

Because our testing strategy took place throughout the development process, bugs were found and then fixed incrementally. While this did not allow us to discover bugs in large batches and provide statistics about the bugs that were discovered, it allowed us to fix bugs as they arose. This was important to us, because many of our functions, especially the low-level functions, form the basis of functionality for higher-level functions and ensuring that these functions were bug-free allowed us to continue development on the higher-level functions without being blocked.

## Group Work Strategy
Our group began work on the project two weeks before the deadline. At this time, each member of the team began to familiarize themselves with the project and began to understand what was required. As members began to work, they would update the other members on what had been accomplished and what was the next item on the TODO list. To ensure even splitting of the work, members would request that certain features were left for them to implement. In this way, members were able to work on the project when they had time to do so without worrying about not contributing. The group members would consistently keep a tally of what work was completed and what work was still required to implement, and group members were able to choose tasks to whittle down the necessary work. Once a sizeable portion of the product had been done, a TODO list was started on what was needed to finalize the project. At this time, each member volunteered to work on a few of the "clean up" tasks that were required.

As our group was not able to meet in person to work on this project, we had a group chat made to ensure constant communication between members. Members were able to keep each other up-to-date on what had been completed and what was still left to be done. Members were could also consult the group when they found a task to be difficult and needed assistance. This allowed members to work individually, but collaborate if needed. As well, it ensured that the program that was developed matched the requirements and expectations of each member.

In order to ensure all requirements were met, lists of tasks were made by directly consulting the requirements. This allowed us to stay organized and address the needed features of the projects.

In order to not miss any clarifications, we also copied all the clarifications into our todo list so that we could change our previous work if needed and could easily see the clarifications for new work

Overall, our group maintained good communication throughout the project with members volunteering on what aspects they wanted to work on. All members were eager to contribute and the dynamics of the team were positive.

### Member estimates and tasks
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
    - Handle privileged users
- Report additions

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
- Database and utility test cases
- Execution of manual testing
- Additions to design document

#### Eric
Time Estimate: ~12 hours

Tasks:
- Implementing the give a badge post-action
- Large code refactors, general code quality improvements
- Implementing/improving the menu and code flow with back and logout
- General product polish (User friendly prompts, visual consistency, error messages with usage hints, QoL improvements)
- Manual testing, bug fixing
- Writing design document
