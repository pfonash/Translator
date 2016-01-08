__author__ = 'mono'

NEWLINE = "\n"

class Addresser(object):

    def returnAddress(self, operation, number):
        return "RET_ADDRESS_" + operation + str(number)

class Codes(object):
    '''
    Holds lookup tables that map commands to Hack assembly code
    '''

    def __init__(self):

        self.addresser = Addresser()
        self.inputFileName = ""

        self.counts = {
            "eq": 0,
            "lt": 0,
            "gt": 0,
            "true": 0,
            "false": 0,
            "function":0
        }

        self.binaryOps = {
                "add":"D=M+D",
                "sub": "D=M-D",
                "and": "D=M&D",
                "or": "D=M|D"
        }

        self.unaryOps = {
            "not":"D=!D",
            "neg":"D=-D"
         }

        self.inputFileName = ""

        self.registerLocations = {
            "temp":5,
            "static":16,
            "pointer":3
        }

        self.segments = {
            "argument":"ARG",
            "local":"LCL",
            "that":"THAT",
            "this":"THIS"
        }

        self.specialOps = {
            "eq":"D;JEQ",
            "gt":"D;JGT",
            "lt":"D;JLT"
        }

        self.spOperators = {
            "increment":"M=M+1",
            "decrement":"M=M-1"
        }

    def arithmetic(self, operation):

        if operation in self.specialOps:

            operationCode = self.specialOps[operation]
            self.counts[operation] += 1
            returnAddress = self.addresser.returnAddress(operation, self.counts[operation])

            return \
            "@SP" + NEWLINE + \
            "M=M-1" + NEWLINE + \
            "A=M" + NEWLINE + \
            "D=M" + NEWLINE + \
            "@SP" + NEWLINE + \
            "M=M-1" + NEWLINE + \
            "A=M" + NEWLINE + \
            "D=M-D" + NEWLINE + \
            self.writeTrueAddress(returnAddress) + NEWLINE + \
            operationCode + NEWLINE + \
            self.writeFalseAddress(returnAddress) + NEWLINE + \
            "0;JMP" + NEWLINE + \
            self.writeTrueLabelAndLogic(returnAddress) + NEWLINE + \
            self.writeFalseLabelAndLogic(returnAddress) + NEWLINE + \
            "(" + returnAddress + ")" + NEWLINE + \
            "@SP" + NEWLINE + \
            "M=M+1" + NEWLINE

        if operation in self.binaryOps:

            operationCode = self.binaryOps[operation]
            return \
            "@SP" + NEWLINE + \
            "M=M-1" + NEWLINE + \
            "A=M" + NEWLINE + \
            "D=M" + NEWLINE + \
            "@SP" + NEWLINE + \
            "M=M-1" + NEWLINE + \
            "A=M" + NEWLINE + \
            operationCode + NEWLINE + \
            "@SP" + NEWLINE + \
            "A=M" + NEWLINE + \
            "M=D" + NEWLINE + \
            "@SP" + NEWLINE + \
            "M=M+1" + NEWLINE

        if operation in self.unaryOps:

            operationCode = self.unaryOps[operation]
            return \
            "@SP" + NEWLINE + \
            "M=M-1" + NEWLINE + \
            "A=M" + NEWLINE + \
            "D=M" + NEWLINE + \
            operationCode + NEWLINE + \
            "@SP" + NEWLINE + \
            "A=M" + NEWLINE + \
            "M=D" + NEWLINE + \
            "@SP" + NEWLINE + \
            "M=M+1" + NEWLINE

    def setSPTo(self, flag):

        if flag:
            return "@SP" + NEWLINE + \
                   "A=M" + NEWLINE + \
                   "M=-1"
        else:
            return "@SP" + NEWLINE + \
                   "A=M" + NEWLINE + \
                   "M=0"

    def getRegisterLocation(self, index, register):

        location = self.registerLocations[register]
        return location + int(index)

    def pop(self, segment, index):

        if segment == "temp" or segment == "pointer":
            segment = str(self.getRegisterLocation(index, segment))
            return \
            "@SP" + NEWLINE + \
            "M=M-1" + NEWLINE + \
            "A=M" + NEWLINE + \
            "D=M" + NEWLINE + \
            "@" + segment + NEWLINE + \
            "M=D" + NEWLINE

        elif segment == "static":
            segment = str(self.getRegisterLocation(index, segment))
            return \
            "@SP" + NEWLINE + \
            "M=M-1" + NEWLINE + \
            "A=M" + NEWLINE + \
            "D=M" + NEWLINE + \
            "@" + self.inputFileName + "." + segment + NEWLINE + \
            "M=D" + NEWLINE

        # If ARG, LCL, THIS, THAT -- first, use the index and segment to find Address Value and store it in temp.  next, get value from stack.
        # finally, store value from stack as value in the location of the Address Value
        else:
            segment = self.segments[segment]
            return \
            "@SP" + NEWLINE + \
            "M=M-1" + NEWLINE + \
            "@" + index + NEWLINE + \
            "D=A" + NEWLINE + \
            "@" + segment + NEWLINE + \
            "D=D+M" + NEWLINE + \
            "@R13" + NEWLINE + \
            "M=D" + NEWLINE + \
            "@SP" + NEWLINE + \
            "A=M" + NEWLINE + \
            "D=M" + NEWLINE + \
            "@R13" + NEWLINE + \
            "A=M" + NEWLINE + \
            "M=D" + NEWLINE

    def push(self, segment, index):

        if segment == "temp":
            segment = str(self.getRegisterLocation(index, segment))
            return \
            "@" + segment + NEWLINE + \
            "D=M" + NEWLINE + \
            "@SP" + NEWLINE + \
            "A=M" + NEWLINE + \
            "M=D" + NEWLINE + \
            "@SP" + NEWLINE + \
            "M=M+1" + NEWLINE

        elif segment == "constant":
            return "@" + index + NEWLINE + \
            "D=A" + NEWLINE + \
            "@SP" + NEWLINE + \
            "A=M" + NEWLINE + \
            "M=D" + NEWLINE + \
            "@SP" + NEWLINE + \
            "M=M+1" + NEWLINE

        elif segment == "pointer":
            segment = str(self.getRegisterLocation(index, segment))
            return \
            "@" + segment + NEWLINE + \
            "D=M" + NEWLINE + \
            "@SP" + NEWLINE + \
            "A=M" + NEWLINE + \
            "M=D" + NEWLINE + \
            "@SP" + NEWLINE + \
            "M=M+1" + NEWLINE

        elif segment == "static":
            segment = str(self.getRegisterLocation(index, segment))
            return \
            "@" + self.inputFileName + "." + segment + NEWLINE + \
            "D=M" + NEWLINE + \
            "@SP" + NEWLINE + \
            "A=M" + NEWLINE + \
            "M=D" + NEWLINE + \
            "@SP" + NEWLINE + \
            "M=M+1" + NEWLINE

        # If ARG, LCL, THIS, THAT
        else:
            segment = self.segments[segment]
            return \
            "@" + index + NEWLINE + \
            "D=A" + NEWLINE + \
            "@" + segment + NEWLINE + \
            "D=D+M" + NEWLINE + \
            "A=D" + NEWLINE + \
            "D=M" + NEWLINE + \
            "@SP" + NEWLINE + \
            "A=M" + NEWLINE + \
            "M=D" + NEWLINE + \
            "@SP" + NEWLINE + \
            "M=M+1" + NEWLINE

    def writeFalseAddress(self, returnAddress):
        self.counts["false"] += 1
        return "@" + "false" + str(self.counts["false"])

    def writeTrueAddress(self, returnAddress):
        self.counts["true"] += 1
        return "@" + "true" + str(self.counts["true"])

    def writeFalseLabelAndLogic(self, returnAddress):
        return \
        "(false" + str(self.counts["false"]) + ")" + NEWLINE + \
        self.writeFalseLogic(returnAddress)

    def writeFalseLogic(self, returnAddress):
        return \
        self.setSPTo(False) + NEWLINE + \
        "@" + returnAddress + NEWLINE + \
        "0;JMP"

    def writeTrueLabelAndLogic(self, returnAddress):
        return \
        "(true" + str(self.counts["true"]) + ")" + NEWLINE + \
        self.writeTrueLogic(returnAddress)

    def writeTrueLogic(self, returnAddress):
        return \
            self.setSPTo(True) + NEWLINE + \
            "@" + returnAddress + NEWLINE + \
            "0;JMP"