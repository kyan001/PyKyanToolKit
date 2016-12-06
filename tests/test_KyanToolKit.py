# -*- coding: utf-8 -*-
##################################################################
# For KTK
##################################################################
import sys
import os
import unittest

import FakeOut
import FakeIn
import FakeOs

sys.path.insert(0, '../')
import KyanToolKit


class test_KyanToolKit(unittest.TestCase):
    '''
    KyanToolKit.py Unit Tests
    '''
    ktk_version = '5.0.1'

    def setUp(self):
        self.ktk = KyanToolKit.KyanToolKit()
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
        self.assertEqual(self.ktk_version, self.ktk.version)

    def test_init(self):
        'testing __init__()'
        self.assertTrue(self.ktk.trace_file)

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
        test_url = "http://www.superfarmer.net/static/img/index/div_card_products.png"
        color = self.ktk.imageToColor(test_url)
        self.assertEqual(color, (5, 147, 208))

    def test_imageToColor_hex(self):
        test_url = "http://www.superfarmer.net/static/img/index/div_card_products.png"
        color = self.ktk.imageToColor(test_url, mode='hex')
        self.assertEqual(color, '#0593D0')

    def test_clearScreen(self):
        self.ktk.clearScreen()
        self.assertTrue(self.fakeos.readline() in 'cls clear')

    def test_checkResult_1(self):
        self.ktk.checkResult(0)
        self.assertTrue("Done" in self.fakeout.readline())

    def test_checkResult_2(self):
        self.ktk.checkResult(1)
        self.assertTrue("Failed" in self.fakeout.readline())

    def test_runCmd(self):
        self.ktk.runCmd("echo Test Text")
        self.assertEqual(self.fakeos.readline(), "echo Test Text")

    def test_readCmd(self):
        self.assertEqual(self.ktk.readCmd(r"echo Test Text"), "Test Text\n")

    def test_getUser(self):
        self.assertEqual(self.ktk.getUser(), os.getlogin())

    def test_ajax_get(self):
        url = 'https://api.douban.com/v2/movie/search'
        param = {'q': '胜者即是正义', 'count': 1}
        result = self.ktk.ajax(url, param, 'get')
        cast = result.get('subjects')[0].get('casts')[1].get('name')
        self.assertEqual(cast, '新垣结衣')

    def test_needPlatform(self):
        self.ktk.needPlatform(sys.platform)
        expect_word_need = "Need: {0}\n".format(sys.platform)
        expect_word_current = "Current: {0}\n".format(sys.platform)
        test_output = self.fakeout.readline()
        self.assertTrue(expect_word_need in test_output)
        self.assertTrue(expect_word_current in test_output)

    def test_needUser(self):
        current_user = self.ktk.getUser()
        self.ktk.needUser(current_user)
        expect_word_need = "Need: {0}\n".format(current_user)
        expect_word_current = "Current: {0}\n".format(current_user)
        test_output = self.fakeout.readline()
        self.assertTrue(expect_word_need in test_output)
        self.assertTrue(expect_word_current in test_output)

    def test_TRACE(self):
        f = self.ktk.trace_file
        old_trace_exist = os.path.exists(f)
        self.ktk.TRACE("Test Text")
        self.assertTrue(os.path.exists(f))
        if not old_trace_exist:
            os.remove(f)

    def test_inTrace(self):
        @self.ktk.inTrace
        def inTrace():
            print("Test Text")
        f = self.ktk.trace_file
        old_trace_exist = os.path.exists(f)
        inTrace()
        self.assertEqual(self.fakeout.readline(), "Test Text\n")
        self.assertTrue(os.path.exists(f))
        if not old_trace_exist:
            os.remove(f)

if __name__ == '__main__':
    KyanToolKit.KyanToolKit().clearScreen()
    unittest.main(verbosity=2, exit=False)  # print more info, no sys.exit() called.
