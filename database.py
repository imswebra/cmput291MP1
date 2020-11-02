import sqlite3
from datetime import date
import random, string

#TODO: Actually catch the correct errors!!
conn = None


def count_keywords(string1, string2, keywords):
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
    try:
        global conn
        conn = sqlite3.connect(db_name)
        conn.create_function("count_keywords", 3, count_keywords)

        return True
    except Exception as e:
        print(e)
        return False


def generate_unique_key(length, table, col_name):
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
    try:
        c = conn.cursor()
        c.execute("SELECT * FROM badges")
        return c.fetchall()

    except Exception as e:
        print(e)
        return None


def give_badge(uid, badge_name):
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


def add_tag(pid, tag):
    try:
        c = conn.cursor()

        c.execute('''
            insert into tags values
            (:pid, :tag)
        ''', {
            "pid": pid,
            "tag": tag
        })

        conn.commit()
        return True

    except Exception as e:
        print(e)
        return False


def edit_post(pid, title, body):
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
