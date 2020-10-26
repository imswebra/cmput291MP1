
from sys import argv
import database as db

from logged_in import logged_in
from login import login


if __name__ == '__main__':
    db_name = argv[1]
    is_connected = db.connect(db_name)

    while(is_connected):
        is_logged_in, uid, pwd, is_privilege = login()
        if is_logged_in:
            logged_in(uid, pwd, is_privilege)
