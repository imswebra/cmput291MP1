import sqlite3
from datetime import date
import random, string

#TODO: Actually catch the correct errors
conn = None

def connect(db_name):
    try:
        global conn
        conn = sqlite3.connect(db_name)
        return True
    except Exceptions as e:
        print(e)
        return False


#TODO: Implement
def prevent_sql_injection():
    pass


def generate_unique_key(length, table, col_name):
    while(True):
        key = ''.join(random.choice(string.digits) for _ in range(length))

        try:
            c = conn.cursor()
            stmt = 'SELECT {} FROM {} WHERE {}={};'.format(
                col_name, table, col_name, key
                )
            c.execute(stmt)
            row = c.fetchone()

            if row is None:
                return key
        except Exceptions as e:
            print(e)

def sign_up(uid, name, city, pwd):
    try:
        c = conn.cursor()
        today = date.today()
        c.execute('''
            INSERT INTO users VALUES
            (:uid, :name, :pwd, :city, :date)
        ''', {
                "uid": uid,
                "name": name,
                "pwd": pwd,
                "city": city,
                "date": today
            }
        )

        conn.commit()
    except sqlite3.IntegrityError as e:
        print(e)
        return False

    return True


def login(uid, pwd):
    try:
        c = conn.cursor()
        c.execute('''
            SELECT *
            FROM users
            WHERE uid =:uid AND pwd =:pwd
        ''', {
                "uid": uid,
                "pwd": pwd
            }
        )

        row = c.fetchone()
        if row is None:
            print("Could not find user")
            return False
        else:
            return True

    except Exceptions as e:
        print(e)
        return False


def check_privilege(uid):
    try:
        c = conn.cursor()
        c.execute('''
            SELECT *
            FROM privileged
            WHERE uid =:uid
        ''', {
                "uid": uid,
            }
        )

        row = c.fetchone()
        if row is None:
            return False
        else:
            return True

    except Exceptions as e:
        print(e)
        return False


def post_question(title, body, uid):

    try:
        c = conn.cursor()
        today = date.today()
        post_id = generate_unique_key(4, "posts", "pid")
        c.execute('''
            Insert INTO posts VALUES
            (:pid, :pdate, :title, :body, :poster)
        ''', {
                "pid": post_id,
                "pdate": today,
                "title": title,
                "body": body,
                "poster": uid
            }
        )

        c.execute('''
            Insert INTO questions VALUES
            (?, null)
        ''', (post_id,)
        )

        conn.commit()
    except sqlite3.OperationError as e:
        print(e)
        return False

    return True
