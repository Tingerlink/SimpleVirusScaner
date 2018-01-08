#!-*-coding:utf-8-*-
import sys
import Api
import BaseManager as bm
import ScannerManager as sm

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import uic

(Ui_MainWindow, QMainWindow) = uic.loadUiType('gui/mainWindow.ui')


class MainWindow(QMainWindow):
    signalCount = pyqtSignal(dict, name='signalCount')
    signalFindVirus = pyqtSignal(dict, name='signalFindVirus')
    signalScanFolder = pyqtSignal(dict, name='signalScanFolder')
    signalScanFile = pyqtSignal(dict, name='signalScanFile')
    signalCommit = pyqtSignal(dict, name='signalCommit')

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.api = Api.ApiOS()
        self.baseManager = bm.BaseManager()
        self.scannerManager = sm.ScannerManager()

        self.pathBase = self.baseManager.loadSettings()
        if (self.pathBase is None):
            self.pathBase = ""
        self.ui.tbBasePath.setText(self.pathBase)

        #self.ui.btnRun.clicked.connect(lambda: self.startScan())

        # Обработчик сигнала
        self.signalCount.connect(self.signalCountHandler, Qt.QueuedConnection)
        self.signalFindVirus.connect(self.signalFindVirusHandler, Qt.QueuedConnection)
        self.signalScanFolder.connect(self.signalScanFolderHandler, Qt.QueuedConnection)
        self.signalScanFile.connect(self.signalScanFileHandler, Qt.QueuedConnection)
        self.signalCommit.connect(self.signalCommitHandler, Qt.QueuedConnection)

    def signalCountHandler(self, data):  # Вызывается для обработки сигнала
        self.ui.lbScanFiles.setText(str(data['countScan']))

    def signalFindVirusHandler(self, data):  # Вызывается для обработки сигнала
        self.ui.ldDetectVirus.setText(str(data['count']))
        line = "Virus name: " + data['newFinds']['virus']['name'] + " : " + data['newFinds']['file']['path'] + "\\" + data['newFinds']['file']['name']

        #{"file" : file, "pattern" : name, "virus": virusPattern, "type" : "in_name"}
        self.ui.listVirus.addItem(line)

    def signalScanFolderHandler(self, data):  # Вызывается для обработки сигнала
        self.ui.lbScanFolder.setText(data['folder'])

    def signalScanFileHandler(self, data):  # Вызывается для обработки сигнала
        self.ui.lbScanFile.setText(data['file'])


    def signalCommitHandler(self, data):  # Вызывается для обработки сигнала
        self.ui.lbScanFolder.setText("...")
        self.ui.lbScanFile.setText("...")
        self.api.send_system_message(self.api.MESSAGE_WARNING, u"Проверка завершина")
        self.ui.btnStart.setEnabled(True)
        self.ui.btnSettings.setEnabled(True)
        self.ui.btnOpenBase.setEnabled(True)
        self.ui.btnOpenFolder.setEnabled(True)
        self.ui.menuSettings.setEnabled(True)
        self.ui.menuStart.setEnabled(True)

    def getVirusBase(self):
        try:
            base = self.baseManager.loadBase(self.pathBase)
            if (base != None):
                self.baseManager.saveSettings(self.pathBase)
            return base
        except:
            return None
        return None

    def __del__(self):
        self.ui = None

    def openDataBaseVirus(self):
        path = self.api.show_open_data_dialog(self)
        if (path != None and path != ""):
            self.ui.tbBasePath.setText(path)

    def openFolderForScan(self):
        path = self.api.show_open_folder_dialog(self)
        if (path != None and path != ""):
            self.ui.tbFolderPath.setText(path)

    def stopScan(self):
        self.scannerManager.isStop = True

    def baseSettings(self):
        self.pathBase = unicode(self.ui.tbBasePath.text())
        if (self.pathBase == None or self.pathBase == ""):
            self.api.send_system_message(self.api.MESSAGE_ERROR, u"Необходимо выбрать базу вирусов")
            return
        master = bm.BaseMaster(self.pathBase, self)
        master.show()

    def startScan(self):
        path = "/"
        flag = False

        self.ui.listVirus.clear()

        settings = {"FileNameScan" : "unused", "FileExiptionScan" : "unused", "FileScan" : "unused"}
        if (self.ui.cbFullScanName.isChecked()):
            settings['FileNameScan'] = "Full"
            flag = True
        if (self.ui.cbSelectedScanName.isChecked()):
            settings['FileNameScan'] = "Selected"
            flag = True

        if (self.ui.cbFullScanExeption.isChecked()):
            settings['FileExiptionScan'] = "Full"
            flag = True
        if (self.ui.cbSelectedScanExeption.isChecked()):
            settings['FileExiptionScan'] = "Selected"
            flag = True

        if (self.ui.cbScanFile.isChecked()):
            settings['FileScan'] = "Use"
            flag = True

        if (not flag):
            self.api.send_system_message(self.api.MESSAGE_ERROR, u"Необходимо выбрать хотя бы один параметр сканирования")
            return


        if (self.ui.tbFolderPath.text() != None and self.ui.tbFolderPath.text() != ""):
            path = self.ui.tbFolderPath.text() + "\\"
        else:
            self.api.send_system_message(self.api.MESSAGE_ERROR, u"Необходимо выбрать папку для сканирования")
            return

        self.scannerManager.isStop = False

        self.pathBase = unicode(self.ui.tbBasePath.text())
        virusBase = self.getVirusBase()

        if (virusBase == None):
            self.api.send_system_message(self.api.MESSAGE_ERROR, u"Необходимо выбрать базу вирусов")
        else:
            self.ui.btnStart.setEnabled(False)
            self.ui.btnSettings.setEnabled(False)
            self.ui.btnOpenBase.setEnabled(False)
            self.ui.btnOpenFolder.setEnabled(False)
            self.ui.menuSettings.setEnabled(False)
            self.ui.menuStart.setEnabled(False)

            self.scannerManager.ScanAll(unicode(path), self.signalCount,
                                        self.signalFindVirus,
                                        self.signalScanFolder,
                                        self.signalScanFile,
                                        self.signalCommit,
                                        virusBase,
                                        settings)


if __name__ == '__main__':
    # create application
    app = QApplication(sys.argv)
    app.setApplicationName(u"Сканер вирусов")

    # create widget
    w = MainWindow()
    w.setWindowTitle(u"Сканер вирусов")
    w.show()

    #f = bm.BaseManager()

    #f.saveSettings("E:\\EasyInstall\\Python\\Май 2017\\id60091236\\scanner\\Scanner\\bases\\base.vscan")
    # connection
    #QObject.connect(app, SIGNAL('lastWindowClosed()'), app, SLOT('quit()'))

    # execute application
    sys.exit(app.exec_())


#cm = CheckM()

##files = FileManager.getFileGeneratorForFolder("C:\\")

#i = 0

#gen = FileManager.getGeneratorForFolder("E:\\")

#for item in gen:
#    for file in item[2]:
#        if (cm.CheckingName(file, "%wan%", True)):
#            print(item[0] + "\\" + file + " Is Virus")

#        if (i % 100 == 0):
#            print(u"Проверено " + str(i))
#        i += 1

