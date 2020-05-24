#!/usr/bin/env python3
##################################################################
# For KTK
##################################################################
import sys
import os
import unittest
import getpass

import FakeOut
import FakeIn
import FakeOs

ktk_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ktk_dir)
import KyanToolKit  # noqa


class test_KyanToolKit(unittest.TestCase):
    '''
    KyanToolKit.py Unit Tests
    '''
    ktk_version = '6.3.1'

    def setUp(self):
        self.ktk = KyanToolKit.KyanToolKit
        self.ktk_inst = KyanToolKit.KyanToolKit()
        # redirect stdout
        self.console_out = sys.stdout
        self.fakeout = FakeOut.FakeOut()
        sys.stdout = self.fakeout
        # redirect stdin
        self.console_in = sys.stdin
        self.fakein = FakeIn.FakeIn()
        sys.stdin = self.fakein
        # monkey patch
        self.os_system = os.system
        self.fakeos = FakeOs.FakeOs()
        os.system = self.fakeos.system

    def tearDown(self):
        # clean fakin/out buffer
        self.fakeout.clean()
        self.fakein.clean()
        self.fakeos.clean()
        # set back stdin/out to console
        sys.stdout = self.console_out
        sys.stdin = self.console_in
        os.system = self.os_system

    def test_version(self):
        self.assertEqual(self.ktk_version, self.ktk.__version__)

    def test_init(self):
        'testing __init__()'
        self.assertTrue(self.ktk_inst.trace_file)

    def test_banner(self):
        expect_word = '###############\n#  Test Text  #\n###############'
        self.assertEqual(expect_word, self.ktk.banner("Test Text"))

    def test_md5_string(self):
        md5 = self.ktk.md5("Test Text")
        self.assertEqual(md5, 'f1feeaa3d698685b6a6179520449e206')

    def test_md5_int(self):
        md5 = self.ktk.md5(123)
        self.assertEqual(md5, '202cb962ac59075b964b07152d234b70')

    def test_md5_bytes(self):
        md5 = self.ktk.md5(b'Test Text')
        self.assertEqual(md5, 'f1feeaa3d698685b6a6179520449e206')

    def test_imageToColor_rgb(self):
        test_url = "http://www.kyan001.com/static/img/index/div_card_products.png"
        color = self.ktk.imageToColor(test_url)
        self.assertEqual(color, (5, 147, 208))

    def test_imageToColor_hex(self):
        test_url = "http://www.kyan001.com/static/img/index/div_card_products.png"
        color = self.ktk.imageToColor(test_url, mode='hex')
        self.assertEqual(color, '#0593D0')

    def test_clearScreen(self):
        self.ktk.clearScreen()
        self.assertTrue(self.fakeos.readline() in 'cls clear')

    def test_getPyCmd(self):
        result = self.ktk.getPyCmd()
        self.assertTrue(result in ('py', 'python3'))

    def test_runCmd(self):
        self.ktk.runCmd("echo Test Text")
        self.assertEqual(self.fakeos.readline(), "echo Test Text")

    def test_readCmd(self):
        self.assertEqual(self.ktk.readCmd(r"echo Test Text"), "Test Text\n")

    def test_getUser(self):
        self.assertEqual(self.ktk.getUser(), getpass.getuser())

    @unittest.skipIf(os.name == 'nt', 'Only in posix')
    def test_isCmdExist(self):
        self.assertFalse(self.ktk.isCmdExist("notexist"))
        self.assertTrue(self.ktk.isCmdExist("ls"))

    def test_ajax_get(self):
        url = 'https://yesno.wtf/api'
        param = {'force': 'yes'}
        result = self.ktk.ajax(url, param, 'get')
        answer = result.get('answer')
        self.assertEqual(answer, 'yes')

    def test_readFile(self):
        filepath = os.path.join(ktk_dir, 'tests', 'test_KyanToolKit.py')
        content = self.ktk.readFile(filepath)
        self.assertTrue(content is not None)

    def test_updateFile(self):
        url = 'https://raw.githubusercontent.com/kyan001/PyKyanToolKit/master/tests/testfile'
        filepath = os.path.join(ktk_dir, 'tests', 'testfile')
        result = self.ktk.updateFile(filepath, url)
        expect = 'testfile is already up-to-date.'
        self.assertFalse(result)
        self.assertTrue(expect in self.fakeout.readline())

    def test_getDir(self):
        dirname, basename = self.ktk.getDir(__file__)
        self.assertTrue(dirname.endswith('tests'))
        self.assertEqual(basename, "tests")

    def test_diff_same(self):
        diffs = self.ktk.diff("test", "test")
        self.assertFalse(diffs)

    def test_diff_str(self):
        a, b = "test1", "test2"
        expect_diff = [
            "--- <class 'str'>",
            "+++ <class 'str'>",
            '@@ -1 +1 @@',
            '-test1',
            '+test2'
        ]
        self.assertEqual(self.ktk.diff(a, b), expect_diff)

    def test_diff_list(self):
        a, b = ["a", "c"], ["b", "c"]
        expect_diff = [
            "--- <class 'list'>",
            "+++ <class 'list'>",
            '@@ -1 +1 @@',
            '-a',
            '+b'
        ]
        self.assertEqual(self.ktk.diff(a, b), expect_diff)

    def test_diff_context(self):
        a, b = ["a", "c"], ["b", "c"]
        expect_diff = [
            "--- <class 'list'>",
            "+++ <class 'list'>",
            '@@ -1,2 +1,2 @@',
            '-a',
            '+b',
            ' c'
        ]
        self.assertEqual(self.ktk.diff(a, b, context=1), expect_diff)

    def test_diff_file(self):
        a = os.path.join(ktk_dir, 'tests', 'testfile')
        b = "This file should not changed too"
        expect_diff = [
            '--- testfile',
            "+++ <class 'str'>",
            '@@ -1 +1 @@',
            '-This file should not changed',
            '+This file should not changed too'
        ]
        self.assertEqual(self.ktk.diff(a, b), expect_diff)

    def test_diff_files(self):
        a = os.path.join(ktk_dir, 'tests', 'testfile')
        b = os.path.join(ktk_dir, 'tests', 'testfile2')
        expect_diff = [
            '--- testfile',
            '+++ testfile2',
            '@@ -1 +1 @@',
            '-This file should not changed',
            '+This file should not changed too'
        ]
        self.assertEqual(self.ktk.diff(a, b), expect_diff)

    def test_diff_force_str(self):
        a = os.path.join(ktk_dir, 'tests', 'testfile')
        b = os.path.join(ktk_dir, 'tests', 'testfile2')
        expect_diff_partial = [
            "--- <class 'str'>",
            "+++ <class 'str'>",
            '@@ -1 +1 @@'
        ]
        for li in expect_diff_partial:
            self.assertTrue(li in self.ktk.diff(a, b, force_str=True))

    def test_needPlatform(self):
        self.ktk.needPlatform(sys.platform)
        expect_word_need = "Need: {0}".format(sys.platform)
        expect_word_current = "Current: {0}".format(sys.platform)
        test_output = self.fakeout.readline()
        self.assertTrue(expect_word_need in test_output)
        self.assertTrue(expect_word_current in test_output)

    def test_needUser(self):
        current_user = self.ktk.getUser()
        self.ktk.needUser(current_user)
        expect_word_need = "Need: {0}".format(current_user)
        expect_word_current = "Current: {0}".format(current_user)
        test_output = self.fakeout.readline()
        self.assertTrue(expect_word_need in test_output)
        self.assertTrue(expect_word_current in test_output)

    def test_TRACE(self):
        f = self.ktk_inst.trace_file
        old_trace_exist = os.path.exists(f)
        self.ktk_inst.TRACE("Test Text")
        self.assertTrue(os.path.exists(f))
        if not old_trace_exist:
            os.remove(f)

    def test_inTrace(self):
        @self.ktk_inst.inTrace
        def inTrace():
            print("Test Text")

        fl = self.ktk_inst.trace_file
        old_trace_exist = os.path.exists(fl)
        inTrace()
        self.assertEqual(self.fakeout.readline(), "Test Text\n")
        self.assertTrue(os.path.exists(fl))
        if not old_trace_exist:
            os.remove(fl)


if __name__ == '__main__':
    unittest.main(verbosity=2, exit=False)  # print more info, no sys.exit() called.
