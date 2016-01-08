__author__ = 'mono'

import os
import sys

fileExtension = ".jack"

class InputManager(object):

    def __init__(self, sys.argv):

        self.outputFilePath = ""
        self.outputName = ""
        self.filesToTranslate = []

    def validateInput(self, argv):

        if len(argv) != 2:

            self.showUsage()
            exit()

        return argv[1]

    def getFileName(self, path):
        return path.split("/")[2]

    def getFilesInPath(self, path):
        return [path + fileName for fileName in os.listdir(path) if VM_FILE_EXT in fileName]

    def getOutputPath(self, path):
        splitPath = path.split("/")
        self.outputName = splitPath[1]
        return splitPath[0] + "/" + splitPath[1] + "/" + splitPath[1] + ASM_FILE_EXT

    def getOutputName(self, path):
        return self.outputName

    def showUsage(self):
        print("Usage: Translator fileDir")
