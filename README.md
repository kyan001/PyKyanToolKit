# KyanToolKit
[![Build Status](https://travis-ci.org/kyan001/PyKyanToolKit.svg?branch=master)](https://travis-ci.org/kyan001/PyKyanToolKit)

A console toolkit for common uses

```python
# Static Methods
>>> from KyanToolKit import KyanToolKit as ktk

>>> ktk.__version__
'6.2.1'

>>> Print(ktk.banner("KyanToolKit"))  # Generate banner for text
###################
#   KyanToolKit   #
###################

>>> ktk.md5("KyanToolKit")  # Return md5 hash for text.
'a7599cb70a39f9d9d18a76608bf21d4e'

>>> ktk.imageToColor('http://image-url/image')  # Get theme color of image.
(152, 156, 69)  # RGB value

>>> ktk.imageToColor('http://image-url/image', scale=500)  # Cost more time to generate a preciser color. default scale is 200.
(152, 156, 69)

>>> ktk.imageToColor('http://image-url/image', mode='hex')  # Return color in hex. default mode is 'rgb'.
'#989C45'

>>> ktk.clearScreen()  # Clear the console.

>>> ktk.getPyCmd()  # Get python running command for different OS.
'python3'

>>> ktk.checkResult(result)  # Check unix command result. 0 means OK.
| (Result) Done

>>> ktk.runCmd("echo hello")  # Run console command.
*
| __RUN COMMAND__________________________
| (Command) echo hello
hello
| (Result) Done
`

>>> ktk.readCmd("echo hello")  # Run and read the output of a command.
'hello\n'

>>> ktk.isCmdExist("ls")  # Test if command is exist.
True

>>> ktk.getDir("./file")  # Get file dir's path and basename.
("/path/to/filedir", "filedir")  # As python tuple.

>>> print("\n".join(ktk.diff(...)))  # .diff() returns list. Use "\n".join() to print.
>>> ktk.diff("str1", "str2")  # Compare 2 strings, return the list of diffs.
--- <class 'str'>
+++ <class 'str'>
@@ -1 +1 @@
-str1
+str2

>>> ktk.diff(["a", "b"], ["a", "b", "c"])  # Compare 2 lists and print diffs.
--- <class 'list'>
+++ <class 'list'>
@@ -2,0 +3 @@
+c

>>> ktk.diff(["a", "b"], ["a", "b", "c"], context=2)  # Show diffs with 2 extra context lines.
--- <class 'list'>
+++ <class 'list'>
@@ -1,2 +1,3 @@
 a  # context
 b  # context
+c  # diff

>>> ktk.diff("/path/to/file1", "/path/to/file2")  # Compare between 2 files.
--- file1
+++ file2
...

>>> ktk.diff("/path/to/file1", "str")  # Compare between file and str/list.
--- file1
+++ <class 'str'>
...

>>> if not ktk.diff('str', 'str'): print("No diff")  # If no diff, return [].
No diff

>>> ktk.updateFile('file', 'http://file-url')  # Update file if the file is not as same as url content.
False  # if already up-to-date.

>>> ktk.ajax('http://ajax-url')  # Start a AJAX request.
{'result': 'data'}  # As python dict.

>>> ktk.ajax('http://ajax-url', {'data': 'value'})  # AJAX request with param.
{'result': 'data'}

>>> ktk.ajax('http://ajax-url', method='post')  # AJAX request using post. default is 'get'.
{'result': 'data'}

>>> ktk.readFile('file')  # Read file using different encoding automatically.
"file content"

>>> ktk.needPlatform("linux")  # Continue if platform is need. else quit.
*
| __PLATFORM CHECK__________________________
| (Info) Need: linux
| (Info) Current: linux
`

>>> ktk.needUser('user')  # Continue if user is correct.
*
| __USER CHECK__________________________
| (Info) Need: user
| (Info) Current: user001
User Check Failed

# Non-static methods
>>> import KyanToolKit
>>> ktk = KyanToolKit.KyanToolKit()

@ktk.in_trace
def func():
    print("Hello World")

>>> func()  # Calling informations are recorded in trace file
>>> ktk.TRACE("LOG THIS")  # Log word into trace file
>>> ktk.trace_file  # Show trace file location
"trace.xml"
```
