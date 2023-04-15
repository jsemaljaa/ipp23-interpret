import sys


class ReturnCodes:

    BAD_ARGUMENT = 10
    BAD_INPUT_FILE = 11
    BAD_OUTPUT_FILE = 12

    # WF stands for Well-formed
    NOT_WF_XML = 31
    BAD_XML_TREE = 32

    SEMANTIC = 52
    OPERAND_TYPE = 53
    UNDEFINED_VARIABLE = 54
    UNDEFINED_FRAME = 55
    MISSING_VALUE = 56
    OPERAND_VALUE = 57
    BAD_STRING = 58

    knownCodes = [
        BAD_ARGUMENT,
        BAD_INPUT_FILE,
        BAD_OUTPUT_FILE,
        NOT_WF_XML,
        BAD_XML_TREE,
        SEMANTIC,
        OPERAND_TYPE,
        UNDEFINED_VARIABLE,
        UNDEFINED_FRAME,
        MISSING_VALUE,
        OPERAND_VALUE,
        BAD_STRING
    ]

    def __init__(self, code):
        if code not in self.knownCodes:
            exit(code)

        sys.stderr.write("Error {}! ".format(code))
        match code:
            case self.BAD_ARGUMENT:
                sys.stderr.write("Missing script parameter or forbidden parameter combination found\n")
            case self.BAD_INPUT_FILE:
                sys.stderr.write("Failed to open an input file\n")
            case self.BAD_OUTPUT_FILE:
                sys.stderr.write("Failed to open an output file\n")
            case self.NOT_WF_XML:
                sys.stderr.write("Given XML file is not well-formed\n")
            case self.BAD_XML_TREE:
                sys.stderr.write("Given XML file has unexpected XML structure\n")
            case self.SEMANTIC:
                sys.stderr.write("Semantic\n")
            case self.OPERAND_TYPE:
                sys.stderr.write("Bad operands types\n")
            case self.UNDEFINED_VARIABLE:
                sys.stderr.write("Trying to access a non-existent variable\n")
            case self.UNDEFINED_FRAME:
                sys.stderr.write("Trying to access a non-existent frame\n")
            case self.MISSING_VALUE:
                sys.stderr.write("Missing value (either in variable, data stack or call stack)\n")
            case self.OPERAND_VALUE:
                sys.stderr.write("Wrong operand value\n")
            case self.BAD_STRING:
                sys.stderr.write("Wrong string operation\n")

        exit(code)