# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'viewer.ui'
#
# Created: Mon Aug 11 12:44:35 2014
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.setEnabled(True)
        MainWindow.resize(540, 810)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("resources/icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.imageWidget = ImageWidget(self.centralwidget)
        self.imageWidget.setOrientation(QtCore.Qt.Vertical)
        self.imageWidget.setObjectName(_fromUtf8("imageWidget"))
        self.verticalLayout_2.addWidget(self.imageWidget)
        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.exposureTimeBox = QtGui.QSpinBox(self.groupBox)
        self.exposureTimeBox.setMinimum(10)
        self.exposureTimeBox.setMaximum(5000)
        self.exposureTimeBox.setSingleStep(10)
        self.exposureTimeBox.setProperty("value", 100)
        self.exposureTimeBox.setObjectName(_fromUtf8("exposureTimeBox"))
        self.gridLayout_2.addWidget(self.exposureTimeBox, 0, 1, 1, 1)
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 0, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_2)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.groupBox_2 = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.gridLayout = QtGui.QGridLayout(self.groupBox_2)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.gridLayout_3 = QtGui.QGridLayout()
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.scaleMinBox = QtGui.QSpinBox(self.groupBox_2)
        self.scaleMinBox.setMaximum(99999)
        self.scaleMinBox.setSingleStep(20)
        self.scaleMinBox.setObjectName(_fromUtf8("scaleMinBox"))
        self.gridLayout_3.addWidget(self.scaleMinBox, 0, 1, 1, 1)
        self.autoscaleButton = QtGui.QCheckBox(self.groupBox_2)
        self.autoscaleButton.setChecked(True)
        self.autoscaleButton.setObjectName(_fromUtf8("autoscaleButton"))
        self.gridLayout_3.addWidget(self.autoscaleButton, 2, 1, 1, 1)
        self.scaleMaxBox = QtGui.QSpinBox(self.groupBox_2)
        self.scaleMaxBox.setMinimum(1)
        self.scaleMaxBox.setMaximum(99999)
        self.scaleMaxBox.setSingleStep(10)
        self.scaleMaxBox.setProperty("value", 2000)
        self.scaleMaxBox.setObjectName(_fromUtf8("scaleMaxBox"))
        self.gridLayout_3.addWidget(self.scaleMaxBox, 1, 1, 1, 1)
        self.colormapBox = QtGui.QComboBox(self.groupBox_2)
        self.colormapBox.setObjectName(_fromUtf8("colormapBox"))
        self.gridLayout_3.addWidget(self.colormapBox, 3, 1, 1, 1)
        self.label_2 = QtGui.QLabel(self.groupBox_2)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_3.addWidget(self.label_2, 0, 0, 1, 1)
        self.label_5 = QtGui.QLabel(self.groupBox_2)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout_3.addWidget(self.label_5, 3, 0, 1, 1)
        self.label_3 = QtGui.QLabel(self.groupBox_2)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout_3.addWidget(self.label_3, 1, 0, 1, 1)
        self.rescaleButton = QtGui.QPushButton(self.groupBox_2)
        self.rescaleButton.setObjectName(_fromUtf8("rescaleButton"))
        self.gridLayout_3.addWidget(self.rescaleButton, 0, 3, 1, 1)
        self.rotateCWButton = QtGui.QPushButton(self.groupBox_2)
        self.rotateCWButton.setEnabled(True)
        self.rotateCWButton.setObjectName(_fromUtf8("rotateCWButton"))
        self.gridLayout_3.addWidget(self.rotateCWButton, 1, 3, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem1, 0, 2, 1, 1)
        self.rotateCCWButton = QtGui.QPushButton(self.groupBox_2)
        self.rotateCCWButton.setObjectName(_fromUtf8("rotateCCWButton"))
        self.gridLayout_3.addWidget(self.rotateCCWButton, 1, 2, 1, 1)
        self.showROIBox = QtGui.QCheckBox(self.groupBox_2)
        self.showROIBox.setEnabled(True)
        self.showROIBox.setObjectName(_fromUtf8("showROIBox"))
        self.gridLayout_3.addWidget(self.showROIBox, 3, 3, 1, 1)
        self.flipVerticalButton = QtGui.QPushButton(self.groupBox_2)
        self.flipVerticalButton.setObjectName(_fromUtf8("flipVerticalButton"))
        self.gridLayout_3.addWidget(self.flipVerticalButton, 2, 2, 1, 1)
        self.flipHorizontalButton = QtGui.QPushButton(self.groupBox_2)
        self.flipHorizontalButton.setObjectName(_fromUtf8("flipHorizontalButton"))
        self.gridLayout_3.addWidget(self.flipHorizontalButton, 2, 3, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_3, 0, 0, 2, 1)
        self.verticalLayout_2.addWidget(self.groupBox_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.adjustROIButton = QtGui.QPushButton(self.centralwidget)
        self.adjustROIButton.setObjectName(_fromUtf8("adjustROIButton"))
        self.horizontalLayout.addWidget(self.adjustROIButton)
        self.roiStatisticsButton = QtGui.QToolButton(self.centralwidget)
        self.roiStatisticsButton.setObjectName(_fromUtf8("roiStatisticsButton"))
        self.horizontalLayout.addWidget(self.roiStatisticsButton)
        self.cameraSettingsButton = QtGui.QToolButton(self.centralwidget)
        self.cameraSettingsButton.setObjectName(_fromUtf8("cameraSettingsButton"))
        self.horizontalLayout.addWidget(self.cameraSettingsButton)
        self.acquisitionButton = QtGui.QPushButton(self.centralwidget)
        self.acquisitionButton.setObjectName(_fromUtf8("acquisitionButton"))
        self.horizontalLayout.addWidget(self.acquisitionButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 540, 29))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        self.menuRing_Buffer = QtGui.QMenu(self.menubar)
        self.menuRing_Buffer.setObjectName(_fromUtf8("menuRing_Buffer"))
        MainWindow.setMenuBar(self.menubar)
        self.statusBar = QtGui.QStatusBar(MainWindow)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        MainWindow.setStatusBar(self.statusBar)
        self.actionSaveAs = QtGui.QAction(MainWindow)
        self.actionSaveAs.setObjectName(_fromUtf8("actionSaveAs"))
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.actionAbout = QtGui.QAction(MainWindow)
        self.actionAbout.setEnabled(False)
        self.actionAbout.setObjectName(_fromUtf8("actionAbout"))
        self.actionEnable = QtGui.QAction(MainWindow)
        self.actionEnable.setCheckable(True)
        self.actionEnable.setChecked(True)
        self.actionEnable.setObjectName(_fromUtf8("actionEnable"))
        self.actionView = QtGui.QAction(MainWindow)
        self.actionView.setObjectName(_fromUtf8("actionView"))
        self.menuFile.addAction(self.actionSaveAs)
        self.menuFile.addAction(self.actionExit)
        self.menuHelp.addAction(self.actionAbout)
        self.menuRing_Buffer.addAction(self.actionEnable)
        self.menuRing_Buffer.addAction(self.actionView)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuRing_Buffer.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "qCamera Viewer", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("MainWindow", "Exposure settings", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Exposure time [ms]", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("MainWindow", "Viewing Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.autoscaleButton.setText(QtGui.QApplication.translate("MainWindow", "Autoscale", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Scale min", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("MainWindow", "Colormap", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "Scale max", None, QtGui.QApplication.UnicodeUTF8))
        self.rescaleButton.setText(QtGui.QApplication.translate("MainWindow", "Rescale", None, QtGui.QApplication.UnicodeUTF8))
        self.rotateCWButton.setText(QtGui.QApplication.translate("MainWindow", "Rotate CW", None, QtGui.QApplication.UnicodeUTF8))
        self.rotateCCWButton.setText(QtGui.QApplication.translate("MainWindow", "Rotate CCW", None, QtGui.QApplication.UnicodeUTF8))
        self.showROIBox.setText(QtGui.QApplication.translate("MainWindow", "Show ROI", None, QtGui.QApplication.UnicodeUTF8))
        self.flipVerticalButton.setText(QtGui.QApplication.translate("MainWindow", "Flip vertical", None, QtGui.QApplication.UnicodeUTF8))
        self.flipHorizontalButton.setText(QtGui.QApplication.translate("MainWindow", "Flip horizontal", None, QtGui.QApplication.UnicodeUTF8))
        self.adjustROIButton.setText(QtGui.QApplication.translate("MainWindow", "Adjust ROI", None, QtGui.QApplication.UnicodeUTF8))
        self.roiStatisticsButton.setText(QtGui.QApplication.translate("MainWindow", "ROI statistics...", None, QtGui.QApplication.UnicodeUTF8))
        self.cameraSettingsButton.setText(QtGui.QApplication.translate("MainWindow", "Camera settings...", None, QtGui.QApplication.UnicodeUTF8))
        self.acquisitionButton.setText(QtGui.QApplication.translate("MainWindow", "Begin acquisition", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("MainWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHelp.setTitle(QtGui.QApplication.translate("MainWindow", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.menuRing_Buffer.setTitle(QtGui.QApplication.translate("MainWindow", "Ring Buffer", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSaveAs.setText(QtGui.QApplication.translate("MainWindow", "Save image as...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit.setText(QtGui.QApplication.translate("MainWindow", "Exit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout.setText(QtGui.QApplication.translate("MainWindow", "About", None, QtGui.QApplication.UnicodeUTF8))
        self.actionEnable.setText(QtGui.QApplication.translate("MainWindow", "Enabled", None, QtGui.QApplication.UnicodeUTF8))
        self.actionView.setText(QtGui.QApplication.translate("MainWindow", "View", None, QtGui.QApplication.UnicodeUTF8))

from guiqwt.plot import ImageWidget
