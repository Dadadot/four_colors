# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QMainWindow, QMenu,
    QMenuBar, QSizePolicy, QStatusBar, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 601)
        self.actionLoad = QAction(MainWindow)
        self.actionLoad.setObjectName(u"actionLoad")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_3 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalWidget_2 = QWidget(self.centralwidget)
        self.horizontalWidget_2.setObjectName(u"horizontalWidget_2")
        self.horizontalLayout = QHBoxLayout(self.horizontalWidget_2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.c_image_main = QWidget(self.horizontalWidget_2)
        self.c_image_main.setObjectName(u"c_image_main")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.c_image_main.sizePolicy().hasHeightForWidth())
        self.c_image_main.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(self.c_image_main)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        self.horizontalLayout.addWidget(self.c_image_main)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.c_image_selection = QWidget(self.horizontalWidget_2)
        self.c_image_selection.setObjectName(u"c_image_selection")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.c_image_selection.sizePolicy().hasHeightForWidth())
        self.c_image_selection.setSizePolicy(sizePolicy1)
        self.c_image_selection.setMaximumSize(QSize(16777215, 16777215))
        self.verticalLayout_4 = QVBoxLayout(self.c_image_selection)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout_2.addWidget(self.c_image_selection)

        self.c_colors = QWidget(self.horizontalWidget_2)
        self.c_colors.setObjectName(u"c_colors")
        sizePolicy1.setHeightForWidth(self.c_colors.sizePolicy().hasHeightForWidth())
        self.c_colors.setSizePolicy(sizePolicy1)
        self.c_colors.setAutoFillBackground(False)
        self.horizontalLayout_2 = QHBoxLayout(self.c_colors)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout_2.addWidget(self.c_colors)


        self.horizontalLayout.addLayout(self.verticalLayout_2)


        self.verticalLayout_3.addWidget(self.horizontalWidget_2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 23))
        self.menuLoad_Image = QMenu(self.menubar)
        self.menuLoad_Image.setObjectName(u"menuLoad_Image")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuLoad_Image.menuAction())
        self.menuLoad_Image.addAction(self.actionLoad)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionLoad.setText(QCoreApplication.translate("MainWindow", u"Load", None))
        self.menuLoad_Image.setTitle(QCoreApplication.translate("MainWindow", u"Image", None))
    # retranslateUi

