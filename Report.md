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

## Software Design
> **TODO:** Update this as needed after refactors/filename changes\
> **TODO:** I feel like this needs more?

`main.py` handles the CLI arugments, and has only three other responsibilities: Initialize the database connection (via `database.py`), run the login routine (from `login.py`) and pass the user information to `logged_in.py`.

`login.py` contains code for the login routine, with it's main high level function being `login_or_signup()`. This function prompts the user and runs the appropriate sub-function for either action.

`logged_in.py` contains the code for the main functionality of the program. `logged_in()` is the highest level function that prompts between posting a question and searching for a post. These each have their own subfunctions (`post_question()` and `search_select_posts()`), and after a sucessful search and selection, the selected post pid is passed to the `post_action()` function. This function allows the user to select post-actions, all of which also have their own subfunctions. This nesting subfunction structure follows what would be expected from a menu structure for this program, and thus it facilitates the code for moving back up the menu tree.

`database.py` is somewhat standalone in contrast. It contains and abstracts away all of the SQL interaction code, and is thus referenced at all levels of the code. For the most part, the functions defined in this file have equivalents in `login.py` and `logged_in.py`; While those handle user input, errors, printing, and the navigation structure, the equivalents in `database.py` contain strictly the SQL calls, with some of the error handling being passed back up to the calling function. Examples of those equivalents are `login()`, `sign_up()`, `post_question()`, `search_posts()`, and all the various post-action functions.

`utils.py` is the only other python file, and just contains helper utility functions.

## Differences in Design from Specification
1. The specification document says that for the "give a badge" post-action, the user must provide a badge name. The marking rubric later clarifies that this badge name must be valid in the sense that it already exists in badges table. Instead of taking a text input for this post-action, we opted to allow the user to select a badge from a list for an improved user-experience. This is implemented and functions much in the same way as selecting from search results.

## Testing Strategy
> **TODO:** Make tests, fill out this section

>The testing strategy discusses your general strategy for testing, with the scenarios being tested, the coverage of your test cases and (if applicable) some statistics on the number of bugs found and the nature of those bugs.

## Group Work Strategy
The group work strategy between all the members was fairly loose and relaxed. We didn't formally split up the work into three sections; Generally, the team members worked on the project as they had time, just working on what needed to be done at the time. We communicated and coordinated regularly as we each made updates to the project.

### Member estimates and tasks
> **TODO:** Update this once everything has been finalized\
> **TODO:** Make repo public after submission deadline has passed

The full commit log can be viewed [here](https://github.com/imswebra/cmput291MP1/commits/master).

#### Mitchell
Time Estimate:

Tasks:
- Building the initial program structure
- Initial implementation of many of the required features:
    - Sign-up and login process
    - Post question, post answer post-action
    - Search
    - Vote post-action

#### Nayan
Time Estimate:

Tasks:
- Initial implementation of many of the required features:
    - Mark as accepted post-action
    - Add tag post-action
    - Edit post post-action

#### Eric
Time Estimate: ~12 hours

Tasks:
- Implementing the give a badge post-action
- Large code refactors, general code quality improvements
- Implementing/improving the menu and code flow with back and logout
- General product polish (User friendly prompts, visual consistency, error messages with usage hints, QoL improvements)
- Manual testing, bug fixing
- Writing design document
