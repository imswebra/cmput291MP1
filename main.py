
from sys import argv, exit

import database as db
from logged_in import logged_in
from login import login_or_signup


if __name__ == '__main__':
    if (len(argv) <= 1 or len(argv) > 2):
        print("One database argument expected, received", len(argv) - 1)
        exit(1)

    is_connected = db.connect(argv[1])

    while (is_connected):
        uid, is_privileged = login_or_signup()
        if uid is not None:
            logged_in(uid, is_privileged)
