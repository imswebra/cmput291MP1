import sqlite3
from datetime import date
import random, string

#TODO: Actually catch the correct errors!!
conn = None


def count_keywords(string1, string2, string3, keywords):
    """Counts number of keywords present in the two strings

    Note that only counts +1 if keyword is in either string or 0 if not. Does
    not count the number of occurrences.

    Args:
        string1 (str): The first string to check keyword occurrence within
        string2 (str): The second string to check keyword occurrence within
        string3 (str): The third string to check keyword occurrence within
        keywords ([str]): A list of keywords to check for occurrences within
            string1 and string2
    Returns:
        (int): The number of keyword occurrences
    """
    try:
        string1 = string1.lower() if string1 else ""
        string2 = string2.lower() if string2 else ""
        string3 = string3.lower() if string3 else ""

        total_count = 0
        keywords = keywords.lower().split()
        for k in keywords:
            if k in string1 or k in string2 or k in string3:
                total_count += 1

        return total_count
    except Exception as e:
        print(e)
        return 0


def connect(db_name):
    """Attempts to connect to a database of a given name

    Also adds the custom function 'count_keywords' to the database connection.

    Args:
        db_name (str): The name of the database to connect to
    Returns:
        (bool): True on connection success, False otherwise
    """
    try:
        global conn
        conn = sqlite3.connect(db_name)
        conn.create_function("count_keywords", 4, count_keywords)

        return True
    except Exception as e:
        print(e)
        return False


def generate_unique_key(length, table, col_name):
    """Creates a new unique key for a column within a table

    Args:
        length (int): The desired length of a the key
        table (str): The table within which the key should be unique
        col_name (str): The table's column within which the key should be
            unique
    Returns:
        (int): The generated unique key
    """
    while(True):
        key = ''.join(random.choice(string.digits) for _ in range(length))

        try:
            c = conn.cursor()
            # Using format here is ok since no user input is used
            stmt = 'SELECT {} FROM {} WHERE {}={};'.format(
                col_name, table, col_name, key
                )
            c.execute(stmt)
            row = c.fetchone()

            if row is None:
                return key
        except Exception as e:
            print(e)


def sign_up(uid, name, city, pwd):
    """Creates a new user

    Args:
        uid (str): The new user id
        name (str): The new user's name
        city (str): The new user's city
        pwd (str): The new user's password
    Returns:
        (bool): True on signup success, False otherwise
    """
    try:
        c = conn.cursor()
        today = date.today()

        if (check_has_case_insensitive_entry("users", ["uid"], [uid])):
            print("This username has already been created (usernames are case-insensitive)")
            return False

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
        if "UNIQUE constraint failed" in str(e):
            print("Sorry, that ID is already in use")
        else:
            print(e)
        return False
    except Exception as e:
        print(e)
        return False

    return True


def login(uid, pwd):
    """Checks if a given uid and password match any users

    Args:
        uid (str): The user id to attempt to login
        pwd (str): The password to attempt to log into uid's account with
    Returns:
        (bool): True on login success, False otherwise
    """
    try:
        c = conn.cursor()
        c.execute('''
            SELECT *
            FROM users
            WHERE lower(uid) =:uid AND pwd =:pwd
        ''', {
                "uid": uid.lower(),
                "pwd": pwd
            }
        )

        row = c.fetchone()
        if row is None:
            print("No matching ID and password was found")
            return False
        else:
            return True

    except Exception as e:
        print(e)
        return False


def check_privilege(uid):
    """Checks if a given uid is a privileged user or not

    Args:
        uid (str): The user id to check if privileged
    Returns:
        (bool): True if privileged, False otherwise
    """
    try:
        c = conn.cursor()
        c.execute('''
            SELECT *
            FROM privileged
            WHERE lower(uid) =:uid
        ''', {
                "uid": uid.lower(),
            }
        )

        row = c.fetchone()
        if row is None:
            return False
        else:
            return True

    except Exception as e:
        print(e)
        return False


def post_question(title, body, uid):
    """Posts a new question

    Args:
        title (str): The title of the new question post
        body (str): The body of the new question post
        uid (str): The uid of the question's poster
    Returns:
        (bool): True on success, False otherwise
    """
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
    except Exception as e:
        print(e)
        return False

    return True


def search_posts(keywords):
    """Searches all posts related by keywords

    Args:
        keywords([str]): The keywords to search for
    Returns:
        ([results row]): The list of matching posts
    """

    try:
        c = conn.cursor()

        sql = ('''
            with tagCount as (
                select p.pid as pid, group_concat(t.tag) as tagsStr
                from posts p join tags t on p.pid = t.pid
                group by p.pid
            ), voteCount as (
                select p.pid, max(v.vno) as count
                from posts p join votes v on p.pid = v.pid
                group by p.pid
            ), answerCount as (
                select q.pid as pid, count(a.pid) as count
                from questions q
                left outer join answers a on q.pid = a.qid
                group by q.pid
            )
            select p.pid,
            p.pdate,
            p.title,
            p.body,
            p.poster,
            count_keywords(p.title, p.body, tc.tagsStr, ?) as wordCount,
            ifnull(vc.count, 0),
            ac.count
            from posts p
            left outer join tagCount tc on p.pid = tc.pid
            left outer join voteCount vc on p.pid = vc.pid
            left outer join answerCount ac on p.pid = ac.pid
            where wordCount > 0
            order by wordcount desc;
        ''')

        c.execute(sql, (" ".join(keywords),))

        rows = c.fetchall()

        return rows
    except Exception as e:
        print(e)
        return []


def post_answer(title, body, uid, qid):
    """Posts a new answer to a given question

    Args:
        title (str): The title of the new answer post
        body (str): The body of the new answer post
        uid (str): The uid of the answer's poster
        qid (str): The question id which is being answer
    Returns:
        (bool): True on success, False otherwise
    """
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
            Insert INTO answers VALUES
            (?, ?)
        ''', (post_id, qid,)
        )

        conn.commit()
    except Exception as e:
        print(e)
        return False

    return True


def post_vote(pid, uid):
    """Posts a vote by the given user to the given post

    Args:
        pid (str): The post id which is being given a vote
        uid (str): The user which is voting on the post
    Returns:
         (bool): True on success, False otherwise
    """
    try:
        c = conn.cursor()
        today = date.today()

        # Check and see if a user has already voted on this
        # post
        c.execute('''
            select v.uid
            from votes v
            where v.pid = ?
            and v.uid = ?
        ''', (pid, uid,))

        row = c.fetchone()
        if row is not None:
            print("You have already voted on this post")
            return False

        # Get the next vote number
        c.execute('''
            select ifnull(max(vno), 0)
            from votes v
            where v.pid = ?
        ''', (pid,)
        )

        row = c.fetchone()
        vote_number = row[0] + 1

        c.execute('''
            Insert INTO votes VALUES
            (:pid, :vno, :vdate, :uid)
        ''', {
                "pid": pid,
                "vno": vote_number,
                "vdate": today,
                "uid": uid
            }
        )

        conn.commit()
    except Exception as e:
        print(e)
        return False

    return True


def get_question_of_answer(answer_pid):
    """Returns the question id corresponding to the given answer id

    Args:
        answer_pid (str): The post id of the answer whose corresponding
            question is to be returned
    Returns:
        (str): The post id of the corresponding question
    """
    try:
        c = conn.cursor()

        c.execute('''
            select q.pid,
            q.theaid
            from questions q,
            answers a
            where a.pid = ?
            and a.qid = q.pid;
        ''', [answer_pid]
        )

        return c.fetchone()

    except Exception as e:
        print(e)
        return None


def mark_accepted(answer_pid, question_pid):
    """Marks a given answer as accepted for the given question

    Args:
        answer_pid (str): The post id of the answer that is being marked as
            accepted
        question_pid (str): The post id of the question whose theaid value is
            being set to answer_pid
    Returns:
        (bool): True on success, False otherwise
    """
    try:
        c = conn.cursor()

        c.execute('''
            update questions
            set theaid = ?
            where pid = ?;
        ''', (answer_pid, question_pid))

        conn.commit()
        return True

    except Exception as e:
        print(e)
        return False


def get_badges():
    """Retrieves the list of all possible badges

    Returns:
        ([badges row]): All entries from the badges table
    """
    try:
        c = conn.cursor()
        c.execute("SELECT * FROM badges")
        return c.fetchall()

    except Exception as e:
        print(e)
        return None


def give_badge(uid, badge_name):
    """Gives the given badge to the given user

    Args:
        uid (str): The uid of which to give a badge
        badge_name (str): The name of the badge which is being given
    Returns:
        (bool): True on success, False otherwise
    """
    try:
        c = conn.cursor()
        today = date.today()

        if (check_has_case_insensitive_entry("ubadges", ["uid", "date", "bname"], [uid, today, badge_name])):
            print("This badge has already been added to this post (badges are case-insensitive)")
            return False

        c.execute('''
            insert INTO ubadges VALUES
            (:uid, :date, :bname)
        ''', {
                "uid": uid,
                "date": today,
                "bname": badge_name,
            }
        )

        conn.commit()
    except sqlite3.IntegrityError as e:
        if "UNIQUE constraint failed" in str(e):
            print("A badge was already given to this user today")
        else:
            print(e)
        return False
    except Exception as e:
        print(e)
        return False

    return True


def add_tag(pid, tag):
    """Adds the given tag to a given post

    Args:
        pid (str): The post ID which is being given the tag
        tag (str): The string of the tag which is being added to the post
    Returns:
        (bool): True on success, False otherwise
    """
    try:
        if (check_has_case_insensitive_entry("tags", ["pid", "tag"], [pid, tag])):
            print("This tag has already been added to this post (tags are case-insensitive)")
            return False

        c = conn.cursor()

        c.execute('''
            insert into tags values
            (:pid, :tag)
        ''', {
            "pid": pid,
            "tag": tag.lower()
        })

        conn.commit()
        return True

    except Exception as e:
        print(e)

        return False


def edit_post(pid, title, body):
    """Updates the given post with a new title and body

    Args:
        pid (str): The post ID which is being editted
        title (str): The new title to assign to the post, "" to use old title
        body (str): The new body to assign to the post, "" to use old body
    Returns:
        (bool): True on success, False otherwise
    """
    try:
        c = conn.cursor()

        if title == "":
            c.execute('''
                update posts
                set body = ?
                where pid = ?
            ''', (body, pid))
        elif body == "":
            c.execute('''
                update posts
                set title = ?
                where pid = ?
            ''', (title, pid))
        else:
            c.execute('''
                update posts
                set title = ?,
                body = ?
                where pid = ?
            ''', (title, body, pid))

        conn.commit()
        return True

    except Exception as e:
        print(e)
        return False


def check_has_case_insensitive_entry(table_name, column_names, values):
    """Returns True a table already has a case-insensitive value, else False

    Args:
        table_name (str): The table in which case-insensitivity is checked
        column_names ([str]): A list of columns to check
        values ([str]): A list of values to check each corresponding to its
            similarly indexed value in column_names
    Returns:
        (bool): True if table has value in column_name, False otherwise
    """
    try:
        c = conn.cursor()

        sql = 'SELECT * FROM {} WHERE'.format(
                table_name
        )
        for i in range(len(column_names)):
            sql += ' LOWER({}) = \'{}\''.format(column_names[i], values[i].lower())
            if i == len(column_names) - 1:
                sql += ';'
            else:
                sql += ' AND'

        c.execute(sql)

        row = c.fetchone()

        if row is None:
            return False
        return True

    except Exception as e:
        print(e)
        return True
