import re
import collections
from py_obfuscate.insertstatement import InsertStatement

class MySql:
    insert_regex = r"^\s*INSERT\s*(IGNORE )?\s*INTO `(.*?)` \((.*?)\) VALUES\s*"

    def is_insert(self, string):
        if re.match(self.insert_regex, string, re.IGNORECASE):
            return True
        else:
            return False

class InsertStatement(InsertStatement):
    
    insert_regex = r"^\s*INSERT\s*(IGNORE )?\s*INTO `(.*?)` \((.*?)\) VALUES(.*);"

    def __init__(self, insertString):
        match = re.match(self.insert_regex, insertString, re.IGNORECASE)
        self.is_insert_ignore = match.group(1) is None
        self.table_name = match.group(2)
        self.columns = [self.__trim(x) for x in match.group(3).split(',')]
        self.inserts = self.__parseInserts(match.group(4))

    def __trim(self,x):
        return x.strip('` ')

    def get_inserts(self):
        return self.inserts

    def table(self):
        return self.table_name

    def empty(self):
        self.inserts = []

    def __iter__(self):
        yield from self.inserts

    def __parseInserts(self, insertsString):

        rows = []
        row = collections.OrderedDict()
        current_field = None
        column = 0
        
        escaped = False
        in_quoted_string = False
        in_row_string = False

        for c in insertsString:

            if escaped: 
                escaped = False
                current_field = "" if current_field is None else current_field
                current_field += c
            
            elif c == "\\":
                escaped = True
                #current_field = "" if current_field is None else current_field
                #current_field += c
            
            elif c == "(" and not in_quoted_string and not in_row_string:
                in_row_string = True
            
            elif c == ")" and not in_quoted_string and in_row_string:
                if current_field is not None:
                    row[self.columns[column]] = current_field
                    column += 1
                rows.append(row)
                column = 0
                row = collections.OrderedDict()
                current_field = None
                in_row_string = False
            
            elif c == "'" and not in_quoted_string:
                in_quoted_string = True
                current_field = ''
            
            elif c == "'" and in_quoted_string:
                in_quoted_string = False
                if current_field is not None:
                    row[self.columns[column]] = current_field
                    column += 1
                current_field = None
            
            elif c == "," and not in_quoted_string and in_row_string:
                in_quoted_string = False
                if current_field is not None:
                    row[self.columns[column]] = current_field
                    column += 1
                current_field = None
            
            elif c == "L" and not in_quoted_string and in_row_string and current_field == "NUL":
                current_field = None
                row[self.columns[column]] = current_field
                column += 1

            elif (c == " " or  c == "\t") and not in_quoted_string:
                # Don't add whitespace not in a string
                pass
            elif in_row_string:
                current_field = "" if current_field is None else current_field
                current_field += c
        
        return rows

    def to_string(self):

        if len(self.inserts) == 0:
            return ""

        column_string_list = self._columns_to_string()
        values_string_list = self._values_to_string()
        return "INSERT INTO `{}` ({}) VALUES {};".format(
            self.table_name,
            column_string_list,
            values_string_list 
        )

    def _columns_to_string(self):
        return "`" + ("`,`".join(self.columns)) + "`"
        
    def _values_to_string(self):
        row_strings = []
        for row in self.inserts:
            field_strings = []
            for field, value in row.items():
                if value is None:
                    field_strings.append("NULL")
                else:
                    field_strings.append("'" + self._escape(value) + "'")
            row_strings.append( "(" + (",".join(field_strings)) + ")" )

        return ",".join(row_strings)

    def _escape(self, string):
        return string.replace("'", "\\'")