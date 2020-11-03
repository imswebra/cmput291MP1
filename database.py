import sqlite3
from datetime import date
import random, string

#TODO: Actually catch the correct errors!!
conn = None


def count_keywords(string1, string2, keywords):
    """
    Counts the number of occurrence of each keyword of the keyword
    list within string1 and string2
    Parameters:
        string1 (str): The first string to check keyword occurence within
        string2 (str): The second string to check keyword occurence within
        keywords ([str]): a list of keywords to check for occurences within
            string1 and string2
    Returns:
        the number of keyword occurences
    """
    try:
        total_count = 0
        keywords = keywords.split()
        for k in keywords:
            total_count += string1.lower().count(k) + string2.lower().count(k)

        return total_count
    except Exception as e:
        print(e)
        return 0


def connect(db_name):
    """
    Attempts to connect to a database of a given name. Also adds the
    custom function 'count_keywords' to the database connection
    Parameters:
        db_name (str): the name of the database to connect to
    Returns:
        True on connection success, False otherwise
    """
    try:
        global conn
        conn = sqlite3.connect(db_name)
        conn.create_function("count_keywords", 3, count_keywords)

        return True
    except Exception as e:
        print(e)
        return False


def generate_unique_key(length, table, col_name):
    """
    Creates a new unique key for a column within a table
    Parameters:
        length (int): the desired length of a the key
        table (str): the table within which the key should be unique
        col_name (str): the table's column within which the the key should
            be unique
    Returns:
        (int): the generated unique key
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
    """
    Creates a new user
    Parameters:
        uid (str): the user id to attempt to signup
        name (str): the name of the new user attempting to signup
        city (str): the city of the new user attempting to signup
        pwd (str): the password to attempt to signup uid's account with
    Returns:
        True on signup success, False otherwise
    """
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
    """
    Checks if a given uid and password match any users
    Parameters:
        uid (str): the user id to attempt to login
        pwd (str): the password to attempt to log into uid's account with
    Returns:
        True on login success, False otherwise
    """
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
            print("No matching ID and password was found")
            return False
        else:
            return True

    except Exception as e:
        print(e)
        return False


def check_privilege(uid):
    """
    Checks if a given uid is a privileged user or not
    Parameters:
        uid (str): the user id to check if privileged
    Returns:
        True if privileged, False otherwise
    """
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

    except Exception as e:
        print(e)
        return False


def post_question(title, body, uid):
    """
    Allows a user to post a new question
    Parameters:
        title (str): the title of the new question post
        body (str): the body of the new question post
        uid (str): the uid of the question's poster
    Returns:
        True on success, False otherwise
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
    """
    Allows a user to search all posts related by a 
    Parameters:
        title (str): the title of the new answer post
        body (str): the body of the new answer post
        uid (str): the uid of the answer's poster
        qid (str): the question id which is being answer
    Returns:
        True on success, False otherwise
    """
    # Get posts with keywords
    keywords = [s.lower() for s in keywords]
    joined_keywords = " ".join(keywords)
    keywords.append(joined_keywords)
    keywords.append(joined_keywords)

    try:
        c = conn.cursor()

        sql = ('''
            with tagCount as (
                select p.pid as pid, count(*) as keywordCount
                from posts p join tags t on p.pid = t.pid
                where lower(tag) in ({seq})
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
            count_keywords(p.title, p.body, ?) + ifnull(tc.keywordCount, 0) as wordCount,
            ifnull(vc.count, 0),
            ac.count
            from posts p
            left outer join tagCount tc on p.pid = tc.pid
            left outer join voteCount vc on p.pid = vc.pid
            left outer join answerCount ac on p.pid = ac.pid
            where count_keywords(p.title, p.body, ?) > 0
            or tc.keywordCount > 0
            order by wordcount desc;
        ''').format(
            seq=','.join(['?']*(len(keywords) - 2))
        )

        c.execute(sql, keywords,)

        rows = c.fetchall()

        return rows
    except Exception as e:
        print(e)
        return []


def post_answer(title, body, uid, qid):
    """
    Allows a user to post an answer to a question, marked by qid
    Parameters:
        title (str): the title of the new answer post
        body (str): the body of the new answer post
        uid (str): the uid of the answer's poster
        qid (str): the question id which is being answer
    Returns:
        True on success, False otherwise
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
    """
    Allows a user to vote on a post
    Parameters:
        pid (str): the post id which is being given a vote
        uid (str): the user which is voting on the post
    Returns:
        True on success, False otherwise
    """
    try:
        c = conn.cursor()
        today = date.today()

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
    """
    Returns the question which corresponds to a given answer post id
    Parameters:
        answer_pid (str): the post id of the answer whose corresponding
            question is to be returned
    Returns:
        the question entry that corresponds to the provided answer_pid
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
    """
    Allows a privileged user to mark an answer as the accepted answer
    for its corresponding question post
    Parameters:
        answer_pid (str): the post id of the answer that is being
            marked as accepted
        question_pid (str): the post id of the question post whose
            theaid value is being set to answer_pid
    Returns:
        True on success, False otherwise
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
    """
    Retrieves the list of all possible badges
    Returns:
        All entries from the badges table
    """
    try:
        c = conn.cursor()
        c.execute("SELECT * FROM badges")
        return c.fetchall()

    except Exception as e:
        print(e)
        return None


def give_badge(uid, badge_name):
    """
    Allows a privileged user to give a user a badge on today's date
    Parameters:
        uid (str): the uid of which to give a badge
        badge_name (str): the name of the badge which is being given
    Returns:
        True on success, False otherwise
    """
    try:
        c = conn.cursor()
        today = date.today()

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

def check_post_has_tag(pid, tag):
    """Returns true a post already has a case-insensitive tag, false otherwise

    Parameters:
        pid (str): the post ID which is being checked if it has tag
        tag (str): the string of the tag to check if a post has
    """
    try:
        c = conn.cursor()

        c.execute('''
            SELECT * FROM tags
            WHERE pid =:pid
            AND lower(tag) =:tag
        ''', {
                "pid": pid,
                "tag": tag.lower()
            }
        )

        row = c.fetchone()

        if row is None:
            return False
        return True

    except Exception as e:
        print(e)
        return True

def add_tag(pid, tag):
    """
    Allows a privileged user to add a tag to a post
    Parameters:
        pid (str): the post ID which is being given the tag
        tag (str): the string of the tag which is being added to the post
    Returns:
        True on success, False otherwise
    """
    try:
        if (check_post_has_tag(pid, tag)):
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
    """
    Allows a privileged user to edit the title and body of a post
    Parameters:
        pid (str): the post ID which is being editted
        title (str): the new title to assign to the post
        body (str): the new body to assign to the post
    Returns:
        True on success, False otherwise
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
