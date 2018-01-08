#!-*-coding:utf-8-*-

import os
import json
from PyQt4.QtGui import *
from PyQt4 import uic
from PyQt4.QtCore import *

(Ui_BaseMaster, QWidget) = uic.loadUiType('gui/base.ui')

class BaseMaster(QWidget):
    def __init__(self, path, parent=None):
        super(BaseMaster, self).__init__(parent)
        self.setWindowFlags(Qt.Dialog | Qt.WindowSystemMenuHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle("Модальное окно")
        
        self.ui = Ui_BaseMaster()
        self.ui.setupUi(self)
        self.bm = BaseManager()
    
        self.basePath = path
      
        self.baseVirus = self.bm.loadBase(path)
        self.setBase()
    
    def addNewVirusToBase(self, virusName):
        if (self.baseVirus == None):
            self.baseVirus = []
        self.baseVirus.append({"name": unicode(virusName), "patterns": [], "fnames": [], "fexeptions": []})

        self.bm.saveBase(self.baseVirus, self.basePath)
        self.setBase()

    def addNewVirus(self):
        virusName = self.ui.tbNewVirus.text()
        self.addNewVirusToBase(virusName)

    def deleteCurrentRow(self):
        index = self.ui.listVirus.currentRow()

        if (index > -1):
            self.baseVirus.remove(self.baseVirus[index])
            self.bm.saveBase(self.baseVirus, self.basePath)
            self.setBase()

    def renameVirus(self):
        name = unicode(self.ui.tbVirusName.toPlainText())
        index = self.ui.listVirus.currentRow()
        if (name != "" and index > -1):
            self.baseVirus[index]['name'] = name
            self.bm.saveBase(self.baseVirus, self.basePath)
            self.setBase()


    def itemChacked(self, index):        
        index = self.ui.listVirus.currentRow()
        self.ui.tbVirusName.setText(self.baseVirus[index]['name'])
        self.setByBase(index)

    def setByBase(self, index):
        self.setNames(self.baseVirus[index]['fnames'])
        self.setExiptions(self.baseVirus[index]['fexeptions'])
        self.setFilePatterns(self.baseVirus[index]['patterns'])

    def setNames(self, arr):
        data = ""
        for item in arr:
            data += item + "\n"
        self.ui.tbName.setText(data)

    def setExiptions(self, arr):
        data = ""
        for item in arr:
            data += item + "\n"
        self.ui.tbExiption.setText(data)

    def setFilePatterns(self, arr):
        data = ""
        for item in arr:
            data += item + "\n"
        self.ui.tbFile.setText(data)


    def parsePatterns(self, QTextEdit):
        patterns = unicode(QTextEdit.toPlainText()).split("\n")

        return patterns

    def apply(self):
        index = self.ui.listVirus.currentRow()
        fnames = self.parsePatterns(self.ui.tbName)
        fexeptions = self.parsePatterns(self.ui.tbExiption)
        patterns = self.parsePatterns(self.ui.tbFile)

        self.baseVirus[index]['fnames'] = fnames
        self.baseVirus[index]['fexeptions'] = fexeptions
        self.baseVirus[index]['patterns'] = patterns

        self.bm.saveBase(self.baseVirus, self.basePath)
        self.setBase()


    def setBase(self):
        try:
            self.ui.listVirus.addItems([])
            self.ui.listVirus.clear()
        except:
            pass
        for virus in self.baseVirus:
            self.ui.listVirus.addItem(virus['name'])

    def __del__(self):
        self.ui = None


class BaseManager:

    def save_base(self, base, path):
        with open(path, 'w') as outfile:
            json.dump(base, outfile)

    def loadBase(self, path):
        if (os.path.isfile(path)):
            with open(path) as json_data:
                base = json.load(json_data)
                return base
    
    def saveSettings(self, pathBase, pathSettings="settings.svscan"):
        with open(pathSettings, 'w') as outfile:
            json.dump({"pathBase" : pathBase}, outfile)

    def loadSettings(self, pathSettings="settings.svscan"):
        if (os.path.isfile(pathSettings)):
            with open(pathSettings) as json_data:
                settings = json.load(json_data)

                if ("pathBase" in settings and os.path.isfile(settings['pathBase'])):
                    return settings['pathBase']

        return None





