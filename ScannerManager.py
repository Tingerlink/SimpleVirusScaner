#!-*-coding:utf-8-*-

import sys
import time
import threading
import Api

import CheckingManager
import FileManager as fm

class ScannerManager:

    isStop = False
    api = Api.ApiOS()

    def thread(my_func):
        def wrapper(*args, **kwargs):
            my_thread = threading.Thread(target=my_func, args=args, kwargs=kwargs)
            my_thread.start()
        return wrapper

    @thread
    def ScanAll(self, path, signalCount, signalFindVirus, signalScanFolder, signalScanFile, commit, virusBase, settings):
        gen = fm.getGeneratorForFolder(path)
      
        i = 0
        countVirus = 0
        for item in gen:
            if (self.isStop):
                commit.emit({"status" : "commit"})
                return
            for file in item[2]:                      
                signalScanFile.emit({"file" : file})        
                signalScanFolder.emit({"folder" : item[0]}) 
                 
                result = self.checkFileWithBase({"name":file, "path":item[0]+"\\"+file}, virusBase, settings)

                if (result != None):
                    countVirus += 1
                    signalFindVirus.emit({"count" : countVirus, "newFinds": result})             
                
                i += 1
                signalCount.emit({"countScan" : i})
                
        commit.emit({"status" : "commit"})

    def checkFileWithBase(self, file, virusBase, settings):
        cm = CheckingManager.CheckingManager()

        for virusPattern in virusBase:
            if (settings['FileNameScan'] != "unused"):
                for name in virusPattern['fnames']:
                    if (name == ""):
                        continue
                    if (cm.CheckingName(file['name'], name, settings['FileNameScan'] == "Selected")):
                        return {"file" : file, "pattern" : name, "virus": virusPattern, "type" : "in_name"}
            
            if (settings['FileExiptionScan'] != "unused"):
                for fexeption in virusPattern['fexeptions']:
                    if (fexeption == ""):
                        continue
                    if (cm.CheckingExtension(file['name'], fexeption, settings['FileExiptionScan'] == "Selected")):
                        return {"file" : file, "pattern" : fexeption, "virus": virusPattern, "type" : "in_exeption"}

            if (settings['FileScan'] != "unused"):
                for data in virusPattern['patterns']:
                    if (data == ""):
                        continue
                    if (cm.ChackingFileByBinaryPattern(file['path'], data)):
                        return {"file" : file, "pattern" : data, "virus": virusPattern, "type" : "in_exeption"}
        
        return None