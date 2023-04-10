import sys

# https://towardsdatascience.com/should-we-use-custom-exceptions-in-python-b4b4bca474ac
# https://www.programiz.com/python-programming/user-defined-exception

# class BadArgumentException(Exception):
#     """
#     Exception raised for cases with wrong or missing arguments
#     """
#
# class BadInputException(Exception):
#     pass
#
# class BadOutputException(Exception):
#     pass
#
# class NotWellFormattedXMLException(Exception):
#     pass
#
# class BadXMLTreeException(Exception):
#     pass
#
# class BadSemanticException(Exception):
#     pass
#
# class BadOperandTypeException(Exception):
#     pass
#
# class UndefinedVariableException(Exception):
#     pass
#
# class UndefinedFrameException(Exception):
#     pass
#
# class MissingValueException(Exception):
#     pass
#
# class BadOperandValueException(Exception):
#     pass
#
# class BadStringException(Exception):
#     pass


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
    SUCCESS = 0

    def __init__(self):
        pass

    def exit_e(self, code):
        if code != self.SUCCESS:
            sys.stderr.write("Error! ")
        else:
            exit(code)

        match code:
            case self.BAD_ARGUMENT:
                sys.stderr.write("Missing script parameter or forbidden parameter combination found")
            case self.BAD_INPUT_FILE:
                sys.stderr.write("Failed to open an input file")
            case self.BAD_OUTPUT_FILE:
                sys.stderr.write("Failed to open an output file")
            case self.NOT_WF_XML:
                sys.stderr.write("Given XML file is not well-formed")
            case self.BAD_XML_TREE:
                sys.stderr.write("Given XML file has unexpected XML structure")
            case self.SEMANTIC:
                sys.stderr.write("Semantic analysis failed")
            case self.OPERAND_TYPE:
                sys.stderr.write("Bad operands types")
            case self.UNDEFINED_VARIABLE:
                sys.stderr.write("Trying to access a non-existent variable")
            case self.UNDEFINED_FRAME:
                sys.stderr.write("Trying to access a non-existent frame")
            case self.MISSING_VALUE:
                sys.stderr.write("Missing value (either in variable, data stack or call stack)")
            case self.OPERAND_VALUE:
                sys.stderr.write("Wrong operand value")
            case self.BAD_STRING:
                sys.stderr.write("Wrong string operation")

        exit(code)
