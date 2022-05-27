import io
import sys
import unittest

from mock import patch
from PyQt5.QtWidgets import QApplication, QWidget

from dls_powerpmacanalyse.ppmacanalyse_control import Controlform

app = QApplication(sys.argv)
test_widget = QWidget()


class ControlTest(unittest.TestCase):
    def setUp(self):
        self.obj = Controlform(test_widget)

    def test_inital_form(self):
        self.assertEqual(self.obj.lineServer0.text(), "192.168.56.10")
        self.assertEqual(self.obj.linePort0.text(), "22")

    @patch("dls_powerpmacanalyse.ppmacanalyse_control.subprocess.Popen")
    def testBackupSuccess(self, mock_ppmac_cmd):
        output = ""
        mock_ppmac_cmd.return_value.stderr = io.BytesIO(output.encode())
        self.obj.runBackup()
        assert mock_ppmac_cmd.called
        assert "completed" in self.obj.textOutput.toPlainText()

    @patch("dls_powerpmacanalyse.ppmacanalyse_control.Controlform.wasCancelled")
    @patch("dls_powerpmacanalyse.ppmacanalyse_control.subprocess.Popen")
    def testBackupCancel(self, mock_ppmac_cmd, mock_was_cancelled):
        self.obj.cancelBackup = True
        output = ""
        mock_was_cancelled.return_value = True
        mock_ppmac_cmd.return_value.stderr = io.BytesIO(output.encode())
        self.obj.runBackup()
        assert mock_ppmac_cmd.called
        assert "cancelled" in self.obj.textOutput.toPlainText()

    @patch("dls_powerpmacanalyse.ppmacanalyse_control.subprocess.Popen")
    def testBackupFail(self, mock_ppmac_cmd):
        output = "PowerPmac error"
        mock_ppmac_cmd.return_value.stderr = io.BytesIO(output.encode())
        self.obj.runBackup()
        assert mock_ppmac_cmd.called
        assert output in self.obj.textOutput.toPlainText()

    @patch("dls_powerpmacanalyse.ppmacanalyse_control.subprocess.Popen")
    def testCompare(self, mock_ppmac_cmd):
        output = ""
        mock_ppmac_cmd.return_value.stderr = io.BytesIO(output.encode())
        self.obj.runCompare()
        assert mock_ppmac_cmd.called
        assert "completed" in self.obj.textOutput.toPlainText()

    @patch("dls_powerpmacanalyse.ppmacanalyse_control.subprocess.Popen")
    def testRecover(self, mock_ppmac_cmd):
        output = ""
        mock_ppmac_cmd.return_value.stderr = io.BytesIO(output.encode())
        self.obj.runRecover()
        assert mock_ppmac_cmd.called
        assert "completed" in self.obj.textOutput.toPlainText()

    @patch("dls_powerpmacanalyse.ppmacanalyse_control.subprocess.Popen")
    def testDownload(self, mock_ppmac_cmd):
        output = ""
        mock_ppmac_cmd.return_value.stderr = io.BytesIO(output.encode())
        self.obj.runDownload()
        assert mock_ppmac_cmd.called
        assert "completed" in self.obj.textOutput.toPlainText()

    def tearDown(self):
        self.obj.close()
