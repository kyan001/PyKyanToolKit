# KyanToolKit
[![Build Status](https://travis-ci.org/kyan001/PyKyanToolKit.svg?branch=master)](https://travis-ci.org/kyan001/PyKyanToolKit)

A console toolkit for common uses

```python
>>> import KyanToolKit

# static methods
>>> ktk = KyanToolKit.KyanToolKit
>>> ktk.__version__
'6.0.1'

>>> Print(ktk.banner("KyanToolKit"))  # generate banner for text
###################
#   KyanToolKit   #
###################

>>> ktk.md5("KyanToolKit")  # return md5 hash for text.
'a7599cb70a39f9d9d18a76608bf21d4e'

>>> ktk.imageToColor('http://image-url/image')  # get theme color of image.
(152, 156, 69)  # RGB value

>>> ktk.imageToColor('http://image-url/image', scale=500)  # cost more time to generate a preciser color. default scale is 200.
(152, 156, 69)

>>> ktk.imageToColor('http://image-url/image', mode='hex')  # return color in hex. default mode is 'rgb'.
'#989C45'

>>> ktk.clearScreen()  # clear the console.

>>> ktk.getPyCmd()  # get python running command for different OS.
'python3'

>>> ktk.checkResult(result)  # check unix command result. 0 means OK.
| (Result) Done

>>> ktk.runCmd("echo hello")  # run console command.
*
| __RUN COMMAND__________________________
| (Command) echo hello
hello
| (Result) Done
`

>>> ktk.readCmd("echo hello")  # run and read the output of a command.
'hello\n'

>>> ktk.isCmdExist("ls")  # test if command is exist.
True

>>> ktk.updateFile('file', 'http://file-url')  # update file if the file is not as same as url content.

>>> ktk.ajax('http://ajax-url')  # start a ajax request.
{'result': 'data'}  # as python dict

>>> ktk.ajax('http://ajax-url', {'data': 'value'})  # ajax request with param.
{'result': 'data'}

>>> ktk.ajax('http://ajax-url', method='post')  # ajax request using post. default if 'get'.
{'result': 'data'}

>>> ktk.readFile('file')  # read file using different encoding automatically.
"file content"

>>> ktk.needPlatform("linux")  # continue if platform is need. else quit.
*
| __PLATFORM CHECK__________________________
| (Info) Need: linux
| (Info) Current: linux
`

>>> ktk.needUser('user')  # continue if user is correct.
*
| __USER CHECK__________________________
| (Info) Need: user
| (Info) Current: user001
User Check Failed

# Other methods
>>> ktk = KyanToolKit.KyanToolKit()

@ktk.in_trace
def func():
    print("Hello World")

>>> func()  # Calling informations are recorded in trace file
>>> ktk.TRACE("LOG THIS")  # Log word into trace file
>>> ktk.trace_file  # show trace file location
"trace.xml"
```
