# Translates VM code into Hack assembly code

import ByteParser
import Codes
import FileManager
from pprint import pprint
import sys
import Writer


def main():

    asmInstructions = []
    codes = Codes.Codes()
    codeWriter = Writer.CodeWriter(codes)
    commands = ByteParser.Commands()
    fileWriter = Writer.FileWriter()
    inputManager = FileManager.InputManager()
    outputFilePath = "/Users/mono/OneDrive/Developer/nand2tetris/Translator/"
    parser = ByteParser.Parser(commands)
    translator = Translator(codes, parser)

    # Validate and get file path(s)
    path = inputManager.validateInput(sys.argv)
    filesToTranslate = inputManager.getFilesInPath(path)

    # Set output file name/path
    outputFilePath = outputFilePath + inputManager.getOutputPath(path)
    codes.inputFileName = inputManager.getOutputName(outputFilePath)

    firstFile = True
    filePaths = [vmFilePath for vmFilePath in filesToTranslate]

    for filePath in filePaths:
        with open(filePath) as vmFile:
            codes.inputFileName = inputManager.getFileName(filePath)

            instructions = [vmInstruction.strip(('\r\n')) for vmInstruction in vmFile if parser.isInstruction(vmInstruction)]

            # Add Sys init bootstrap code
            if firstFile:
                instructions = codeWriter.writeSysInit() + instructions
                firstFile = False

            asmInstructions = asmInstructions + [translator.translate(instruction) for instruction in instructions]

    asmInstructions = [codeWriter.writeInit()] + asmInstructions
    fileWriter.write(asmInstructions, outputFilePath)

class Translator(object):

    def __init__(self, codes, parser):
        self.codes = codes
        self.codeWriter = Writer.CodeWriter(self.codes)
        self.parser = parser

    def translate(self, instruction):
        fields = (self.parser.parse(instruction))

        # Determine the type of command
        command = fields[0]
        commandType = self.parser.commandType(command)

        if commandType  == "arithmetic":
             return self.codeWriter.writeArithmetic(command)

        elif commandType  == "function":
            if command == "function":

                functionName = fields[1]
                functionArgs = fields[2]
                return self.codeWriter.writeFunction(functionName, functionArgs)

            if command == "call":
                functionName = fields[1]
                functionArgs = fields[2]
                return self.codeWriter.writeCall(functionName, functionArgs)

            if command == "return":
                 return self.codeWriter.writeReturn()

        elif commandType  == "memory":
            segment = fields[1]
            index = fields[2]
            return self.codeWriter.writePushPop(command, segment, index)

        # Else, program flow
        elif commandType  == "program":
            programFlowCommand = fields[0]
            label = fields[1]

            if programFlowCommand == "label":
                return self.codeWriter.writeLabel(label)
            elif programFlowCommand == "goto":
                return self.codeWriter.writeGoto(label)
            else:
                return self.codeWriter.writeIf(label)
        else:
            print "Invalid bytecode: command in instruction not recognized."
            exit()
main()
