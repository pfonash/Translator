ARITHMETIC = "arithmetic"
NEWLINE = "\n"
STACK = "STACK"

class Codes(object):
    '''
    Holds lookup tables that map commands to Hack assembly code
    '''
    arithmetic = {
        "add":
            "@SP" + NEWLINE +
            "A=M" + NEWLINE +
            "D=M" + NEWLINE +
            "@SP" + NEWLINE +
            "M=M-1" + NEWLINE +
            "A=M" + NEWLINE +
            "D=M+D" + NEWLINE +
            "@SP" + NEWLINE +
            "M=M-1" + NEWLINE +
            "A=M" + NEWLINE +
            "M=D"
    }

