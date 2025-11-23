# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindows.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QCheckBox, QComboBox,
    QFormLayout, QGridLayout, QHeaderView, QLabel,
    QLineEdit, QMainWindow, QMenu, QMenuBar,
    QProgressBar, QPushButton, QScrollArea, QSizePolicy,
    QStatusBar, QTableView, QWidget)

class Ui_MainWindows(object):
    def setupUi(self, MainWindows):
        if not MainWindows.objectName():
            MainWindows.setObjectName(u"MainWindows")
        MainWindows.resize(1250, 785)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(MainWindows.sizePolicy().hasHeightForWidth())
        MainWindows.setSizePolicy(sizePolicy)
        palette = QPalette()
        brush = QBrush(QColor(255, 255, 255, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Button, brush)
        palette.setBrush(QPalette.Active, QPalette.Base, brush)
        palette.setBrush(QPalette.Active, QPalette.Window, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Button, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Base, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Window, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Button, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Base, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Window, brush)
        MainWindows.setPalette(palette)
        MainWindows.setAutoFillBackground(False)
        MainWindows.setStyleSheet(u"background-color:white\n"
" \n"
" ")
        MainWindows.setAnimated(False)
        MainWindows.setDockNestingEnabled(False)
        self.actionHISTORY = QAction(MainWindows)
        self.actionHISTORY.setObjectName(u"actionHISTORY")
        self.actionSetting = QAction(MainWindows)
        self.actionSetting.setObjectName(u"actionSetting")
        self.actionData_outport = QAction(MainWindows)
        self.actionData_outport.setObjectName(u"actionData_outport")
        self.centralwidget = QWidget(MainWindows)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(1)
        sizePolicy1.setVerticalStretch(1)
        sizePolicy1.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy1)
        self.centralwidget.setBaseSize(QSize(0, 0))
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(1)
        sizePolicy2.setVerticalStretch(1)
        sizePolicy2.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy2)
        font = QFont()
        font.setFamilies([u"\u65b0\u5b8b\u4f53"])
        font.setPointSize(16)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet(u"background-color:white")
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_2, 2, 3, 1, 1)

        self.label_8 = QLabel(self.centralwidget)
        self.label_8.setObjectName(u"label_8")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(1)
        sizePolicy3.setVerticalStretch(1)
        sizePolicy3.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy3)
        font1 = QFont()
        font1.setFamilies([u"Adobe \u5b8b\u4f53 Std L"])
        font1.setPointSize(10)
        self.label_8.setFont(font1)
        self.label_8.setStyleSheet(u"background-color:white")
        self.label_8.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_8, 10, 2, 1, 1)

        self.label_11 = QLabel(self.centralwidget)
        self.label_11.setObjectName(u"label_11")
        sizePolicy2.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy2)
        font2 = QFont()
        font2.setFamilies([u"Arial Black"])
        font2.setPointSize(16)
        font2.setBold(True)
        self.label_11.setFont(font2)
        self.label_11.setStyleSheet(u"background-color:white")
        self.label_11.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_11, 0, 3, 1, 3)

        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setObjectName(u"scrollArea")
        sizePolicy1.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy1)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setEnabled(True)
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 379, 600))
        self.scrollAreaWidgetContents_2.setBaseSize(QSize(0, 0))
        self.formLayout = QFormLayout(self.scrollAreaWidgetContents_2)
        self.formLayout.setObjectName(u"formLayout")
        self.image_label_1 = QLabel(self.scrollAreaWidgetContents_2)
        self.image_label_1.setObjectName(u"image_label_1")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.image_label_1.sizePolicy().hasHeightForWidth())
        self.image_label_1.setSizePolicy(sizePolicy4)
        self.image_label_1.setPixmap(QPixmap(u"C:/Users/Administrator/Desktop/\u6837\u672c\u6210\u679c1.png"))
        self.image_label_1.setScaledContents(True)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.image_label_1)

        self.image_label_7 = QLabel(self.scrollAreaWidgetContents_2)
        self.image_label_7.setObjectName(u"image_label_7")
        self.image_label_7.setBaseSize(QSize(2, 0))
        self.image_label_7.setPixmap(QPixmap(u"C:/Users/Administrator/Desktop/\u6837\u672c\u6210\u679c1.png"))
        self.image_label_7.setScaledContents(True)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.image_label_7)

        self.name_label_1 = QLabel(self.scrollAreaWidgetContents_2)
        self.name_label_1.setObjectName(u"name_label_1")
        self.name_label_1.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.name_label_1)

        self.name_label_7 = QLabel(self.scrollAreaWidgetContents_2)
        self.name_label_7.setObjectName(u"name_label_7")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.name_label_7)

        self.image_label_2 = QLabel(self.scrollAreaWidgetContents_2)
        self.image_label_2.setObjectName(u"image_label_2")
        self.image_label_2.setPixmap(QPixmap(u"C:/Users/Administrator/Desktop/\u6837\u672c\u6210\u679c1.png"))
        self.image_label_2.setScaledContents(True)

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.image_label_2)

        self.image_label_8 = QLabel(self.scrollAreaWidgetContents_2)
        self.image_label_8.setObjectName(u"image_label_8")
        self.image_label_8.setPixmap(QPixmap(u"C:/Users/Administrator/Desktop/\u6837\u672c\u6210\u679c1.png"))
        self.image_label_8.setScaledContents(True)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.image_label_8)

        self.name_label_2 = QLabel(self.scrollAreaWidgetContents_2)
        self.name_label_2.setObjectName(u"name_label_2")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.name_label_2)

        self.name_label_8 = QLabel(self.scrollAreaWidgetContents_2)
        self.name_label_8.setObjectName(u"name_label_8")

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.name_label_8)

        self.image_label_3 = QLabel(self.scrollAreaWidgetContents_2)
        self.image_label_3.setObjectName(u"image_label_3")
        self.image_label_3.setPixmap(QPixmap(u"C:/Users/Administrator/Desktop/\u6837\u672c\u6210\u679c1.png"))
        self.image_label_3.setScaledContents(True)

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.image_label_3)

        self.image_label_9 = QLabel(self.scrollAreaWidgetContents_2)
        self.image_label_9.setObjectName(u"image_label_9")
        self.image_label_9.setPixmap(QPixmap(u"C:/Users/Administrator/Desktop/\u6837\u672c\u6210\u679c1.png"))
        self.image_label_9.setScaledContents(True)

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.image_label_9)

        self.name_label_3 = QLabel(self.scrollAreaWidgetContents_2)
        self.name_label_3.setObjectName(u"name_label_3")

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.name_label_3)

        self.name_label_9 = QLabel(self.scrollAreaWidgetContents_2)
        self.name_label_9.setObjectName(u"name_label_9")

        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.name_label_9)

        self.image_label_4 = QLabel(self.scrollAreaWidgetContents_2)
        self.image_label_4.setObjectName(u"image_label_4")
        self.image_label_4.setPixmap(QPixmap(u"C:/Users/Administrator/Desktop/\u6837\u672c\u6210\u679c1.png"))
        self.image_label_4.setScaledContents(True)

        self.formLayout.setWidget(6, QFormLayout.LabelRole, self.image_label_4)

        self.image_label_10 = QLabel(self.scrollAreaWidgetContents_2)
        self.image_label_10.setObjectName(u"image_label_10")
        self.image_label_10.setPixmap(QPixmap(u"C:/Users/Administrator/Desktop/\u6837\u672c\u6210\u679c1.png"))
        self.image_label_10.setScaledContents(True)

        self.formLayout.setWidget(6, QFormLayout.FieldRole, self.image_label_10)

        self.name_label_4 = QLabel(self.scrollAreaWidgetContents_2)
        self.name_label_4.setObjectName(u"name_label_4")

        self.formLayout.setWidget(7, QFormLayout.LabelRole, self.name_label_4)

        self.name_label_10 = QLabel(self.scrollAreaWidgetContents_2)
        self.name_label_10.setObjectName(u"name_label_10")

        self.formLayout.setWidget(7, QFormLayout.FieldRole, self.name_label_10)

        self.image_label_5 = QLabel(self.scrollAreaWidgetContents_2)
        self.image_label_5.setObjectName(u"image_label_5")
        self.image_label_5.setPixmap(QPixmap(u"C:/Users/Administrator/Desktop/\u6837\u672c\u6210\u679c1.png"))
        self.image_label_5.setScaledContents(True)

        self.formLayout.setWidget(8, QFormLayout.LabelRole, self.image_label_5)

        self.image_label_11 = QLabel(self.scrollAreaWidgetContents_2)
        self.image_label_11.setObjectName(u"image_label_11")
        self.image_label_11.setPixmap(QPixmap(u"C:/Users/Administrator/Desktop/\u6837\u672c\u6210\u679c1.png"))
        self.image_label_11.setScaledContents(True)

        self.formLayout.setWidget(8, QFormLayout.FieldRole, self.image_label_11)

        self.name_label_5 = QLabel(self.scrollAreaWidgetContents_2)
        self.name_label_5.setObjectName(u"name_label_5")

        self.formLayout.setWidget(9, QFormLayout.LabelRole, self.name_label_5)

        self.name_label_11 = QLabel(self.scrollAreaWidgetContents_2)
        self.name_label_11.setObjectName(u"name_label_11")

        self.formLayout.setWidget(9, QFormLayout.FieldRole, self.name_label_11)

        self.image_label_6 = QLabel(self.scrollAreaWidgetContents_2)
        self.image_label_6.setObjectName(u"image_label_6")
        sizePolicy1.setHeightForWidth(self.image_label_6.sizePolicy().hasHeightForWidth())
        self.image_label_6.setSizePolicy(sizePolicy1)
        self.image_label_6.setPixmap(QPixmap(u"C:/Users/Administrator/Desktop/\u6837\u672c\u6210\u679c1.png"))
        self.image_label_6.setScaledContents(True)

        self.formLayout.setWidget(10, QFormLayout.LabelRole, self.image_label_6)

        self.name_label_6 = QLabel(self.scrollAreaWidgetContents_2)
        self.name_label_6.setObjectName(u"name_label_6")

        self.formLayout.setWidget(11, QFormLayout.LabelRole, self.name_label_6)

        self.name_label_12 = QLabel(self.scrollAreaWidgetContents_2)
        self.name_label_12.setObjectName(u"name_label_12")

        self.formLayout.setWidget(11, QFormLayout.FieldRole, self.name_label_12)

        self.image_label_12 = QLabel(self.scrollAreaWidgetContents_2)
        self.image_label_12.setObjectName(u"image_label_12")
        sizePolicy1.setHeightForWidth(self.image_label_12.sizePolicy().hasHeightForWidth())
        self.image_label_12.setSizePolicy(sizePolicy1)
        self.image_label_12.setPixmap(QPixmap(u"C:/Users/Administrator/Desktop/\u6837\u672c\u6210\u679c1.png"))
        self.image_label_12.setScaledContents(True)

        self.formLayout.setWidget(10, QFormLayout.FieldRole, self.image_label_12)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)

        self.gridLayout.addWidget(self.scrollArea, 4, 6, 6, 2)

        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy5)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet(u"background-color:white")
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_3, 5, 3, 1, 1)

        self.checkBox_2 = QCheckBox(self.centralwidget)
        self.checkBox_2.setObjectName(u"checkBox_2")

        self.gridLayout.addWidget(self.checkBox_2, 9, 1, 1, 1)

        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName(u"lineEdit")
        sizePolicy2.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.lineEdit, 6, 1, 1, 5)

        self.pushButton_3 = QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.gridLayout.addWidget(self.pushButton_3, 10, 0, 1, 1)

        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")

        self.gridLayout.addWidget(self.pushButton, 9, 0, 1, 1)

        self.checkBox_3 = QCheckBox(self.centralwidget)
        self.checkBox_3.setObjectName(u"checkBox_3")

        self.gridLayout.addWidget(self.checkBox_3, 10, 1, 1, 1)

        self.lineEdit_2 = QLineEdit(self.centralwidget)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy6.setHorizontalStretch(1)
        sizePolicy6.setVerticalStretch(1)
        sizePolicy6.setHeightForWidth(self.lineEdit_2.sizePolicy().hasHeightForWidth())
        self.lineEdit_2.setSizePolicy(sizePolicy6)

        self.gridLayout.addWidget(self.lineEdit_2, 9, 5, 1, 1)

        self.label_10 = QLabel(self.centralwidget)
        self.label_10.setObjectName(u"label_10")
        sizePolicy3.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy3)
        self.label_10.setFont(font1)
        self.label_10.setStyleSheet(u"background-color:white")
        self.label_10.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_10, 9, 4, 1, 1)

        self.lineEdit_4 = QLineEdit(self.centralwidget)
        self.lineEdit_4.setObjectName(u"lineEdit_4")
        sizePolicy6.setHeightForWidth(self.lineEdit_4.sizePolicy().hasHeightForWidth())
        self.lineEdit_4.setSizePolicy(sizePolicy6)

        self.gridLayout.addWidget(self.lineEdit_4, 10, 3, 1, 1)

        self.pushButton_5 = QPushButton(self.centralwidget)
        self.pushButton_5.setObjectName(u"pushButton_5")
        sizePolicy7 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        sizePolicy7.setHorizontalStretch(1)
        sizePolicy7.setVerticalStretch(1)
        sizePolicy7.setHeightForWidth(self.pushButton_5.sizePolicy().hasHeightForWidth())
        self.pushButton_5.setSizePolicy(sizePolicy7)

        self.gridLayout.addWidget(self.pushButton_5, 10, 6, 1, 2)

        self.label_21 = QLabel(self.centralwidget)
        self.label_21.setObjectName(u"label_21")
        sizePolicy2.setHeightForWidth(self.label_21.sizePolicy().hasHeightForWidth())
        self.label_21.setSizePolicy(sizePolicy2)
        self.label_21.setFont(font)
        self.label_21.setStyleSheet(u"background-color:white")
        self.label_21.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_21, 3, 6, 1, 2)

        self.pushButton_4 = QPushButton(self.centralwidget)
        self.pushButton_4.setObjectName(u"pushButton_4")
        sizePolicy6.setHeightForWidth(self.pushButton_4.sizePolicy().hasHeightForWidth())
        self.pushButton_4.setSizePolicy(sizePolicy6)

        self.gridLayout.addWidget(self.pushButton_4, 10, 4, 1, 2)

        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setObjectName(u"progressBar")
        sizePolicy2.setHeightForWidth(self.progressBar.sizePolicy().hasHeightForWidth())
        self.progressBar.setSizePolicy(sizePolicy2)
        self.progressBar.setValue(90)

        self.gridLayout.addWidget(self.progressBar, 4, 1, 1, 5)

        self.lineEdit_5 = QLineEdit(self.centralwidget)
        self.lineEdit_5.setObjectName(u"lineEdit_5")
        sizePolicy8 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)
        sizePolicy8.setHorizontalStretch(1)
        sizePolicy8.setVerticalStretch(1)
        sizePolicy8.setHeightForWidth(self.lineEdit_5.sizePolicy().hasHeightForWidth())
        self.lineEdit_5.setSizePolicy(sizePolicy8)

        self.gridLayout.addWidget(self.lineEdit_5, 3, 1, 1, 3)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label, 3, 0, 1, 1)

        self.comboBox = QComboBox(self.centralwidget)
        self.comboBox.setObjectName(u"comboBox")
        sizePolicy6.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        self.comboBox.setSizePolicy(sizePolicy6)

        self.gridLayout.addWidget(self.comboBox, 4, 0, 1, 1)

        self.tableView_2 = QTableView(self.centralwidget)
        self.tableView_2.setObjectName(u"tableView_2")
        self.tableView_2.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

        self.gridLayout.addWidget(self.tableView_2, 5, 0, 4, 1)

        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        sizePolicy9 = QSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Fixed)
        sizePolicy9.setHorizontalStretch(1)
        sizePolicy9.setVerticalStretch(1)
        sizePolicy9.setHeightForWidth(self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy9)
        self.pushButton_2.setStyleSheet(u"QMenuBar {\n"
"    background-color: lightblue;\n"
"}\n"
"QMenuBar::item {\n"
"    background-color: lightblue;\n"
"    color: black;\n"
"}\n"
"QMenuBar::item:selected {\n"
"    background-color: darkblue;\n"
"    color: white;\n"
"}\n"
"QToolBar {\n"
"    background-color: lightblue;\n"
"}\n"
"QToolBar QToolButton {\n"
"    background-color: lightblue;\n"
"    color: black;\n"
"}\n"
"QToolBar QToolButton:hover {\n"
"    background-color: darkblue;\n"
"    color: white;\n"
"}")

        self.gridLayout.addWidget(self.pushButton_2, 3, 4, 1, 2)

        self.tableView = QTableView(self.centralwidget)
        self.tableView.setObjectName(u"tableView")
        sizePolicy1.setHeightForWidth(self.tableView.sizePolicy().hasHeightForWidth())
        self.tableView.setSizePolicy(sizePolicy1)
        self.tableView.setStyleSheet(u"background-color: white;\n"
" \n"
"           ")
        self.tableView.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tableView.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableView.setHorizontalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.tableView.horizontalHeader().setVisible(True)

        self.gridLayout.addWidget(self.tableView, 7, 1, 2, 5)

        MainWindows.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindows)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1250, 22))
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName(u"menu")
        self.menu_2 = QMenu(self.menubar)
        self.menu_2.setObjectName(u"menu_2")
        MainWindows.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindows)
        self.statusbar.setObjectName(u"statusbar")
        MainWindows.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menu.addAction(self.actionSetting)
        self.menu_2.addAction(self.actionHISTORY)
        self.menu_2.addAction(self.actionData_outport)

        self.retranslateUi(MainWindows)

        QMetaObject.connectSlotsByName(MainWindows)
    # setupUi

    def retranslateUi(self, MainWindows):
        MainWindows.setWindowTitle(QCoreApplication.translate("MainWindows", u"\u6838\u6843\u8bc6\u522b\u5668", None))
        self.actionHISTORY.setText(QCoreApplication.translate("MainWindows", u"Historical results", None))
        self.actionSetting.setText(QCoreApplication.translate("MainWindows", u"Setting", None))
        self.actionData_outport.setText(QCoreApplication.translate("MainWindows", u"Data outport", None))
        self.label_2.setText(QCoreApplication.translate("MainWindows", u"\u76f8\u4f3c\u5ea6\u5339\u914d\u6a21\u5757", None))
        self.label_8.setText(QCoreApplication.translate("MainWindows", u"\u9608\u503c\uff1a", None))
        self.label_11.setText(QCoreApplication.translate("MainWindows", u"\u6838\u6843\u5339\u914d\u53ca\u68c0\u7d22", None))
        self.image_label_1.setText("")
        self.image_label_7.setText("")
        self.name_label_1.setText("")
        self.name_label_7.setText("")
        self.image_label_2.setText("")
        self.image_label_8.setText("")
        self.name_label_2.setText("")
        self.name_label_8.setText("")
        self.image_label_3.setText("")
        self.image_label_9.setText("")
        self.name_label_3.setText("")
        self.name_label_9.setText("")
        self.image_label_4.setText("")
        self.image_label_10.setText("")
        self.name_label_4.setText("")
        self.name_label_10.setText("")
        self.image_label_5.setText("")
        self.image_label_11.setText("")
        self.name_label_5.setText("")
        self.name_label_11.setText("")
        self.image_label_6.setText("")
        self.name_label_6.setText("")
        self.name_label_12.setText("")
        self.image_label_12.setText("")
        self.label_3.setText(QCoreApplication.translate("MainWindows", u"\u914d\u5bf9\u68c0\u7d22\u6a21\u5757", None))
        self.checkBox_2.setText(QCoreApplication.translate("MainWindows", u"\u5355\u9879\u6a21\u5f0f", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindows", u"\u5237\u65b0", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindows", u"\u53d6\u6d88\u914d\u5bf9", None))
        self.checkBox_3.setText(QCoreApplication.translate("MainWindows", u"\u663e\u793a\u5168\u90e8", None))
        self.label_10.setText(QCoreApplication.translate("MainWindows", u"\u6570\u91cf", None))
        self.pushButton_5.setText(QCoreApplication.translate("MainWindows", u"\u786e\u5b9a\u914d\u5bf9", None))
        self.label_21.setText(QCoreApplication.translate("MainWindows", u"\u914d\u5bf9\u7ed3\u679c\u67e5\u770b", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindows", u"\u68c0\u7d22", None))
        self.label.setText(QCoreApplication.translate("MainWindows", u"\u5386\u53f2\u914d\u5bf9", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindows", u"\u5f00\u59cb\u5339\u914d", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindows", u"\u83dc\u5355", None))
        self.menu_2.setTitle(QCoreApplication.translate("MainWindows", u"\u5de5\u5177", None))
    # retranslateUi

