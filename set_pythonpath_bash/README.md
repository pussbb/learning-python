 
As we all known if we want to run python script as shell script we would need to do following
```shell
#!/user/bin/env python
# bellow our python script
```

but what if you need to add your own path (with your python modules) into python's default search path for module files. 
Of cause you could do using python language
```python
import os
os.path.append('some/path/to/your/lib_folder')
```

But if I don't want to it in python script? In this case you could try 
```shell
#!/user/bin/env PYTHONPATH="$PYTHONPATH:$OUR_PY_LIB_PATH" python
```
but it won't work because linux/unix shebang(#!) will pass only first argument  PYTHONPATH='ssss' and when you will try to execute you script
```shell
./some_script
```
it simply won't work - it will hangs and never wont exit until you kill it. 
Please note that 
```shell
# /user/bin/env PYTHONPATH="$PYTHONPATH:$OUR_PY_LIB_PATH" python
```
will work fine. 

And it seems that there is no other option to add your into PYTHONPATH 
except doing it at python script. 
But its not . Here is an alternative version how to set path into PYTHONPATH before executing python code
```shell
#!/bin/bash
''':'
function get_real_path() {
    [ -n "$(type -p realpath)" ] && $(type -p realpath) "$1" || $(type -p readlink) -f "$1"
}
REAL_SCRIPT_PATH=$(get_real_path `dirname $0`)
OUR_PY_LIB_PATH=$(get_real_path "$REAL_SCRIPT_PATH/../lib/")
exec env PYTHONPATH="$PYTHONPATH:$OUR_PY_LIB_PATH" python "$0"
'''
# -*- coding: utf-8 -*-
....
'''
```
To execute your application with additional arguments ... you need to add
''':' after shebang , write your bash command's, exec your command with args and at the end add '''.

in my example.
Lets imaging that we have structure like this:
```shell
some_demo_app# ls
... .  - current folder
... lib  - folder with some 3rd party modules 
... README - simple file
... src - folder which contains our script
```

 if you execute it you would see something like this
```shell 
~#some_demo_app/src/conf;echo $?
sjsjs
4
```
- 'sjsjs' - string from /some_demo_app/lib/sxadis.py which prints in 
/some_demo_app/src/conf
- 4 - exit status (echo $?)

**under the hood**
This function will return absolute path. Please note that realpath is missing at old OS (for example Centos 6) , readlink - is deprecated where realpath is present. Generally speaking this function will rwork at  Centso 6 and Centos 7 .... 
```shell
function get_real_path() {
    [ -n "$(type -p realpath)" ] && $(type -p realpath) "$1" || $(type -p readlink) -f "$1"
}
```
than lets determine real scirp path and path to our lib folder
```shell
REAL_SCRIPT_PATH=$(get_real_path `dirname $0`)
OUR_PY_LIB_PATH=$(get_real_path "$REAL_SCRIPT_PATH/../lib/")
```
and the end just execute python  script
```shell
exec env PYTHONPATH="$PYTHONPATH:$OUR_PY_LIB_PATH" python "$0"
```
Here I'm using 'env' because its simpler to set environment variable for application (there is no need to do `export ....` ) , and it will look for Python Interpreter (at some systems it can be at /usr/local/bin, /usr/bin/ ...) 
and specify file "$0" (this file)

and that's it . lib folder added to search modules search path list .


