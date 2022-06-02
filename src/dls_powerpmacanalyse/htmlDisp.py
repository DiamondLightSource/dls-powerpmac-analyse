import os

from PyQt5 import QtCore, QtWebEngineWidgets, QtWidgets

no_diff_html = (
    " <!DOCTYPE html><html><body><p>No differences to display between"
    " Source A and Source B.</p></body></html> "
)
no_file_html = (
    " <!DOCTYPE html><html><body><p>Please select a diff to display from"
    " the list.</p></body></html> "
)


class Ui_ViewerDialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Comparison Viewer")
        Dialog.resize(1800, 800)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(1450, 762, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.listWidget = QtWidgets.QListWidget(Dialog)
        self.listWidget.setGeometry(QtCore.QRect(10, 10, 270, 500))
        self.listWidget.setObjectName("listWidget")
        for i in range(0, self.numFiles):
            item = QtWidgets.QListWidgetItem()
            self.listWidget.addItem(item)
        self.webEngineView = QtWebEngineWidgets.QWebEngineView(Dialog)
        self.webEngineView.setHtml(no_file_html)
        self.webEngineView.setGeometry(QtCore.QRect(290, 10, 1500, 740))
        self.webEngineView.setObjectName("widget")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        self.listWidget.itemPressed["QListWidgetItem*"].connect(self.openFile)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        if self.path is None:
            self.path = "/does/not/exist"

    def setFileList(self, filelist):
        self.filelist = filelist
        self.numFiles = len(filelist)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Comparison Viewer", "Comparison Viewer"))
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)

        for i in range(0, self.numFiles):
            item = self.listWidget.item(i)
            # listsplt = self.filelist[i].split("/")
            name = self.filelist[i].replace(self.path, "")
            rmExtName = name.replace(".html", "")
            item.setText(_translate("Dialog", rmExtName))
        self.listWidget.setSortingEnabled(__sortingEnabled)

    def openFile(self):
        for i in range(0, self.numFiles):
            if self.listWidget.currentRow() == i:
                self.updateWebView(self.filelist[i])
                break

    def updateWebView(self, newpath):
        if os.path.exists(newpath):
            self.webEngineView.load(QtCore.QUrl().fromLocalFile(newpath))
        else:
            self.webEngineView.setHtml(no_diff_html)

    def setPath(self, newpath):
        self.path = newpath


class ComparisonViewer(Ui_ViewerDialog):
    def __init__(self, parent):
        self.dialog = QtWidgets.QDialog()

    def setup(self, rootPath, fileList):
        self.ui = Ui_ViewerDialog()
        self.ui.setPath(rootPath)
        self.ui.setFileList(fileList)
        self.ui.setupUi(self.dialog)

    def show(self):
        self.dialog.show()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_ViewerDialog()
    ui.setPath("rootPath")
    ui.setFileList([])
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
