import mayaTools.saveLoadCtrls.ui.ui as mainUI


if __name__ == '__main__':

    global open_import_dialog
    try:
        open_import_dialog.close()
        open_import_dialog.deleteLater()
    except:
        pass
    open_import_dialog = mainUI.MainDialog()
    open_import_dialog.show()
