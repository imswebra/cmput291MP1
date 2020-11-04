import unittest
import random
import os
from datetime import date

import database as db

class TestDatabase(unittest.TestCase):
    def setUp(self):
        os.system('sqlite3 unittest_database.db <sql/tables.sql')
        os.system('sqlite3 unittest_database.db <sql/data.sql')
        db.connect('unittest_database.db')

    def test_count_keywords(self):
        self.assertEqual(db.count_keywords("Green apples are tasty", "Tasty apples are green", "Nothing", "green tasty"), 2)

    def test_connect(self):
        self.assertTrue(db.connect('unittest_database.db'))
        self.assertFalse(db.connect(None))

    def test_generate_unique_key(self):
        random.seed(0)
        self.assertEqual(db.generate_unique_key(4, "posts", "pid"), '6604')

    def test_sign_up(self):
        c = db.conn.cursor()
        c.execute('''
            SELECT * FROM users
            WHERE uid = 4
        ''')
        row = c.fetchone()
        self.assertEqual(row, None)
        self.assertTrue(db.sign_up("4", "John", "Calgary", "password"))
        c.execute('''
            SELECT * FROM users
            WHERE uid = 4
        ''')
        row = c.fetchone()
        self.assertEqual(row, ("4", "John", "password", "Calgary", str(date.today())))
        self.assertFalse(db.sign_up("4", "John", "Calgary", "password"))

    def test_login(self):
        self.assertTrue(db.login("1", "p"))
        self.assertFalse(db.login("1", "not_password"))
        self.assertFalse(db.login("5", "p"))

    def test_check_privilege(self):
        self.assertTrue(db.check_privilege("1"))
        self.assertFalse(db.check_privilege("2"))

    def test_post_question(self):
        c = db.conn.cursor()
        random.seed(0)
        c.execute('''
            SELECT * FROM posts
            WHERE pid = 6604
        ''')
        row = c.fetchone()
        self.assertEqual(row, None)

        c = db.conn.cursor()
        c.execute('''
            SELECT * FROM questions
            WHERE pid = 6604
        ''')
        row = c.fetchone()
        self.assertEqual(row, None)

        self.assertTrue(db.post_question("New Title", "New body", "3"))

        c.execute('''
            SELECT * FROM posts
            WHERE pid = 6604
        ''')
        row = c.fetchone()
        self.assertEqual(row, ('6604', str(date.today()), 'New Title', 'New body', '3'))

        c = db.conn.cursor()
        c.execute('''
            SELECT * FROM questions
            WHERE pid = 6604
        ''')
        row = c.fetchone()
        self.assertEqual(row, ("6604", None))


    def test_search_posts(self):
        expected = [
            ('1', '2020-09-29', 'Qestion?', 'This is a post about apple.', '1', 5, 2, 1),
            ('2', '2020-08-29', 'Answer apple', 'This is an answer to that qesution', '2', 5, 1, None),
            ('3', '2020-08-29', 'Another Questions', 'This question does not have the keyword in it', '2', 5, 0, 0),
            ('4', "2020-08-29", 'Apple Apple', 'This has apple 4 times ApplE', '3', 5, 0, 0),
            ('5', '2020-08-29', 'Apple Apple', 'This has apple 4 times ApplE', '3', 5, 0, None),
            ('6', '2020-08-29', 'Apple Apple', 'This has apple 4 times ApplE', '3', 5, 0, None),
            ('7', '2020-08-29', 'Apple Apple', 'This has apple 4 times ApplE', '3', 5, 0, None)
        ]
        self.assertEqual(db.search_posts("apple"), expected)

    def test_post_answer(self):
        c = db.conn.cursor()
        random.seed(1)
        c.execute('''
            SELECT * FROM posts
            WHERE pid = 2914
        ''')
        row = c.fetchone()
        self.assertEqual(row, None)

        c = db.conn.cursor()
        c.execute('''
            SELECT * FROM answers
            WHERE pid = 2914
        ''')
        row = c.fetchone()
        self.assertEqual(row, None)

        self.assertTrue(db.post_answer("New Answer Title", "New body", "3", "1"))

        c.execute('''
            SELECT * FROM posts
            WHERE pid = 2914
        ''')
        row = c.fetchone()
        self.assertEqual(row, ('2914', str(date.today()), 'New Answer Title', 'New body', '3'))

        c = db.conn.cursor()
        c.execute('''
            SELECT * FROM answers
            WHERE pid = 2914
        ''')
        row = c.fetchone()
        self.assertEqual(row, ("2914", "1"))

    def test_post_vote(self):
        c = db.conn.cursor()
        c.execute('''
            SELECT * FROM votes
            WHERE pid = 3
            AND uid = 3
        ''')
        row = c.fetchone()
        self.assertEqual(row, None)

        self.assertTrue(db.post_vote("3", "3"))

        c.execute('''
            SELECT * FROM votes
            WHERE pid = 3
            AND uid = 3
        ''')
        row = c.fetchone()
        self.assertEqual(row, ("3", 1, str(date.today()), "3"))

        self.assertFalse(db.post_vote("3", "3"))

    def test_get_question_of_answer(self):
        expected = ("1", None)
        self.assertEqual(db.get_question_of_answer('2'), expected)
        self.assertEqual(db.get_question_of_answer('1'), None)

    def mark_accepted(self):
        c = db.conn.cursor()
        c.execute('''
            SELECT * FROM questions
            WHERE pid = 1
        ''')
        row = c.fetchone()
        self.assertEqual(row, ("1", None))

        self.assertTrue(db.mark_accepted("2", "1"))

        c.execute('''
            SELECT * FROM questions
            WHERE pid = 1
        ''')
        row = c.fetchone()
        self.assertEqual(row, ("1", "2"))

    def test_get_badges(self):
        expected = [
            ('Great post', 'Gold'),
            ('Best answer', 'Gold'),
            ('Original post', 'Silver'),
            ('Interesting question', 'Silver'),
            ('Good post', 'Bronze'),
            ('Decent post', 'Bronze')
        ]
        self.assertEqual(db.get_badges(), expected)

    def test_give_badge(self):
        c = db.conn.cursor()
        c.execute('''
            SELECT * FROM ubadges
            WHERE uid = 2
            AND bname = 'Great post'
        ''')
        row = c.fetchone()

        self.assertEqual(row, None)

        self.assertTrue(db.give_badge("2", "Great post"))

        c.execute('''
            SELECT * FROM ubadges
            WHERE uid = 2
            AND bname = 'Great post'
        ''')
        row = c.fetchone()

        self.assertEqual(row, ("2", str(date.today()), "Great post"))

        self.assertFalse(db.give_badge("2", "Great post"))

    def test_add_tag(self):
        c = db.conn.cursor()
        c.execute('''
            SELECT * FROM tags
            WHERE pid = 4
            AND tag = 'bob'
        ''')
        row = c.fetchone()

        self.assertEqual(row, None)

        self.assertTrue(db.add_tag("4", "Bob"))

        c.execute('''
            SELECT * FROM tags
            WHERE pid = 4
            AND tag = 'bob'
        ''')
        row = c.fetchone()

        self.assertEqual(row, ("4", "bob"))

        self.assertFalse(db.add_tag("4", "BOB"))

    def test_edit_post(self):
        c = db.conn.cursor()
        c.execute('''
            SELECT * FROM posts
            WHERE pid = 1
        ''')
        row = c.fetchone()

        self.assertEqual(row, ("1", "2020-09-29", "Qestion?", "This is a post about apple.", "1"))

        self.assertTrue(db.edit_post("1", "This is a new Title", "This is a new body"))

        c.execute('''
            SELECT * FROM posts
            WHERE pid = 1
        ''')
        row = c.fetchone()

        self.assertEqual(row, ("1", "2020-09-29", "This is a new Title", "This is a new body", "1"))

    def test_case_insensitive_tag(self):
        self.assertFalse(db.check_has_case_insensitive_entry("tags", ["pid", "tag"], ["1", "BANANA"]))
        self.assertTrue(db.add_tag("1", "banana"))
        self.assertTrue(db.check_has_case_insensitive_entry("tags", ["pid", "tag"], ["1", "BaNaNa"]))

if __name__ == '__main__':
    unittest.main()
