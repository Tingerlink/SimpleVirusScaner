#!-*-coding:utf-8-*-

import FileManager
import Api
import mmap
import sys
from contextlib import closing

class CheckingManager:
    api = Api.ApiOS()

    def splitFileName(self, fileName):
        sep = '.'
        vals = fileName.split(sep)
        name = ""
        extension = ""

        for i in range(len(vals)):
            if (i == 0):
                name = vals[i]
                continue

            if (i < len(vals) - 1):
                name += sep + vals[i]
                continue

            extension = vals[i]

        return {"name":name, "extension":extension}    

   
    def CheckingName(self, fileName, pattern, deepScan = False):
        file = self.splitFileName(fileName)

        if (not deepScan):
            if (unicode(file['name']) == pattern and not unicode(file['extension']) in self.api.EXCEPTIONS):
                return True
        else:
            if (unicode(file['name']).find(pattern) > -1 and not unicode(file['extension']) in self.api.EXCEPTIONS):
                return True
        return False

    def CheckingExtension(self, fileName, pattern, deepScan = False):
        file = self.splitFileName(fileName)
                
        if (not deepScan):
            if (unicode(file['extension']) == pattern and not unicode(file['extension']) in self.api.EXCEPTIONS):
                return True
        else:
            if (unicode(file['extension']).find(pattern) > -1 and not unicode(file['extension']) in self.api.EXCEPTIONS):
                return True
        return False

    def ChackingFileByBinaryPattern(self, path, pattern):       
        try:
            file = self.splitFileName(path)
            if (unicode(file['extension']) in self.api.EXCEPTIONS):
                return False

            with open(path, 'rb', 0) as file, \
                closing(mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ)) as s:
                    if (s.find(pattern) != -1):
                        return True
        except:
            return False
        return False

    def CheckWithGenerator():
        gen = FileManager.getGeneratorForFolder()

