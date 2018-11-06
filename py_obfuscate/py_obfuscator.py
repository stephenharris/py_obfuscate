import random
import re
from faker import Faker
import py_obfuscate.mysql as mysql

class Obfuscator:

    NUMERICS = '1234567890'
    ALPHA_LC = "abcdefghijklmnopqrstuvwxyz"
    ALPHA_UC = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    OTHER_CHARS = "_+-=[{]}/?|!@#$%^&*()`~"
    ALPHA = None
    ALL = None

    def __init__(self, config):
        self.ALPHA = self.ALPHA_LC + self.ALPHA_UC
        self.ALL = self.ALPHA_LC + self.ALPHA_UC
        self.config = config
        self.faker = Faker(config.get('locale','en_GB'))

    def obfuscate(self, streamIn, streamOut):
        mysqlParser = mysql.MySql()
        for line in streamIn.readlines():
            if mysqlParser.is_insert(line):
                insert_statement = mysql.InsertStatement(line)
                self.obfuscate_insert_statement(insert_statement)
                streamOut.write(insert_statement.to_string())
            else:
                streamOut.write(line)

        streamIn.close()              

    def obfuscate_insert_statement(self, insert_statement):

        table = insert_statement.table()
        table_config = self.config["tables"].get(table, None)

        if table_config is None:
            return
        
        if table_config.get("truncate", False):
            insert_statement.empty()
            return

        for row in insert_statement:
            for column, value in row.items():
                if column not in table_config.keys():
                    continue
                
                column_config = table_config[column]

                unless = column_config.get("unless", None)

                if unless is None or self._row_not_excluded(row, unless):
                    row[column] = self._obfuscate_value(value, column_config)
    

    def _obfuscate_value(self, value, column_config):

        value_type = column_config.get("type", "")

        if value_type == 'fixed' and isinstance(column_config.get("value", ""), str):
            return column_config.get("value", "")

        elif value_type == 'fixed' and not isinstance(column_config.get("value", ""), str):
            values = column_config.get("value")
            index = random.randint(0, len(values) - 1)
            return values[index]

        elif value_type == 'string':
            length = column_config.get("length", 10)
            chars = column_config.get("chars", self.ALL)
            return self.random_string(length,chars)

        elif value_type == 'integer':
            minimum = column_config.get("min", 0)
            maximum = column_config.get("max", 100)
            return random.randint(minimum,maximum)

        elif value_type == 'email':
            return self.faker.email() + "." + self.random_string(5,self.ALPHA_LC) + ".example.com"

        elif value_type == 'name':
            return self.faker.name()

        elif value_type == 'first_name':
            return self.faker.first_name()

        elif value_type == 'username':
            username = re.sub(r'[^a-z]', '', ((self.faker.first_name()[0]) + self.faker.last_name()).lower())
            return username

        elif value_type == 'last_name':
            return self.faker.last_name()

        elif value_type == 'address':
            return re.sub(r"\n", " ", faker.address())

        elif value_type == 'street_address':
            return self.faker.street_address()

        elif value_type == 'secondary_address':
            return self.faker.secondary_address()

        elif value_type == 'city':
            return self.faker.city()

        elif value_type == 'postcode':
            return self.faker.postcode()

        elif value_type == 'company':
            return self.faker.company()

        elif value_type == 'ip':
            return self.faker.ipv4_private()

        elif value_type == 'url':
            return self.faker.url()

        elif value_type == 'sortcode':
            return "0000" + self.random_string(2, self.NUMERICS)

        elif value_type == 'bank_account':
            return "00000" + self.random_string(3, self.NUMERICS)

        elif value_type == 'mobile':
            return "07700900" + self.random_string(3, self.NUMERICS)
            
        elif value_type == 'uk_landline':
            return "01632" + self.random_string(6, self.NUMERICS)

        elif value_type == 'NULL':
            return None
            
    def random_string(self, length, chars = None):
        chars = self.ALPHA + self.NUMERICS + self.OTHER_CHARS if chars is None else chars
        return ''.join(random.choice(chars) for i in range(length))

    def _row_not_excluded(self, row, unless):
        for column, value in unless.items():
            actual = row.get(column, None)
            if actual != value :
                return True
        return False
