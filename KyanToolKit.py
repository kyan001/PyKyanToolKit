# -*- coding: utf-8 -*-
##################################################################
# By Kyan
##################################################################
import os
import sys
import time
import getpass
import subprocess
import shlex
import urllib.request
import hashlib
import json
import io
from functools import wraps
import difflib

import consoleiotools as cit


class KyanToolKit(object):
    __version__ = '6.3.0'

    def __init__(self, trace_file="trace.xml"):
        self.trace_file = trace_file

    def __del__(self):
        pass

# -Decorators-----------------------------------------------------
    def inTrace(self, func: callable):  # decorator
        """将被修饰函数的进入和退出写入日志"""
        @wraps(func)
        def call(*args, **kwargs):
            self.TRACE("Enter " + func.__qualname__ + "()")
            result = func(*args, **kwargs)
            self.TRACE("Leave " + func.__qualname__ + "()")
            return result
        return call

# -Text Process---------------------------------------------------
    @staticmethod
    def banner(content_="Well Come"):
        """生成占3行的字符串"""
        # char def
        sp_char = "#"
        # length calc
        itsays = content_.strip()
        effective_length = int(len(itsays))
        # gen contents
        side_space = ' ' * int(effective_length * ((1 - 0.618) / 0.618) / 2)
        content_line = sp_char + side_space + itsays + side_space + sp_char
        content_line_length = len(content_line)
        banner_border = sp_char * content_line_length
        return banner_border + '\n' + content_line + '\n' + banner_border

    @staticmethod
    def md5(words=""):
        if type(words) != bytes:  # md5的输入必须为 bytes 类型
            words = str(words).encode()
        return hashlib.md5(words).hexdigest()

# -Image Process--------------------------------------------------
    @staticmethod
    def imageToColor(url: str, scale=200, mode='rgb'):
        """将 url 指向的图片提纯为一个颜色"""
        from PIL import Image
        import colorsys
        if url:
            response = urllib.request.urlopen(url)
            img_buffer = io.BytesIO(response.read())
            img = Image.open(img_buffer)
            img = img.convert('RGBA')
            img.thumbnail((scale, scale))
            statistics = {'r': 0, 'g': 0, 'b': 0, 'coef': 0}
            for cnt, (r, g, b, a) in img.getcolors(img.size[0] * img.size[1]):
                hsv = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
                saturation = hsv[1] * 255
                coefficient = (saturation * cnt * a) + 0.01  # avoid 0
                statistics['r'] += coefficient * r
                statistics['g'] += coefficient * g
                statistics['b'] += coefficient * b
                statistics['coef'] += coefficient
                color = (
                    int(statistics['r'] / statistics['coef']),
                    int(statistics['g'] / statistics['coef']),
                    int(statistics['b'] / statistics['coef'])
                )
            if mode.lower() == 'rgb':
                return color
            elif mode.lower() == 'hex':
                return "#%0.2X%0.2X%0.2X" % color
            else:
                return color
        else:
            return False

# -System Fucntions-----------------------------------------------
    @staticmethod
    def clearScreen():
        """Clear the screen"""
        if "win32" in sys.platform:
            os.system('cls')
        elif "linux" in sys.platform:
            os.system('clear')
        elif 'darwin' in sys.platform:
            os.system('clear')
        else:
            cit.err("No clearScreen for " + sys.platform)

    @staticmethod
    def getPyCmd():
        """get OS's python command"""
        if sys.platform.startswith('win'):
            return 'py'
        elif "linux" in sys.platform:
            return 'python3'
        elif 'darwin' in sys.platform:
            return 'python3'
        else:
            cit.err("No python3 command for " + sys.platform)

    @staticmethod
    def runCmd(cmd):
        """run command and show if success or failed

        Args:
            cmd: string
        Returns:
            bool: Does this command run successfully
        """
        cit.echo(cmd, "command")
        result = os.system(cmd)
        if not result:
            cit.warn("Command Failed")

    @staticmethod
    def readCmd(cmd):
        """run command and return the str format stdout

        Args:
            cmd: string
        Returns:
            str: what the command's echo
        """
        cit.echo(cmd, "command")
        args = shlex.split(cmd)
        proc = subprocess.Popen(args, stdout=subprocess.PIPE)
        (proc_stdout, proc_stderr) = proc.communicate(input=None)  # proc_stdin
        return proc_stdout.decode()  # stdout & stderr is in bytes format

    @staticmethod
    def isCmdExist(cmd):
        """test if command is available for execution

        Args:
            cmd: string
        Returns:
            bool: if the command is exist
        """
        proc = os.popen("command -v {}".format(cmd))
        result = proc.read()
        proc.close()
        return (result != "")

    @staticmethod
    def getDir(file_) -> (str, str):
        """Get file dir's dirname and dir's basename.

        If file located at /path/to/filedir/file, then the dirname is "/path/to/filedir", and basename is "filedir"

        Args:
            file_: str. Local filename. Normally it's __file__

        Returns:
            str: File dir's path.
            str: File dir's basename.
        """
        dirname = os.path.dirname(os.path.abspath(file_))
        basename = os.path.basename(dirname)
        return dirname, basename

    @staticmethod
    def diff(a, b, force_str=False, context=0) -> list:
        """Compare two strings/lists or files and return their diffs.

        Args:
            a: str/list/file. The source of comparison.
            b: str/list/file. The target of comparison.
            force_str: bool. Set to `True` if you wanna force to compare `a` and `b` as string. Default is False.
            context: int. Number of context lines returns with diffs. Default is 0, no context lines shows.

        Returns:
            list: Diffs where the dst is not same as src. Only lines with diffs in the result. The first 2 lines are the header of diffs.
        """
        src, dst = {'raw': a}, {'raw': b}
        for d in (src, dst):
            if isinstance(d['raw'], str):
                if (not force_str) and os.path.isfile(d['raw']):
                    d['label'] = os.path.basename(d['raw'])  # filename will show in header of diffs
                    with open(d['raw'], encoding='utf-8') as f:
                        d['content'] = f.readlines()
                else:
                    d['label'] = str(str)
                    d['content'] = d['raw'].split('\n')  # convert str to list for comparison. Ex. ['str',]
            else:
                d['label'] = str(type(d['raw']))
                d['content'] = d['raw']
        diffs = difflib.unified_diff(src['content'], dst['content'], n=context, fromfile=src['label'], tofile=dst['label'])
        return [ln.strip('\n') for ln in diffs]  # Ensure no \n returns

    @staticmethod
    def updateFile(file_, url):
        """Check and update file compares with remote_url

        Args:
            file_: str. Local filename. Normally it's __file__
            url: str. Remote url of raw file content. Normally it's https://raw.github.com/...
        Returns:
            bool: file updated or not
        """
        def compare(s1, s2):
            return s1 == s2, len(s2) - len(s1)

        if not url or not file_:
            return False
        try:
            req = urllib.request.urlopen(url)
            raw_codes = req.read()
            with open(file_, 'rb') as f:
                current_codes = f.read().replace(b'\r', b'')
            is_same, diff = compare(current_codes, raw_codes)
            if is_same:
                cit.info("{} is already up-to-date.".format(file_))
                return False
            else:
                cit.ask("A new version is available. Update? (Diff: {})".format(diff))
                if cit.get_choice(['Yes', 'No']) == 'Yes':
                    with open(file_, 'wb') as f:
                        f.write(raw_codes)
                    cit.info("Update Success.")
                    return True
                else:
                    cit.warn("Update Canceled")
                    return False
        except Exception as e:
            cit.err("{f} update failed: {e}".format(f=file_, e=e))
            return False

# -Get Information------------------------------------------------
    @staticmethod
    def ajax(url, param={}, method='get'):
        """Get info by ajax

        Args:
            url: string
        Returns:
            dict: json decoded into a dict
        """
        param = urllib.parse.urlencode(param)
        if method.lower() == 'get':
            req = urllib.request.Request(url + '?' + param)
        elif method.lower() == 'post':
            param = param.encode('utf-8')
            req = urllib.request.Request(url, data=param)
        else:
            raise Exception("invalid method '{}' (GET/POST)".format(method))
        rsp = urllib.request.urlopen(req)
        if rsp:
            rsp_json = rsp.read().decode('utf-8')
            rsp_dict = json.loads(rsp_json)
            return rsp_dict
        return None

    @staticmethod
    def readFile(filepath):
        """Try different encoding to open a file in readonly mode"""
        for mode in ("utf-8", 'gbk', 'cp1252', 'windows-1252', 'latin-1'):
            try:
                with open(filepath, mode='r', encoding=mode) as f:
                    content = f.read()
                    cit.info('以 {} 格式打开文件'.format(mode))
                    return content
            except UnicodeDecodeError:
                cit.warn('打开文件：尝试 {} 格式失败'.format(mode))
        return None


# -Pre-checks---------------------------------------------------
    @staticmethod
    @cit.as_session("Platform Check")
    def needPlatform(expect_platform: str):
        cit.info("Need: " + expect_platform)
        cit.info("Current: " + sys.platform)
        if expect_platform not in sys.platform:
            cit.bye("Platform Check Failed")

    @staticmethod
    @cit.as_session("User Check")
    def needUser(expect_user: str):
        cit.info("Need: " + expect_user)
        cit.info("Current: " + KyanToolKit.getUser())
        if KyanToolKit.getUser() != expect_user:
            cit.bye("User Check Failed")

# -Debug---------------------------------------------------------
    def TRACE(self, input_: str, trace_type='INFO'):
        trace_content = ''.join(input_)
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        current_function = sys._getframe().f_back
        current_function_name = current_function.f_code.co_name
        current_line = current_function.f_code.co_firstlineno
        current_filename = current_function.f_code.co_filename
        trace_header = '\n<{type} FILE="{file}" LINE="{line}" TIME="{time}" FUNC="{func}()">\n'.format(
            type=trace_type, file=current_filename, line=str(current_line),
            time=current_time, func=current_function_name
        )
        with open(self.trace_file, 'a') as trace:
            trace.write(trace_header + trace_content + "\n</" + trace_type + ">\n")


# -Internal Uses-------------------------------------------------
    @staticmethod
    def getUser():
        return getpass.getuser()
