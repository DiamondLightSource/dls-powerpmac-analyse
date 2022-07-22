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

    @patch("dls_powerpmacanalyse.login.Loginform.exec")
    @patch("dls_powerpmacanalyse.ppmacanalyse_control.subprocess.Popen")
    def testInvalidUser(self, mock_ppmac_cmd, mock_login):
        output = "Invalid username given"
        mock_ppmac_cmd.return_value.stderr = io.BytesIO(output.encode())
        mock_login.return_value = True
        self.obj.runPPmacAnalyseCmd(["test", "cmd", "string"], 0, "Backup")
        assert "Invalid username" in self.obj.textOutput.toPlainText()

    @patch("PyQt5.QtWidgets.QFileDialog.getOpenFileName")
    def testIgnoreFileBrowser(self, mock_dialog):
        mock_dialog.return_value = "test/dir", "_filter"
        self.obj.ignoreFileBrowser()
        assert self.obj.lineIgnoreFile0.text() == "test/dir"
        self.obj.mode = 1
        self.obj.ignoreFileBrowser()
        assert self.obj.lineIgnoreFile1.text() == "test/dir"

    @patch("PyQt5.QtWidgets.QFileDialog.getExistingDirectory")
    def testOutputDirBrowser(self, mock_dialog):
        dir = "test/outputdir"
        mock_dialog.return_value = dir
        self.obj.outputDirBrowser()
        assert self.obj.lineOutputDir0.text() == dir
        self.obj.mode = 1
        self.obj.outputDirBrowser()
        assert self.obj.lineOutputDir1.text() == dir
        self.obj.mode = 2
        self.obj.outputDirBrowser()
        assert self.obj.lineOutputDir2.text() == dir

    @patch("dls_powerpmacanalyse.htmlDisp.ComparisonViewer.show")
    def testOpenViewer(self, mock_show):
        self.obj.openViewer()
        assert self.obj.lineOutputDir1.text() == "./ppmacAnalyse"
        assert self.obj.compviewer.ui.numFiles == 0

    def tearDown(self):
        self.obj.close()
