from PyQt5 import QtCore, QtWidgets
import sys, ctypes
import pyAesCrypt
from PyQt5.QtWidgets import QMenu, QSystemTrayIcon, qApp
from PyQt5.QtGui import QIcon
from ctypes.wintypes import HKEY, MAX_PATH

def add_to_startup():
    HKEY_CURRENT_USER = -2147483647
    KEY_ALL_ACCESS = 0xf003f
    REG_SZ = 1

    NPPNAME = ctypes.create_unicode_buffer(MAX_PATH)
    ctypes.windll.kernel32.GetModuleFileNameW(0, ctypes.byref(NPPNAME), ctypes.sizeof(NPPNAME))

    phkResult = HKEY()
    ctypes.windll.advapi32.RegOpenKeyExW(HKEY_CURRENT_USER, u'SOFTWARE\Microsoft\Windows\CurrentVersion\Run', 0, KEY_ALL_ACCESS, ctypes.byref(phkResult))
    ctypes.windll.advapi32.RegSetValueExW(phkResult, 'AESCrYpt0r256', 0, REG_SZ, sys.argv[0], len(NPPNAME))
    ctypes.windll.advapi32.RegCloseKey(phkResult)

class Ui_MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Drag and Drop")
        self.setWindowIcon(QIcon('chain.ico'))
        self.setFixedSize(485, 550)
        self.setAcceptDrops(True)
    
    def execute(self):
        try:
            if self.state == 'Encrypt':
                try:
                    self.encrypt(self.file, self.password, self.output)
                    ctypes.windll.user32.MessageBoxW(0, f'File: {self.file} is encrypted', 'Success', 0x00000000 | 0x00000040)
                except:
                    ctypes.windll.user32.MessageBoxW(0, f'Impossible to encrypt file {self.file}', 'Warning', 0x00000000 | 0x00000030)
            if self.state == 'Decrypt':
                try:
                    self.decrypt(self.file, self.password, self.output)
                    ctypes.windll.user32.MessageBoxW(0, f'File: {self.file} is decrypted', 'Success', 0x00000000 | 0x00000040)
                except:
                    ctypes.windll.user32.MessageBoxW(0, f'Impossible to decrypt file {self.file}', 'Warning', 0x00000000 | 0x00000030)
        except:
            ctypes.windll.user32.MessageBoxW(0, 'Fill out all the lines!', 'Warning!', 0x00000000 | 0x00000040)
    
    def encrypt(self, filename, password, output):
        pyAesCrypt.encryptFile(filename, output, password, bufferSize=128 * 1024)
    
    def decrypt(self, filename, password, output):
        pyAesCrypt.decryptFile(filename, output, password, bufferSize=128 * 1024)
    
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()
    
    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        for file in files:
            self.lineEdit.setText(file)

    def pr(self):
        if self.radioButton.isChecked():
            self.state = 'Encrypt'
        if self.radioButton_2.isChecked():
            self.state = 'Decrypt'
        self.file = self.lineEdit.text()
        self.password = self.lineEdit_2.text()
        self.output = self.lineEdit_3.text()

    def setupUi(self, MainWindow):
        MainWindow.setWindowFlags(QtCore.Qt.Window)
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(490, 555)
        MainWindow.setStyleSheet("background-color: rgb(116, 116, 116);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(10, 100, 261, 31))
        self.textBrowser.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"background-color: rgb(39, 255, 208);")
        self.textBrowser.setObjectName("textBrowser")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(280, 100, 201, 31))
        self.lineEdit.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(20, 500, 75, 23))
        self.pushButton.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(lambda: self.execute())
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(10, 140, 151, 31))
        self.textEdit.setStyleSheet("background-color: rgb(39, 255, 208);")
        self.textEdit.setObjectName("textEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(280, 140, 201, 31))
        self.lineEdit_2.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.textBrowser_2 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_2.setGeometry(QtCore.QRect(10, 180, 181, 31))
        self.textBrowser_2.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"background-color: rgb(39, 255, 208);")
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_3.setGeometry(QtCore.QRect(280, 180, 201, 31))
        self.lineEdit_3.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton.setGeometry(QtCore.QRect(400, 230, 82, 17))
        self.radioButton.setObjectName("radioButton")
        self.radioButton.toggled.connect(lambda: self.pr())
        self.radioButton_2 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_2.setGeometry(QtCore.QRect(400, 260, 82, 17))
        self.radioButton_2.setObjectName("radioButton_2")
        self.radioButton_2.toggled.connect(lambda: self.pr())
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 491, 51))
        self.label.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"background-color: rgb(21, 255, 68);")
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("AESCrYpt0r256", "AESCrYpt0r256"))
        self.textBrowser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">Enter the path to file or drop it here</span></p></body></html>"))
        self.pushButton.setText(_translate("MainWindow", "PushButton"))
        self.textEdit.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">Enter the password</span></p></body></html>"))
        self.textBrowser_2.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">Enter the path for output</span></p></body></html>"))
        self.radioButton.setText(_translate("MainWindow", "Encrypt"))
        self.radioButton_2.setText(_translate("MainWindow", "Decrypt"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; font-weight:600; text-decoration: underline;\">STRONG ENCRYPTION ALGORITHM AES-256-CBC</span></p></body></html>"))

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = Ui_MainWindow()

    menu = QMenu()
    checkAction = menu.addAction("Show")
    checkAction.triggered.connect(lambda: ex.show())
    checkAction_1 = menu.addAction("Hide")
    checkAction_1.triggered.connect(lambda: ex.hide())
    checkAction_2 = menu.addAction("On Top")
    checkAction_2.triggered.connect(lambda: ex.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.WindowStaysOnTopHint))
    checkAction_3 = menu.addAction("StartUp")
    checkAction_3.triggered.connect(lambda: add_to_startup())
    quitAction = menu.addAction("Quit")
    quitAction.triggered.connect(qApp.quit)

    # Creating icon
    icon = QIcon.fromTheme("system-help", QIcon('chain.ico'))

    # Creating tray
    trayIcon = QSystemTrayIcon(icon, app)
    trayIcon.setContextMenu(menu)

    # Showing tray
    trayIcon.show()
    trayIcon.setToolTip("AESCrYpt0r256")
    trayIcon.showMessage("AESCrYpt0r256", "Control mini-application AESCrYpt0r256 from system tray")

    ex.setupUi(ex)
    ex.show()
    sys.exit(app.exec_())
