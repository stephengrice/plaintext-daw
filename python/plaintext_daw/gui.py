# -*- coding: utf-8 -*-
# @Time    : 2023/1/28 23:07
# @Author  : LTstrange

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg


class MainWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("plaintext-DAW")
        self.resize(640, 480)

        btn = qtw.QPushButton(self)
        fnt = qtg.QFont()
        fnt.setPointSize(20)
        btn.setFont(fnt)
        btn.setText("Open Project")
        btn.adjustSize()
        btn.clicked.connect(self.open_project)

        layout = qtw.QVBoxLayout()
        layout.addWidget(btn)

        self.setLayout(layout)

    def open_project(self):
        qtw.QMessageBox().information(self, "plaintext-DAW", "Hello World")


def gui():
    app = qtw.QApplication([])
    mw = MainWindow()
    mw.show()
    return app.exec_()
