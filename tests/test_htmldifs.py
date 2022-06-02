import sys
import unittest

from dls_powerpmacanalyse.htmlDisp import ComparisonViewer
from PyQt5.QtWidgets import QApplication, QDialog

app = QApplication(sys.argv)
test_widget = QDialog()


class htmlDisplayTest(unittest.TestCase):
    def setUp(self):
        self.obj = ComparisonViewer(test_widget)
        self.obj.setup("rootPath", ["test1"])

    def test_inital_form(self):
        self.assertEqual(self.obj.ui.path, "rootPath")
        self.assertEqual(self.obj.ui.filelist, ["test1"])
        self.assertEqual(self.obj.ui.numFiles, 1)

    def test_open_file(self):
        self.obj.ui.openFile()
