************* Module bettyfixer.errors_extractor
bettyfixer/errors_extractor.py:1: [C0114(missing-module-docstring), ] Missing module docstring
bettyfixer/errors_extractor.py:4: [C0116(missing-function-docstring), exctract_errors] Missing function or method docstring
bettyfixer/errors_extractor.py:4: [W0621(redefined-outer-name), exctract_errors] Redefining name 'file_path' from outer scope (line 36)
bettyfixer/errors_extractor.py:13: [W0621(redefined-outer-name), exctract_errors] Redefining name 'errors_file_path' from outer scope (line 30)
bettyfixer/errors_extractor.py:13: [W1514(unspecified-encoding), exctract_errors] Using open without explicitly specifying an encoding
bettyfixer/errors_extractor.py:17: [W0107(unnecessary-pass), exctract_errors] Unnecessary pass statement
bettyfixer/errors_extractor.py:19: [W1514(unspecified-encoding), exctract_errors] Using open without explicitly specifying an encoding
bettyfixer/errors_extractor.py:30: [C0103(invalid-name), ] Constant name "errors_file_path" doesn't conform to UPPER_CASE naming style
bettyfixer/errors_extractor.py:33: [R1732(consider-using-with), ] Consider using 'with' for resource-allocating operations
bettyfixer/errors_extractor.py:33: [W1514(unspecified-encoding), ] Using open without explicitly specifying an encoding


## Report
------

**21 statements analysed.**

Statistics by type
------------------
 
|type     |number |old number |difference |%documented |%badname |
|---------|-------|-----------|-----------|------------|---------|
|module   |1      |NC         |NC         |0.00        |0.00     |
|class    |0      |NC         |NC         |0           |0        |
|method   |0      |NC         |NC         |0           |0        |
|function |1      |NC         |NC         |0.00        |0.00     |



**39 lines have been analyzed**

Raw metrics
-----------

|type      |number |%     |previous |difference |
|----------|-------|------|---------|-----------|
|code      |23     |58.97 |NC       |NC         |
|docstring |0      |0.00  |NC       |NC         |
|comment   |9      |23.08 |NC       |NC         |
|empty     |7      |17.95 |NC       |NC         |



Duplication
-----------

|                         |now   |previous |difference |
|-------------------------|------|---------|-----------|
|nb duplicated lines      |0     |NC       |NC         |
|percent duplicated lines |0.000 |NC       |NC         |



Messages by category
--------------------

|type       |number |previous |difference |
|-----------|-------|---------|-----------|
|convention |3      |NC       |NC         |
|refactor   |1      |NC       |NC         |
|warning    |6      |NC       |NC         |
|error      |0      |NC       |NC         |



Messages
--------

|message id                 |occurrences |
|---------------------------|------------|
|unspecified-encoding       |3           |
|redefined-outer-name       |2           |
|unnecessary-pass           |1           |
|missing-module-docstring   |1           |
|missing-function-docstring |1           |
|invalid-name               |1           |
|consider-using-with        |1           |

<br>



-----------------------------------
Your code has been rated at 5.24/10

