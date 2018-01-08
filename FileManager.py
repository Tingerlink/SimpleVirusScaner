#!-*-coding:utf-8-*-

import os

def getFileForFolder(path):
    objectGenerator = os.walk(path)
    files = []
    for item in objectGenerator:
        files.append({"path" : item[0], "files" : item[2]})
       
    return files

def getGeneratorForFolder(path):
    objectGenerator = os.walk(path)

    return objectGenerator

