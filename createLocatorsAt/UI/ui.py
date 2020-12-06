from PySide2 import QtCore
from PySide2 import QtWidgets
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omUi

import sys
if not "C:\\tools\\mayaTools" in sys.path:
    sys.path.append("C:\\tools\\mayaTools")

import createLocatorsAt.core.createLocAtSelection as c_loc
reload(c_loc)

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
        self.setWindowTitle('Create Locators')

        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        """
        pyside2 create widgets and set defaults
        :return: None
        """

        self.levelSpinBox = QtWidgets.QSpinBox()
        self.levelSpinBox.setValue(3)

        self.trans_checkBox = QtWidgets.QCheckBox('Trans')
        self.trans_checkBox.setChecked(True)
        self.rot_checkBox = QtWidgets.QCheckBox('Rot')
        self.rot_checkBox.setChecked(True)
        self.scl_checkBox = QtWidgets.QCheckBox('Scl')
        self.scl_checkBox.setChecked(True)

        self.match_btn = QtWidgets.QPushButton('Match Locator')
        self.create_btn = QtWidgets.QPushButton('Create Locator')

    def create_layout(self):
        """
        pyside2 create layout
        :return: None
        """
        self.check_hBoxLayout = QtWidgets.QHBoxLayout()
        self.check_hBoxLayout.addStretch()
        self.check_hBoxLayout.addWidget(self.trans_checkBox)
        self.check_hBoxLayout.addWidget(self.rot_checkBox)
        self.check_hBoxLayout.addWidget(self.scl_checkBox)
        self.check_hBoxLayout.addStretch()

        # create button layout
        self.btn_vBoxLayout = QtWidgets.QVBoxLayout()
        self.btn_vBoxLayout.addWidget(self.match_btn)
        self.btn_vBoxLayout.addWidget(self.create_btn)

        # create and add to main layout
        self.main_vBoxLayout = QtWidgets.QVBoxLayout(self)
        self.main_vBoxLayout.addLayout(self.check_hBoxLayout)
        self.main_vBoxLayout.addLayout(self.btn_vBoxLayout)


    def create_connections(self):
        """
        pyside2 create connections
        :return: None
        """
        self.match_btn.clicked.connect(self.match_Loc)
        self.create_btn.clicked.connect(self.create_Loc)

    def create_Loc(self):
        c_loc.createLocAtSelection()

    def match_Loc(self):
        """
        pyside2 connection instructions for load ctrl button
        :return: None
        """
        matchScl = False
        loadBuffers = False
        if self.rot_checkBox.isChecked():
            matchScl = True

        if self.trans_checkBox.isChecked():
            loadBuffers = True

        c_loc.matchLoc(self.lineEdit.text(), matchScl=matchScl, loadBuffers=loadBuffers)


if __name__ == '__main__':

    global open_import_dialog
    try:
        open_import_dialog.close()
        open_import_dialog.deleteLater()
    except:
        pass
    open_import_dialog = MainDialog()
    open_import_dialog.show()
