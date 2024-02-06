************* Module bettyfixer.autoprototype
bettyfixer/autoprototype.py:12: [C0301(line-too-long), ] Line too long (124/100)
bettyfixer/autoprototype.py:28: [C0301(line-too-long), ] Line too long (123/100)
bettyfixer/autoprototype.py:36: [C0301(line-too-long), ] Line too long (106/100)
bettyfixer/autoprototype.py:44: [C0301(line-too-long), ] Line too long (143/100)
bettyfixer/autoprototype.py:53: [C0301(line-too-long), ] Line too long (199/100)
bettyfixer/autoprototype.py:54: [C0303(trailing-whitespace), ] Trailing whitespace
bettyfixer/autoprototype.py:85: [C0303(trailing-whitespace), ] Trailing whitespace
bettyfixer/autoprototype.py:87: [C0303(trailing-whitespace), ] Trailing whitespace
bettyfixer/autoprototype.py:90: [W0311(bad-indentation), ] Bad indentation. Found 8 spaces, expected 4
bettyfixer/autoprototype.py:91: [W0311(bad-indentation), ] Bad indentation. Found 8 spaces, expected 4
bettyfixer/autoprototype.py:92: [W0311(bad-indentation), ] Bad indentation. Found 8 spaces, expected 4
bettyfixer/autoprototype.py:92: [C0325(superfluous-parens), ] Unnecessary parens after 'if' keyword
bettyfixer/autoprototype.py:93: [W0311(bad-indentation), ] Bad indentation. Found 12 spaces, expected 8
bettyfixer/autoprototype.py:94: [W0311(bad-indentation), ] Bad indentation. Found 8 spaces, expected 4
bettyfixer/autoprototype.py:94: [C0325(superfluous-parens), ] Unnecessary parens after 'elif' keyword
bettyfixer/autoprototype.py:95: [W0311(bad-indentation), ] Bad indentation. Found 12 spaces, expected 8
bettyfixer/autoprototype.py:96: [W0311(bad-indentation), ] Bad indentation. Found 8 spaces, expected 4
bettyfixer/autoprototype.py:97: [W0311(bad-indentation), ] Bad indentation. Found 12 spaces, expected 8
bettyfixer/autoprototype.py:98: [C0303(trailing-whitespace), ] Trailing whitespace
bettyfixer/autoprototype.py:98: [W0311(bad-indentation), ] Bad indentation. Found 12 spaces, expected 8
bettyfixer/autoprototype.py:99: [W0311(bad-indentation), ] Bad indentation. Found 16 spaces, expected 12
bettyfixer/autoprototype.py:100: [W0311(bad-indentation), ] Bad indentation. Found 16 spaces, expected 12
bettyfixer/autoprototype.py:1: [C0114(missing-module-docstring), ] Missing module docstring
bettyfixer/autoprototype.py:9: [C0116(missing-function-docstring), betty_check] Missing function or method docstring
bettyfixer/autoprototype.py:27: [C0116(missing-function-docstring), print_check_betty_first] Missing function or method docstring
bettyfixer/autoprototype.py:29: [C0116(missing-function-docstring), print_header_name_missing] Missing function or method docstring
bettyfixer/autoprototype.py:31: [C0116(missing-function-docstring), print_Ctags_header_error] Missing function or method docstring
bettyfixer/autoprototype.py:31: [C0103(invalid-name), print_Ctags_header_error] Function name "print_Ctags_header_error" doesn't conform to snake_case naming style
bettyfixer/autoprototype.py:34: [C0116(missing-function-docstring), check_ctags] Missing function or method docstring
bettyfixer/autoprototype.py:42: [C0116(missing-function-docstring), generate_tags] Missing function or method docstring
bettyfixer/autoprototype.py:44: [W1309(f-string-without-interpolation), generate_tags] Using an f-string that does not have any interpolated variables
bettyfixer/autoprototype.py:49: [C0116(missing-function-docstring), filter_tags] Missing function or method docstring
bettyfixer/autoprototype.py:53: [C0209(consider-using-f-string), filter_tags] Formatting a regular string which could be an f-string
bettyfixer/autoprototype.py:59: [R1705(no-else-return), filter_tags] Unnecessary "else" after "return", remove the "else" and de-indent the code inside it
bettyfixer/autoprototype.py:60: [W1514(unspecified-encoding), filter_tags] Using open without explicitly specifying an encoding
bettyfixer/autoprototype.py:69: [C0116(missing-function-docstring), create_header] Missing function or method docstring
bettyfixer/autoprototype.py:73: [W1514(unspecified-encoding), create_header] Using open without explicitly specifying an encoding
bettyfixer/autoprototype.py:78: [C0116(missing-function-docstring), delete_files] Missing function or method docstring
bettyfixer/autoprototype.py:79: [C0209(consider-using-f-string), delete_files] Formatting a regular string which could be an f-string
bettyfixer/autoprototype.py:83: [C0116(missing-function-docstring), check_header_file] Missing function or method docstring
bettyfixer/autoprototype.py:89: [C0116(missing-function-docstring), autoproto] Missing function or method docstring
bettyfixer/autoprototype.py:96: [C0121(singleton-comparison), autoproto] Comparison 'generate_tags(directory) != False' should be 'generate_tags(directory) is not False' if checking for the singleton value False, or 'generate_tags(directory)' if testing for truthiness
bettyfixer/autoprototype.py:98: [C0121(singleton-comparison), autoproto] Comparison 'filtered_tags != None' should be 'filtered_tags is not None'
bettyfixer/autoprototype.py:6: [C0411(wrong-import-order), ] standard import "import glob" should be placed before "from colorama import Fore"
bettyfixer/autoprototype.py:1: [W0611(unused-import), ] Unused import argparse
bettyfixer/autoprototype.py:4: [W0611(unused-import), ] Unused import re


## Report
======
**79 statements analysed.**

Statistics by type
------------------

|type     |number |old number |difference |%documented |%badname |
|---------|-------|-----------|-----------|------------|---------|
|module   |1      |NC         |NC         |0.00        |0.00     |
|class    |0      |NC         |NC         |0           |0        |
|method   |0      |NC         |NC         |0           |0        |
|function |11     |NC         |NC         |0.00        |9.09     |



External dependencies
---------------------
::

    colorama (bettyfixer.autoprototype)



102 lines have been analyzed

Raw metrics
-----------

|type      |number |%     |previous |difference |
|----------|-------|------|---------|-----------|
|code      |82     |80.39 |NC       |NC         |
|docstring |0      |0.00  |NC       |NC         |
|comment   |5      |4.90  |NC       |NC         |
|empty     |15     |14.71 |NC       |NC         |



Duplication
-----------

|                         |now   |previous |difference |
|-------------------------|------|---------|-----------|
|nb duplicated lines      |0     |NC       |NC         |
|percent duplicated lines |0.000 |NC       |NC         |



Messages by category
--------------------

|type       |number |previous |difference |
|===========|=======|=========|===========|
|convention |29     |NC       |NC         |
|refactor   |1      |NC       |NC         |
|warning    |16     |NC       |NC         |
|error      |0      |NC       |NC         |



Messages
--------

| message id                     | occurrences |
|--------------------------------|-------------|
| missing-function-docstring     | 11          |
| bad-indentation                | 11          |
| line-too-long                  | 5           |
| trailing-whitespace            | 4           |
| unused-import                  | 2           |
| unspecified-encoding           | 2           |
| superfluous-parens             | 2           |
| singleton-comparison           | 2           |
| consider-using-f-string        | 2           |
| wrong-import-order             | 1           |
| no-else-return                 | 1           |
| missing-module-docstring       | 1           |
| invalid-name                   | 1           |
| f-string-without-interpolation | 1           |




-----------------------------------
Your code has been rated at 4.18/10

