__author__ = 'mono'

COMMENT = "//"
SPACE = " "

class Parser(object):

    def __init__(self, commands):
        self.commands = Commands()

    def commandType(self, command):
        '''
        Returns the type of the current VM command. C_ARITHMETIC is returned for all the arithmetic commands
        :return: type of command the input is
        '''
        return self.commands.type(command)

    def isInstruction(self, line):
        # Don't parse comment lines or newlines
        if line:
            if COMMENT in line[0:2] or len(line) == 2:
                return False
            else:
                return True

    def parse(self, instruction):
        '''
        :param instruction: string
        :return: list of commands
        '''
        return instruction.split(SPACE)

class Commands(object):
    '''
    An object that holds lookup tables that map commands to their type.
    '''
    def __init__(self):
        self.arithmetic = ["add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"]
        self.functionCall = ["function", "call", "return"]
        self.memCommand = ["push", "pop"]
        self.programFlow = ["if-goto", "goto", "label"]

    def type(self, command):
        if command in self.arithmetic:
            return "arithmetic"
        if command in self.functionCall:
            return "function"
        if command in self.memCommand:
            return "memory"
        else:
            return "program"