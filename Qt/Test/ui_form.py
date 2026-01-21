# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QPushButton, QSizePolicy,
    QWidget)

class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(800, 600)
        self.bouton_test = QPushButton(Widget)
        self.bouton_test.setObjectName(u"bouton_test")
        self.bouton_test.setGeometry(QRect(360, 360, 80, 24))
        self.label_test = QLabel(Widget)
        self.label_test.setObjectName(u"label_test")
        self.label_test.setGeometry(QRect(350, 310, 101, 16))
        self.label_test.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.retranslateUi(Widget)

        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"Widget", None))
        self.bouton_test.setText(QCoreApplication.translate("Widget", u"Test_Bouton", None))
        self.label_test.setText(QCoreApplication.translate("Widget", u"Test", None))
    # retranslateUi

