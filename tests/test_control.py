import sys
import unittest

from PyQt5.QtWidgets import QApplication, QWidget

from dls_powerpmacanalyse.ppmacanalyse_control import Controlform

app = QApplication(sys.argv)
test_widget = QWidget()


class ControlTest(unittest.TestCase):
    def setUp(self):
        self.obj = Controlform(test_widget)

    def test_inital_form(self):
        self.assertEqual(self.obj.lineServer0.text(), "192.168.56.10")

    def tearDown(self):
        self.obj.close()
