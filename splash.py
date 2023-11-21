# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'splash.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setWindowModality(QtCore.Qt.WindowModal)
        Form.setEnabled(True)
        Form.resize(500, 380)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setStyleSheet("background-color: rgb(39, 137, 243);\n"
"border-radius: 15px;")
        self.vboxlayout = QtWidgets.QVBoxLayout(Form)
        self.vboxlayout.setContentsMargins(0, 0, 0, 0)
        self.vboxlayout.setSpacing(0)
        self.vboxlayout.setObjectName("vboxlayout")
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setMinimumSize(QtCore.QSize(482, 155))
        self.frame.setMaximumSize(QtCore.QSize(482, 155))
        self.frame.setStyleSheet("border-image:  0 0 0 0 stretch stretch;\n"
"border-image: url(:/iconeFooter/Images/iconeFooter.png);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.vboxlayout.addWidget(self.frame)
        self.label = QtWidgets.QLabel(Form)
        self.label.setMaximumSize(QtCore.QSize(16777215, 80))
        self.label.setStyleSheet("color: rgb(255, 255, 255);\n"
"font-size: 20px;\n"
"font-weight: bold;")
        self.label.setMidLineWidth(2)
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setIndent(0)
        self.label.setObjectName("label")
        self.vboxlayout.addWidget(self.label)
        self.progressBar = QtWidgets.QProgressBar(Form)
        self.progressBar.setMaximumSize(QtCore.QSize(490, 16777215))
        self.progressBar.setStyleSheet("QProgressBar{\n"
"    border-radius:10px;\n"
"    background-color: rgb(198, 216, 255);\n"
"}\n"
"\n"
"QProgressBar::chunk{\n"
"   border-radius:10px;\n"
"    background-color: rgb(2, 2, 255);\n"
"}")
        self.progressBar.setProperty("value", 24)
        self.progressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.progressBar.setTextVisible(False)
        self.progressBar.setObjectName("progressBar")
        self.vboxlayout.addWidget(self.progressBar)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setMinimumSize(QtCore.QSize(0, 20))
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label_2.setStyleSheet("color: rgb(255, 255, 255);\n"
"font-size: 10px;\n"
"font-weight: bold;")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.vboxlayout.addWidget(self.label_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Bem vindo ao software de Envio Automático.\n"
"Carregando o aplicativo! Aguarde..."))
        self.label_2.setText(_translate("Form", "versão 0.9.2\n"
"Desenvolvido por Eliabel Barreto"))
import file_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())