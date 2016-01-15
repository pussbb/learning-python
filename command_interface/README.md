**Usage:**
```python
>>> ShellCommand('java', '-version') > 'some_file'
java -version > some_file
>>> 
>>> ShellCommand('java', '-version', file_='asasa'),
java -version file_=asasa
>>> 
>>> ShellCommand('java', '-version', '2>&1')
java -version '2>&1'
>>>
>>> ShellCommand('java', '-version') >> 'some_file'
java -version >> some_file
>>> 
>>> ShellCommand('java', '-version') < 'some_file'
java -version < some_file
>>> 
>>> ShellCommand('java', '-version') & ShellCommand('something')
java -version && something
>>> 
>>> ShellCommand('java', '-version', ShellIORedirection.error_to_out()) + ShellCommand('grep', 'version')
java -version 2>&1 | grep version
>>>
>>> ShellCommand('java', '-version') + ShellIORedirection.error_to_out()
java -version 2>&1
>>> 

```

**Execute command and get executable full path at runtime**
```python
>>> using_command_full_path('java')
$(type -P java)
>>> 
>>> using_command_full_path('java', use_which=True)
$(which java)
>>> 

```

**Execute**
```python
result = ShellCommand('java', '-version').execute()
print(result)
#  output
#  Command exit code 0. Response: b' ......'

#  get command exit code 
print(result.exit_code)

#  get command response
print(result.response)

#  get command response as iterable
print(list(response)
print([line for line in response])
```

**Get command output at runtime**
```python
def handler(line):
    print('got line', line)

cmd = ShellCommand('java', '-version')
cmd.execute(handler=handler)
```

**Raises**
 -  ShellCommandRuntimeException if command ended with nonzero exit code
 -  ShellCommandNotFound if command not found


**Bugs** :
ShellCommandNotFound not always raises because by default it tries to get full path of executable using $(type -P smth). 


