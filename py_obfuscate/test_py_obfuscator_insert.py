import unittest
import os
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/")
import py_obfuscator
import mysql

class TestObfuscateInsert(unittest.TestCase):

    def test_obfuscate_insert(self):
        config = {
            "tables": {
                "users": {
                    "title": { "type": "fixed", "value": ["Mr", "Mrs", "Miss"] },
                    "name": { "type": "name" },
                    "email": { "type": "email" },
                    "phone": { "type": "mobile" },
                    "password": { "type": "fixed", "value": "some known hash" },
                }
            }
        }
        insrt = ("INSERT INTO `users` (`title`,`name`,`password`,`email`,`phone`,`account_no`) VALUES "
                + "('Mr','Adam Smith','Secret','asmith@gmail.com','01784123456','9999999999'),"
                + "('Mrs','Julie Jones','Password','jjones@gmail.com','01784123456','1111111111');")

        obfuscate = py_obfuscator.Obfuscator(config)
        mysqlInsert = mysql.InsertStatement(insrt)
        
        obfuscate.obfuscate_insert_statement(mysqlInsert)

        self.assertNotEqual(mysqlInsert.get_inserts()[0].get("name"), "Adam Smith")
        self.assertNotEqual(mysqlInsert.get_inserts()[0].get("password"), "Secret")
        self.assertNotEqual(mysqlInsert.get_inserts()[0].get("email"), "asmith@gmail.com")
        self.assertNotEqual(mysqlInsert.get_inserts()[0].get("phone"), " 01784123456")
        self.assertEqual(mysqlInsert.get_inserts()[0].get("account_no"), "9999999999")

        self.assertNotEqual(mysqlInsert.get_inserts()[0].get("name"), "Julie Jones")
        self.assertNotEqual(mysqlInsert.get_inserts()[0].get("password"), "Password")
        self.assertNotEqual(mysqlInsert.get_inserts()[0].get("email"), "jjones@gmail.com")
        self.assertNotEqual(mysqlInsert.get_inserts()[0].get("phone"), " 01784123456")
        self.assertEqual(mysqlInsert.get_inserts()[1].get("account_no"), "1111111111")


    def test_unless_row_matches(self):
        config = {
            "tables": {
                "users": {
                    "password": { 
                        "type": "fixed", 
                        "value": "replaced",
                        "unless": {"username": "admin"}
                    },
                }
            }
        }
        insrt = ("INSERT INTO `users` (`username`,`password`) VALUES "
                + "('asmith','$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p92ldGxad68LJZdL17lhWy'),"
                + "('admin','$2a$04$Lzns3sQdgXKaDIguDlqX4uqemS4rZHabwQnNAIra.MXpcIX.1N3Yy'),"
                + "('jjulie','$2a$04$m9bdaJ1.aArg0YwK5oIP4ewoSFIlaVtIOVOoVapKx4F4.Dpt0KnGK');")

        obfuscate = py_obfuscator.Obfuscator(config)
        mysqlInsert = mysql.InsertStatement(insrt)
        
        obfuscate.obfuscate_insert_statement(mysqlInsert)

        self.assertEqual(mysqlInsert.get_inserts()[0].get("password"), 'replaced')
        self.assertEqual(mysqlInsert.get_inserts()[1].get("password"), '$2a$04$Lzns3sQdgXKaDIguDlqX4uqemS4rZHabwQnNAIra.MXpcIX.1N3Yy')
        self.assertEqual(mysqlInsert.get_inserts()[2].get("password"), 'replaced')


    def test_table_not_in_config_ignored(self):
        config = {
            "tables": {
                "users": {
                    "password": { 
                        "type": "fixed", 
                        "value": "replaced",
                        "unless": {"username": "admin"}
                    },
                }
            }
        }
        insrt = ("INSERT INTO `logins` (`username`,`password`) VALUES "
                + "('asmith','$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p92ldGxad68LJZdL17lhWy'),"
                + "('admin','$2a$04$Lzns3sQdgXKaDIguDlqX4uqemS4rZHabwQnNAIra.MXpcIX.1N3Yy'),"
                + "('jjulie','$2a$04$m9bdaJ1.aArg0YwK5oIP4ewoSFIlaVtIOVOoVapKx4F4.Dpt0KnGK');")

        obfuscate = py_obfuscator.Obfuscator(config)
        mysqlInsert = mysql.InsertStatement(insrt)
        
        obfuscate.obfuscate_insert_statement(mysqlInsert)

        self.assertEqual(mysqlInsert.to_string(), insrt)


    def test_table_truncated(self):
        config = {
            "tables": {
                "users": {"truncate": True}
            }
        }
        insrt = ("INSERT INTO `users` (`username`,`password`) VALUES "
                + "('asmith','$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p92ldGxad68LJZdL17lhWy'),"
                + "('admin','$2a$04$Lzns3sQdgXKaDIguDlqX4uqemS4rZHabwQnNAIra.MXpcIX.1N3Yy'),"
                + "('jjulie','$2a$04$m9bdaJ1.aArg0YwK5oIP4ewoSFIlaVtIOVOoVapKx4F4.Dpt0KnGK');")

        obfuscate = py_obfuscator.Obfuscator(config)
        mysqlInsert = mysql.InsertStatement(insrt)
        
        obfuscate.obfuscate_insert_statement(mysqlInsert)

        self.assertEqual(mysqlInsert.to_string(), "")

    def test_order_preserved(self):
        config = {
            "tables": {
                "foo": {
                    "postcode": {"type":"fixed","value":"postcode"},
                    "name": {"type":"fixed","value":"name"},
                    "phone": {"type":"fixed","value":"phone"},
                    "email": {"type":"fixed","value":"email"},
                    "accountno": {"type":"fixed","value":"accountno"}
                }
            }
        }
        insrt = "INSERT INTO `foo` (`oo_id`, `name`, `postcode`, `phone`, `email`, `accountno`, `formtype`) VALUES (1124793,NULL,NULL,NULL,NULL,NULL,NULL);"
        
        obfuscate = py_obfuscator.Obfuscator(config)
        mysqlInsert = mysql.InsertStatement(insrt)
        
        obfuscate.obfuscate_insert_statement(mysqlInsert)

        self.assertEqual(
            mysqlInsert.to_string(), 
            "INSERT INTO `foo` (`oo_id`,`name`,`postcode`,`phone`,`email`,`accountno`,`formtype`) VALUES ('1124793','name','postcode','phone','email','accountno',NULL);"
        )


if __name__ == '__main__':
    unittest.main()
