# Py_Obfuscate

A module for obfuscating a mysqldump file

This project is a partial-port of <a href="https://github.com/mavenlink/my_obfuscate">My_Obfusicate</a>. Under the hood it mostly uses <a href="https://faker.readthedocs.io/en/stable/">Faker</a> for generating fake data.

## Example usage
This package exposes a `py_obfuscate` module which contains `Obfuscator` class with a very simple inteface.
It expects two streams: a read string (e.g. the mysqldump file) and write stream (e.g. the file to write the obfuscated dump to).

```
obfuscate.obfuscate(streamIn, streamOut)
```

As a more practical example, create the file `obfuscate.py`

```
import sys
import yaml
import py_obfuscate

config = yaml.safe_load(open("obfuscator.yaml"))
obfuscate = py_obfuscate.Obfuscator(config)

src = sys.stdin
out = sys.stdout

obfuscate.obfuscate(src, out)
```

Now create a config file (`obfuscate.yaml`), e.g.:

```
tables:
  users:
    name:
      type: "name"
    email:
      type: "email"
    accountno:
      type: "string"
      chars: "1234567890"
      length: 10
```

You should change this config to reflect the tables and columns you wish to obfuscate.

Now you can run:

```
mysqldump -c --add-drop-table --hex-blob -u user -ppassword database | python obfuscate.py > obfuscated_dump.sql
```

**Note** that the `-c` option on mysqldump is *required* to use py_obfuscate. Additionally, the default behavior of mysqldump is to output special characters. This may cause trouble, so you can request hex-encoded blob content with `–hex-blob`. If you get MySQL errors due to very long lines, try some combination of `–max_allowed_packet=128M`, `–single-transaction`, `–skip-extended-insert`, and `–quick`.

## Configuration

In the above example we've used YAML as the configuration format; since you pass `py_obfuscate.Obfuscator` an config object (dictionary) you can
use any format you wish, so long as parses into the same structure. The basic structure is:

```
locale: <local string (optional): defaults "en_GB">
tables:
  <table>:
    truncate: <boolean - set to true to remove insert for this table. Defaults `false`>
    <column>:
      type: <type - how to obfusciate this column>
      <type-specific-option>: <type-specific-option-value> 
```

Tables or columns which are ommitted from the config are ignored. Currently no warning is given.

### Locale
* **type:** string
* **default:** `"en_GB"`

This is the locale string passed to <a href="https://faker.readthedocs.io/en/stable/">Faker</a>. 

### Truncate

Setting `truncate: true` for a table will remove the insert from the mysqldump.

### Types

These are the following types supported:

#### string 

**Options:**
* `chars` (string) The character list to choose from (defaults `"1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_+-=[{]}/?|!@#$%^&*()``~"`)
* `length` (integer) The length of the string (defaults `10`)

#### fixed 

**Options:**
* `value` (string|array) Replace column entries with this value or one of the values in the specified array (defaults `""`)

#### integer 

**Options:**
* `min` (string) Replace column entries with a random integer greater than or equal to this value (defaults `0`)
* `max` (string) Replace column entries with a random integer less than or equal to this value (defaults `100`)

#### email

#### name

#### first_name

#### last_name

#### username

#### address

#### street_address

#### secondary_address

#### city

#### postcode

#### company

#### ip

#### url

#### sortcode

#### bank_account

#### mobile

#### uk_landline

#### null


## Unit testes

    python -m unittest discover -s py_obfuscate


## License

This work is provided under the MIT License. See the included LICENSE file.
