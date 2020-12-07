from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2 import QtGui
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omUi

from saveLoadLocator.core import matchLocator as match_Loc
from saveLoadLocator.core import qc_at10k as qc_at10k
from saveLoadLocator.core import createLocatorAtSelection as create_Loc

for module in [match_Loc, create_Loc, qc_at10k]:
    reload(module)

def maya_main_window():
    """
    Get Maya main window
    :return: int (maya main ptr)
    """
    maya_main_ptr = omUi.MQtUtil.mainWindow()
    return wrapInstance(int(maya_main_ptr), QtWidgets.QWidget)


class MainDialog(QtWidgets.QDialog):
    def __init__(self, parent=maya_main_window()):
        super(MainDialog, self).__init__(parent)
        self.setWindowTitle('Create/Match Locators')
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        """
        pyside2 create widgets and set defaults
        :return: None
        """
        self.sclLineEdit = QtWidgets.QLineEdit('0.5')
        self.sclLineEdit.setValidator(QtGui.QDoubleValidator())
        self.sclLineEdit.setMaximumWidth(45)

        self.translate_checkBox = QtWidgets.QCheckBox('Trans')
        self.translate_checkBox.setChecked(True)

        self.rotate_checkBox = QtWidgets.QCheckBox('Rot')
        self.rotate_checkBox.setChecked(True)

        self.scale_checkBox = QtWidgets.QCheckBox('Scl')
        self.scale_checkBox.setChecked(False)



        self.match_btn = QtWidgets.QPushButton('Match Locator')
        self.qc_btn = QtWidgets.QPushButton('QC at 10k')
        self.divider = QtWidgets.QLabel('--------------------')
        self.divider.setAlignment(QtCore.Qt.AlignCenter)
        self.create_btn = QtWidgets.QPushButton('Create Locator')


    def create_layout(self):
        """
        pyside2 create layout
        :return: None
        """
        self.checkBox_hBox = QtWidgets.QHBoxLayout()
        self.checkBox_hBox.addStretch()
        self.checkBox_hBox.addWidget(self.translate_checkBox)
        self.checkBox_hBox.addWidget(self.rotate_checkBox)
        self.checkBox_hBox.addWidget(self.scale_checkBox)
        self.checkBox_hBox.addStretch()

        self.creatBtn_hBoxLayout = QtWidgets.QHBoxLayout()
        self.creatBtn_hBoxLayout.addWidget(self.create_btn)
        self.creatBtn_hBoxLayout.addWidget(self.sclLineEdit)

        # create button layout
        self.btn_vBoxLayout = QtWidgets.QVBoxLayout()
        self.btn_vBoxLayout.addWidget(self.match_btn)
        self.btn_vBoxLayout.addWidget(self.qc_btn)
        self.btn_vBoxLayout.addStretch()
        self.btn_vBoxLayout.addWidget(self.divider)
        self.btn_vBoxLayout.addLayout(self.creatBtn_hBoxLayout)



        # create and add to main layout
        self.main_vBoxLayout = QtWidgets.QVBoxLayout(self)
        self.main_vBoxLayout.addLayout(self.checkBox_hBox)
        self.main_vBoxLayout.addLayout(self.btn_vBoxLayout)


    def create_connections(self):
        """
        pyside2 create connections
        :return: None
        """

        self.match_btn.clicked.connect(self.mtachLoc)
        self.qc_btn.clicked.connect(self.qc)
        self.create_btn.clicked.connect(self.createLoc)

    def qc(self):
        qc_at10k.qc_at10k()

    def mtachLoc(self):
        """
        pyside2 connection instructions for load ctrl button
        :return: None
        """
        applyTrans = False
        applyRot = False
        applyScale = False

        if self.translate_checkBox.isChecked():
            applyTrans = True

        if self.rotate_checkBox.isChecked():
            applyRot = True

        if self.scale_checkBox.isChecked():
            applyScale = True

        match_Loc.mtachLocatorTransform(applyTrans, applyRot, applyScale)

    def createLoc(self):
        locScl = self.sclLineEdit.text()
        create_Loc.createLocatorAtObject(float(locScl))

"""
from saveLoadLocator.ui import ui

if __name__ == '__main__':

    global open_import_dialog
    try:
        open_import_dialog.close()
        open_import_dialog.deleteLater()
    except:
        pass
    open_import_dialog = ui.MainDialog()
    open_import_dialog.show()
"""

