# Allowed libraries
import argparse

# Implemented libraries with classes
from lib.XMLParse import XMLParse
from lib.Instruction import *


class Interpret:
    def __init__(self):
        self.__gframe = Frame()
        self.__tframe = None
        self.__frames = Stack()

        self.__datastack = Stack()

        self.__parse_args()
        self.__interpret_start()

    def __parse_args(self):
        aparser = argparse.ArgumentParser()
        aparser.add_argument("--source", nargs=1, help="Missing parameter with source file")
        aparser.add_argument("--input", nargs=1, help="Missing parameter with input file")

        args = vars(aparser.parse_args())

        if args['input'] is None and args['source'] is None:
            RC(RC.BAD_ARGUMENT)
        else:
            if args['input'] is None:
                self.__inputPath = None
            else:
                self.__inputPath = args['input'][0]
                self.__inputFile = open(self.__inputPath, 'r')
                self.__inputLines = self.__inputFile.readlines()
                self.__inputLines = [line.strip() for line in self.__inputLines]
                self.__currentInputLine = 0

            if args['source'] is None:
                self.__sourcePath = input()
            else:
                self.__sourcePath = args['source'][0]

    def __tframe_exists(self) -> bool:
        return self.__tframe is not None

    def __frames_not_empty(self) -> bool:
        return self.__frames.size() > 0

    def __get_frame(self, f: str) -> Frame | None:
        if f == 'GF':
            return self.__gframe
        elif f == 'LF':
            if self.__frames_not_empty():
                return self.__frames.top()
            else:
                RC(RC.UNDEFINED_FRAME)
        elif f == 'TF':
            if self.__tframe_exists():
                return self.__tframe
            else:
                RC(RC.UNDEFINED_FRAME)
        else:
            return None

    def __jump_to(self, label: str):
        if label in self.__instructions.labels:
            self.__instructions.pos = self.__instructions.labels[label]
        else:
            RC(RC.SEMANTIC)

    def __update_symbol(self, arg: Symbol) -> Symbol:
        if isinstance(arg, Variable):
            arg = self.__get_variable(arg)

        return arg

    def __get_variable(self, arg: Variable) -> Variable:
        frame = self.__get_frame(arg.frame)
        return frame.get_var(arg.id)

    def __set_variable(self, v: Variable):
        frame = self.__get_frame(v.frame)
        frame.update_var(v.type, v.value, v.id)

    def __interpret_start(self):
        # Get XML representation
        xml = XMLParse(self.__sourcePath)

        # Get list of all instructions
        self.__instructions = xml.get_instructions()
        self.__instructions.transform_list()

        while True:
            instruction = self.__instructions.get_next_instruction()

            if instruction is None:
                break

            if type(instruction) is CREATEFRAME:
                self.__tframe = None
                self.__tframe = Frame()

            elif type(instruction) is PUSHFRAME:
                if self.__tframe_exists():
                    self.__frames.push(self.__tframe)
                    self.__tframe = None
                else:
                    RC(RC.UNDEFINED_FRAME)

            elif type(instruction) is POPFRAME:
                if self.__frames_not_empty():
                    self.__tframe = self.__frames.pop()
                else:
                    RC(RC.UNDEFINED_FRAME)

            elif type(instruction) is RETURN:
                self.__instructions.return_pos()

            elif type(instruction) is BREAK:
                # Displays interpret state:
                # 1) Global frame content
                # 2) Code position
                sys.stderr.write("Global frame content:\n")
                self.__gframe.print()
                sys.stderr.write("Position in code: {}\n".format(self.__instructions.pos))

            elif type(instruction) is DEFVAR:
                var = instruction.args[0]
                frame = self.__get_frame(var.frame)
                frame.define_var(var)

            elif type(instruction) is POPS:
                if self.__datastack.is_empty():
                    RC(RC.MISSING_VALUE)
                else:
                    var = self.__get_variable(instruction.args[0])
                    symb = self.__datastack.pop()
                    var.value = symb.value
                    var.type = symb.type
                    self.__set_variable(var)

            elif type(instruction) is PUSHS:
                symb = self.__update_symbol(instruction.args[0])
                obj = Const(symb.type, symb.value)
                self.__datastack.push(obj)

            elif type(instruction) is WRITE:
                symb = self.__update_symbol(instruction.args[0])
                if symb.type == 'nil':
                    symb.value = ''
                print(symb.value, end='')

            elif type(instruction) is EXIT:
                symb = self.__update_symbol(instruction.args[0])
                if symb.type != 'int':
                    RC(RC.OPERAND_TYPE)
                elif int(symb.value) < 0 or int(symb.value) > 49:
                    RC(RC.OPERAND_VALUE)

                RC(int(symb.value))

            elif type(instruction) is DPRINT:
                symb = self.__update_symbol(instruction.args[0])
                sys.stderr.write(str(symb.value))

            elif type(instruction) is CALL:
                self.__instructions.store_pos()
                label = instruction.args[0]
                self.__jump_to(label.id)

            elif type(instruction) is LABEL:
                pass

            elif type(instruction) is JUMP:
                label = instruction.args[0]
                self.__jump_to(label.id)

            elif type(instruction) in [INT2CHAR, STRLEN, TYPE, MOVE, NOT]:
                var = self.__get_variable(instruction.args[0])
                symb = self.__update_symbol(instruction.args[1])
                var = instruction.exec(var, symb)
                self.__set_variable(var)

            elif type(instruction) is READ:
                var = self.__get_variable(instruction.args[0])
                reqType = instruction.args[1].value

                if self.__inputPath is not None:
                    if len(self.__inputLines) == 0:
                        result = ''
                    else:
                        result = self.__inputLines[self.__currentInputLine]
                        self.__currentInputLine += 1
                else:
                    result = input()
                # result is a line read
                var = instruction.exec(result, reqType, var)
                self.__set_variable(var)

            elif type(instruction) in [CONCAT, GETCHAR, SETCHAR, ADD, SUB, MUL, IDIV,
                                       STRI2INT, LT, GT, EQ, AND, OR]:
                var = self.__get_variable(instruction.args[0])
                symb = self.__update_symbol(instruction.args[1])
                symb2 = self.__update_symbol(instruction.args[2])
                var = instruction.exec(var, symb, symb2)
                self.__set_variable(var)

            elif type(instruction) in [JUMPIFEQ, JUMPIFNEQ]:
                label = instruction.args[0].id
                symb = self.__update_symbol(instruction.args[1])
                symb2 = self.__update_symbol(instruction.args[2])
                if instruction.exec(symb, symb2):
                    self.__jump_to(label)


interpret = Interpret()
