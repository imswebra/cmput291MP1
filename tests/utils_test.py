import unittest

import utils as u

class TestDatabase(unittest.TestCase):
    def test_split_and_strip(self):
        value = "this,   that  , there"
        expected = ["this", "that", "there"]
        self.assertEqual(u.split_and_strip(value), expected)

    def test_keyword_input_validate(self):
        self.assertEqual(u.keyword_input_validate("/back"), (True, False))
        self.assertEqual(u.keyword_input_validate("/logout"), (True, True))
        self.assertEqual(u.keyword_input_validate("other_command"), (False, False))

    def test_get_indices_range(self):
        mock_results = [
            ("value1"),
            ("value2"),
            ("value3"),
            ("value4"),
            ("value5"),
            ("value6"),
            ("value7"),
            ("value8"),
            ("value9"),
        ]
        self.assertEqual(u.get_indices_range(mock_results), (0, 5))
        self.assertEqual(u.get_indices_range(mock_results, 1, 6), (6, 9))
        self.assertEqual(u.get_indices_range(mock_results, 0, 5), (5, 9))

    def test_stringify(self):
        self.assertEqual(u.stringify(None), "N/A")
        self.assertEqual(u.stringify(Exception("a")), "a")
        self.assertEqual(u.stringify(Exception("abcdefg"), 5), "ab...")

    def test_is_index(self):
        mock_results = [
            ("value1"),
            ("value2"),
            ("value3"),
            ("value4"),
            ("value5"),
            ("value6"),
            ("value7"),
            ("value8"),
            ("value9"),
        ]
        self.assertTrue(u.is_index("1", mock_results))
        self.assertFalse(u.is_index("0", mock_results))
        self.assertTrue(u.is_index("9", mock_results))
        self.assertFalse(u.is_index("10", mock_results))

if __name__ == '__main__':
    unittest.main()
