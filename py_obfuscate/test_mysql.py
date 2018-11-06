import unittest
import os
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/")
import mysql

mysqlParser = mysql.MySql()

class TestStringMethods(unittest.TestCase):

    def test_match_insert(self):
        fixture = "INSERT INTO `foo` (`bar`, `baz`, `qux`) VALUES (1, 'one','one'),(2, 'two','two');"
        self.assertEqual(mysqlParser.is_insert(fixture), True)

    def test_not_match_commented_out_insert(self):
        fixture = "<!--INSERT INTO `foo` (`bar`, `baz`, `qux`) VALUES (1, 'one','one'),(2, 'two','two');-->"
        self.assertEqual(mysqlParser.is_insert(fixture), False)

    def test_extrac_insert_details(self):
        fixture = "INSERT INTO `foo` (`bar`, `baz`, `qux`) VALUES (1, 'one','one'),(2, 'two','two');"
        #self.assertEqual(mysql.is_insert(fixture), False)
        mysqlInsert = mysql.InsertStatement(fixture)

    def test_extract_inserts(self):
        fixture = "INSERT INTO `foo` (`bar`, `baz`, `qux`) VALUES (1, 'one','one'),(2, 'two','two');"
        mysqlInsert = mysql.InsertStatement(fixture)
        self.assertEqual(mysqlInsert.get_inserts(), [
            {'bar': '1', 'baz': 'one', 'qux': 'one'},
            {'bar': '2', 'baz': 'two', 'qux': 'two'}
        ])

    def test_with_escaped_characters(self):
        fixture = "INSERT INTO `some_table` (thing1,thing2) VALUES ('bob,@bob.c  , om', 'bo\\', b'),    ('hi', 5)  ;"
        mysqlInsert = mysql.InsertStatement(fixture)
        self.assertEqual(mysqlInsert.get_inserts(), [
            {'thing1': 'bob,@bob.c  , om', 'thing2': "bo', b"},
            {'thing1': 'hi', 'thing2': '5'},
        ])


    def test_with_quoted_parenthesis(self):
        fixture = "INSERT INTO `some_table` (thing1,thing2) VALUES ('(()()())', 'something'), (')(', '()');"
        mysqlInsert = mysql.InsertStatement(fixture)
        self.assertEqual(mysqlInsert.get_inserts(), [
            {'thing1': '(()()())', 'thing2': "something"},
            {'thing1': ')(', 'thing2': "()"}
        ])


    def test_with_null_values(self):
        fixture = "INSERT INTO `some_table` (thing1,thing2) VALUES ('NULL', NULL), (NULL,NULL);"
        mysqlInsert = mysql.InsertStatement(fixture)
        self.assertEqual(mysqlInsert.get_inserts(), [
            {'thing1': 'NULL', 'thing2': None},
            {'thing1': None, 'thing2': None}
        ])
    

    def test_with_empty_values(self):
        fixture = "INSERT INTO `some_table` (thing1,thing2) VALUES (0, NULL), ('',' ');"
        mysqlInsert = mysql.InsertStatement(fixture)
        self.assertEqual(mysqlInsert.get_inserts(), [
            {'thing1': '0', 'thing2': None},
            {'thing1': '', 'thing2': ' '}
        ])

    def test_to_string(self):
        fixture = fixture = "INSERT INTO `foo` (`bar`,`baz`,`qux`) VALUES ('1','one','one'),('2','two','two');"
        mysqlInsert = mysql.InsertStatement(fixture)
        self.assertEqual(mysqlInsert.to_string(), fixture)

    def test_to_string_with_escaped_characters(self):
        fixture = fixture = "INSERT INTO `foo` (`bar`,`baz`,`qux`) VALUES ('o\\'brien','one','one'),('2','two','two');"
        mysqlInsert = mysql.InsertStatement(fixture)
        self.assertEqual(mysqlInsert.to_string(), fixture)

    def test_to_string_tidies_up_sql(self):
        fixture = "INSERT INTO `some_table` (thing1,thing2) VALUES ('bob,@bob.c  , om', 'bo\\', b'),    ('hi', 5)  ;"
        expected = "INSERT INTO `some_table` (`thing1`,`thing2`) VALUES ('bob,@bob.c  , om','bo\\', b'),('hi','5');"
        mysqlInsert = mysql.InsertStatement(fixture)
        self.assertEqual(mysqlInsert.to_string(), expected)

    def test_to_string_handles_null(self):
        fixture = "INSERT INTO `some_table` (`thing1`,`thing2`) VALUES ('NULL',NULL),(NULL,NULL),('',' ');"
        mysqlInsert = mysql.InsertStatement(fixture)
        self.assertEqual(mysqlInsert.to_string(), fixture)

    def test_to_string_handles_parenthesis(self):
        fixture = "INSERT INTO `some_table` (`thing1`,`thing2`) VALUES ('(()()())','something'),(')(','()');"
        mysqlInsert = mysql.InsertStatement(fixture)
        self.assertEqual(mysqlInsert.to_string(), fixture)


if __name__ == '__main__':
    unittest.main()

#('some\"thin\\gel\\\\\se1', 25), ('2', 10)