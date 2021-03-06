# -*- coding: utf-8 -*-
"""
/***************************************************************************
 LoadQSS
                                 A QGIS plugin
 Configure look and feel
                             -------------------
        begin                : 2015-04-29
        copyright            : (C) 2015 All4Gis.
        email                : franka1986 at gmail dot com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 #   any later version.                                                    *
 *                                                                         *
 ***************************************************************************/
"""
# Import the PyQt and QGIS libraries
from .AboutQSSDialog import AboutQSSDialog
from LoadQSS.gui.generated.Load_QSS import Ui_LoadQSSDialog
from LoadQSS.utils.utils import *
from qgis.PyQt.QtCore import Qt
from qgis.gui import *
import os

try:
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *
    from PyQt5.QtWidgets import *
except ImportError:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *


# try:
#     from pydevd import *
# except ImportError:
#     None


class LoadQSSDialog(QDialog, Ui_LoadQSSDialog):
    def __init__(self, iface):
        QDialog.__init__(self)
        self.setupUi(self)
        self.iface = iface
        self.lastOpenedFile = None
        self.app = QApplication.instance()
        self.listStyles.addItems(getStyleList())
        self.currentItem = None

    # Copy style to examples plugin folder
    def to_exmples_folder(self, folder, stylesheet):
        return os.path.join(self.plugin_dir, "examples", folder, stylesheet)

    # About
    def About(self):
        self.About = AboutQSSDialog(self.iface)
        self.About.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint)
        self.About.exec_()

    # Selected row
    def SelectRow(self, checked):
        if checked:
            self.Delete_btn.setEnabled(True)
            self.Activate_btn.setEnabled(True)
            self.currentItem = checked
            self.ApplyStyle(preview=True)
        else:
            self.Delete_btn.setEnabled(False)
            self.Activate_btn.setEnabled(False)
            self.currentItem = None

    # Add new qss
    def AddStyle(self):
        self.filename, _ = QFileDialog.getOpenFileName(self, "Open qss",
                                                       self.lastOpenedFile,
                                                       "*.qss")
        if self.filename:
            flags = Qt.WindowSystemMenuHint | Qt.WindowTitleHint
            text, ok = QInputDialog.getText(self, 'Style Name',
                                            'Enter name for Style:',
                                            flags=flags)
            if ok:
                if text == "":
                    self.iface.messageBar().clearWidgets()
                    self.iface.messageBar().pushMessage("Error: ",
                                                        "Enter theme name.",
                                                        level=QgsMessageBar.CRITICAL,
                                                        duration=3)
                    return

                # Add to list
                self.listStyles.addItem(text)
                # TODO :Copy style to examples folder
                AddNewStyle(text, self.filename)

        return

    # Remove style in list
    def DeleteStyle(self):
        try:
            if(self.currentItem.text() == getPreview()):
                if (self.currentItem.text() == getActivated()):
                    ret = QMessageBox.question(self, 'Delete Style : '
                                               + self.currentItem.text(),
                                               'The style you are about to remove is your active style.\n' +
                                               'The default Qgis style will be set.\n' +
                                               'Are you sure you want to remove it?',
                                               QMessageBox.Yes |
                                               QMessageBox.No, QMessageBox.No)
                    if ret == QMessageBox.Yes:
                        self.ResetStyle()
                    if ret == QMessageBox.No:
                        return
                else:
                    activateStyle(getActivated(), self.iface)
        except Exception:
            None

        self.listStyles.takeItem(self.listStyles.currentRow())
        delStyle(self.currentItem.text())
        self.Delete_btn.setEnabled(False)
        self.Activate_btn.setEnabled(False)
        self.currentItem = None

        return

    # Apply style
    def ApplyStyle(self, preview=False):
        try:
            activateStyle(self.currentItem.text(), self.iface, preview)
        except Exception:
            None
        return

    # Restores style
    def ResetStyle(self):
        self.app.setStyleSheet("")
        setActivated("")
        return

    # Close dialog
    def closeEvent(self, evt):
        activateStyle(getActivated(), self.iface, close=True)
        return
