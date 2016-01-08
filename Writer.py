__author__ = 'mono'
NEWLINE = "\n"

import sys

class CodeWriter(object):

    def __init__(self, codes):
        self.codes = codes
        self.subValues = {

            "THAT":1,
            "THIS":2,
            "ARG":3,
            "LCL":4

        }

    def repositionSP(self, operator):
        operation = self.codes.spOperators[operator]
        return \
        "@SP" + NEWLINE + \
        operation

    def restore(self, segment):
        codeToGetRestoreValue = ""
        subValue = str(self.subValues[segment])

        if subValue == 1:
            codeToGetRestoreValue = "@R14" + NEWLINE + "D=M-" + subValue
        else:
            codeToGetRestoreValue = "@" + subValue + NEWLINE + "D=A" + NEWLINE + "@R14" + NEWLINE + "D=M-D"

        return \
        codeToGetRestoreValue + NEWLINE + \
        self.restoreSegment(segment)

    def restoreSegment(self, segment):
        return \
        "A=D" + NEWLINE + \
        "D=M" + NEWLINE + \
        "@" + segment + NEWLINE + \
        "M=D"

    def save(self, value):
        '''
        :param value: named variable to save before calling function
        :returns: code that saves named variable by pushing it onto the stack
        '''
        return \
        "@" + value + NEWLINE + \
        "D=M" + NEWLINE + \
        "@SP" + NEWLINE + \
        "A=M" + NEWLINE + \
        "M=D" + NEWLINE + \
        self.repositionSP("increment")

    def setFileName(self, fileName):
        '''
        Informs the code writer that the translation of a new VM file is started.
        :param fileName: string
        :return:
        '''
        pass

    def writeArithmetic(self, operation):
        '''
        Writes the assembly code that is the translation of the given arithmetic command.
        :param command: string
        :return:
        '''
        return self.codes.arithmetic(operation)

    def writeCall(self, functionName, numArgs):
        '''
        Writes the assembly code that calls a function with numArgs args
        :param functionName: string
        :param numArgs: int
        :return: string
        '''
        self.codes.counts["function"] += 1
        returnAddress = "RET_ADD_CALL" + str(self.codes.counts["function"])
        return \
        "@" + returnAddress + NEWLINE + \
        "D=A" + NEWLINE + \
        "@SP" + NEWLINE + \
        "A=M" + NEWLINE + \
        "M=D" + NEWLINE + \
        "@SP" + NEWLINE + \
        "M=M+1" + NEWLINE + \
        self.save("LCL") + NEWLINE + \
        self.save("ARG") + NEWLINE + \
        self.save("THIS") + NEWLINE + \
        self.save("THAT") + NEWLINE + \
        "@" + numArgs + NEWLINE + \
        "D=A" + NEWLINE + \
        "@SP" + NEWLINE + \
        "D=M-D" + NEWLINE + \
        "@R15" + NEWLINE + \
        "M=D" + NEWLINE + \
        "@5" + NEWLINE + \
        "D=A" + NEWLINE + \
        "@R15" + NEWLINE + \
        "D=M-D" + NEWLINE + \
        "@ARG" + NEWLINE + \
        "M=D" + NEWLINE + \
        "@SP" + NEWLINE + \
        "D=M" + NEWLINE + \
        "@LCL" + NEWLINE + \
        "M=D" + NEWLINE + \
        self.writeGoto(functionName) + \
        self.writeLabel(returnAddress)

    def writeFunction(self, functionName, numLocals):
        '''
        :param functionName: string
        :param numLocals: int
        :return: string
        '''
        numLocals = int(numLocals)
        pushes = ""
        for value in range(0, numLocals):
            pushes = pushes + self.codes.push("constant", str(0))

        return \
        "(" + functionName + ")" + NEWLINE + \
        pushes

    def writeGoto(self, label):
        '''
        Writes an address to go to
        :param label: string
        :return: string
        '''
        return \
        "@" + label + NEWLINE + \
        "0; JMP" + NEWLINE

    def writeIf(self, label):
        '''
        :param label: string
        :return: string
        '''
        return \
        "@SP" + NEWLINE + \
        "M=M-1" + NEWLINE + \
        "A=M" + NEWLINE + \
        "D=M" + NEWLINE + \
        "@" + label + NEWLINE + \
        "D;JNE" + NEWLINE

    def writeInit(self):
        '''
        Sets the stack pointer to memory address 256 0x100
        :return: string
        '''
        return "@256" + NEWLINE + "D=A" + NEWLINE + "@SP" + NEWLINE + "M=D" + NEWLINE

    def writeLabel(self, label):
        '''
        :param label: string
        :return: string
        '''
        return "(" + label + ")" + NEWLINE

    def writeReturn(self):
        return \
        "@LCL" + NEWLINE + \
        "D=M" + NEWLINE + \
        "@R14" + NEWLINE + \
        "M=D" + NEWLINE + \
        "@5" + NEWLINE + \
        "D=A" + NEWLINE + \
        "@R14" + NEWLINE + \
        "D=M-D" + NEWLINE + \
        "A=D" + NEWLINE + \
        "D=M" + NEWLINE + \
        "@R13" + NEWLINE + \
        "M=D" + NEWLINE + \
        "@SP" + NEWLINE + \
        "M=M-1" + NEWLINE + \
        "A=M" + NEWLINE + \
        "D=M" + NEWLINE + \
        "@ARG" + NEWLINE + \
        "A=M" + NEWLINE + \
        "M=D" + NEWLINE + \
        "@ARG" + NEWLINE + \
        "D=M+1" + NEWLINE + \
        "@SP" + NEWLINE + \
        "M=D" + NEWLINE + \
        self.restore("THAT") + NEWLINE + \
        self.restore("THIS") + NEWLINE + \
        self.restore("ARG") + NEWLINE + \
        self.restore("LCL") + NEWLINE + \
        "@R13" + NEWLINE + \
        "A=M" + NEWLINE + \
        "0;JMP" + NEWLINE

    def writePushPop(self, command, segment, index):
        '''
        Writes the assembly code that is the translation of the given command, where command is either C_PUSH or C_POP.
        :param command: C_PUSH or C_POP)
        :param segment: string
        :param index: int
        :return: null
        '''
        if command == "push":
            return self.codes.push(segment, index)
        return self.codes.pop(segment, index)

    def writeSysInit(self):
        return ["call Sys.init 0"]

class FileWriter(object):
    def write(self, instructions, outputFilePath):
        try:
            f = open(outputFilePath, "w")
            for instruction in instructions:
                f.write(instruction)
            f.close()

        except IOError as e :
            print "I/O error({0}): {1}".format(e.errno, e.strerror) + "instruction:" + instruction

        except ValueError:
            print "Value error"

        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise