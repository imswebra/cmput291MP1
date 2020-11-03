import unittest
# import unittest.mock
from unittest.mock import patch, PropertyMock
import random
import os

import database as db

class TestDatabase(unittest.TestCase):
    def setUp(self):
        os.system('sqlite3 unittest_database.db <sql/tables.sql')
        os.system('sqlite3 unittest_database.db <sql/data.sql')
        db.connect('unittest_database.db')

    def test_count_keywords(self):
        self.assertEquals(db.count_keywords("Green apples are tasty", "Tasty apples are green", "Nothing", "green tasty"), 4)

    def test_connect(self):
        self.assertTrue(db.connect('database.db'))
        self.assertFalse(db.connect(None))

    def test_generate_unique_key(self):
        random.seed(0)
        self.assertEquals(db.generate_unique_key(4, "posts", "pid"), '6604')

    def test_sign_up(self):
        self.assertTrue(db.sign_up("4", "John", "Calgary", "password"))
        self.assertFalse(db.sign_up("4", "John", "Calgary", "password"))

    def test_login(self):
        self.assertTrue(db.login("1", "p"))
        self.assertFalse(db.login("1", "not_password"))
        self.assertFalse(db.login("5", "p"))

    def test_check_privilege(self):
        self.assertTrue(db.check_privilege("1"))
        self.assertFalse(db.check_privilege("2"))

    # TODO: need to find a way to test the specific cursor.lastrowid of the cursor within post_question
    # def test_post_question(self):
    #     random.seed(0)
    #     self.assertTrue(db.post_question("New question", "New question body", "1"))
    #     self.assertEquals(db.conn.cursor().lastrowid, '6604')

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
        self.assertEquals(db.search_posts("apple"), expected)

    def test_get_question_of_answer(self):
        expected = ("1", None)
        self.assertEquals(db.get_question_of_answer('2'), expected)
        self.assertEquals(db.get_question_of_answer('1'), None)

    def test_get_badges(self):
        expected = [
            ('Great post', 'Gold'),
            ('Best answer', 'Gold'),
            ('Original post', 'Silver'),
            ('Interesting question', 'Silver'),
            ('Good post', 'Bronze'),
            ('Decent post', 'Bronze')
        ]
        self.assertEquals(db.get_badges(), expected)

    def test_case_insensitive_tag(self):
        self.assertFalse(db.check_post_has_tag("1", "BANANA"))
        self.assertTrue(db.add_tag("1", "banana"))
        self.assertTrue(db.check_post_has_tag("1", "BaNaNa"))

if __name__ == '__main__':
    unittest.main()