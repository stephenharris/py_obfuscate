import unittest
import os
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/")
import py_obfuscator

obfuscate = py_obfuscator.Obfuscator({})

class TestObfuscator(unittest.TestCase):

    def test_apply_fixed(self):
        config = {
            "type": "fixed",
            "value": "foobar"
        }

        self.assertEqual(obfuscate._obfuscate_value("hello world", config), "foobar")

    def test_apply_fixed_multiple(self):
        config = {
            "type": "fixed",
            "value": ["foo", "bar", "baz"]
        }
        self.assertIn(obfuscate._obfuscate_value("hello world", config), ["foo", "bar", "baz"])


    def test_apply_string_defaults(self):
        config = {
            "type": "string",
        }
        self.assertEqual(len(obfuscate._obfuscate_value("hello world", config)), 10)


    def test_apply_string_with_chars_and_length(self):
        config = {
            "type": "string",
            "chars": "0123456789",
            "length": 30
        }
        value = obfuscate._obfuscate_value("hello world", config)
        self.assertEqual(len(value), 30)
        self.assertRegex(value, r"\d{30}")


    def test_apply_integer_defaults(self):
        config = {
            "type": "integer"
        }
        value = obfuscate._obfuscate_value("hello world", config)
        self.assertRegex(str(value), r"\d+")
        self.assertGreaterEqual(value, 0)
        self.assertLessEqual(value, 100)

    def test_apply_integer_with_min_max(self):
        config = {
            "type": "integer",
            "min": 47,
            "max": 53
        }
        value = obfuscate._obfuscate_value("hello world", config)
        self.assertRegex(str(value), r"\d+")
        self.assertGreaterEqual(value, 47)
        self.assertLessEqual(value, 53)

    def test_apply_email(self):
        config = {
            "type": "email"
        }
        value = obfuscate._obfuscate_value("hello world", config)
        self.assertRegex(str(value), r"\S+@\S+\.example.com")


    def test_apply_sortcode(self):
        config = {
            "type": "sortcode",
        }
        value = obfuscate._obfuscate_value("hello world", config)
        self.assertRegex(value, r"\d{6}")


    def test_apply_bank_account(self):
        config = {
            "type": "bank_account"
        }
        value = obfuscate._obfuscate_value("hello world", config)
        self.assertRegex(value, r"\d{8}")


    def test_apply_mobile(self):
        config = {
            "type": "mobile"
        }
        value = obfuscate._obfuscate_value("hello world", config)
        self.assertRegex(value, r"07\d{9}")


    def test_apply_uk_landline(self):
        config = {
            "type": "uk_landline"
        }
        value = obfuscate._obfuscate_value("hello world", config)
        self.assertRegex(value, r"01632\d{6}")

    def test_apply_null(self):
        config = {
            "type": "null"
        }
        value = obfuscate._obfuscate_value("hello world", config)
        self.assertIsNone(value)

    def test_apply_string_with_chars_and_length(self):
        config = {
            "type": "username"
        }
        value = obfuscate._obfuscate_value("hello world", config)
        self.assertRegex(value, r"[a-z]+")


if __name__ == '__main__':
    unittest.main()
