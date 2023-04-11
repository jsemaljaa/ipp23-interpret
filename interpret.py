# Allowed libraries
import sys
import argparse
import os
import codecs
import re

# Implemented libraries with classes
from lib.ReturnCodes import ReturnCodes as RC
from lib.XMLParse import XMLParse
from lib.DataStructures import *
from lib.Instruction import *

aparser = argparse.ArgumentParser()
aparser.add_argument("--source", nargs=1, help="Missing parameter with source file")
aparser.add_argument("--input", nargs=1, help="Missing parameter with input file")

args = vars(aparser.parse_args())

if args['input'] is None and args['source'] is None:
    RC.exit_e(RC.BAD_ARGUMENT)
else:
    if args['input'] is None:
        fileInput = input()
    else:
        fileInput = args['input'][0]

    if args['source'] is None:
        sourcePath = input()
    else:
        sourcePath = args['source'][0]


class Interpret:
    def __init__(self):
        self.__gframe = Frame()
        self.__tframe = None
        self.__frames = Stack()

        self.__datastack = Stack()
        self.__labels = {}

        self.__get_instructions_list()
        self.__interpret_start()

    """
    START BLOCK: FRAMES OPERATIONS
    """

    def __create_frame(self):
        self.__tframe = Frame()

    def __delete_frame(self):
        self.__tframe = None

    def __tframe_exists(self):
        return self.__tframe is not None

    def __frames_not_empty(self):
        return self.__frames.size() > 0

    def __get_tframe(self):
        if self.__tframe_exists():
            return self.__tframe
        else:
            RC().exit_e(RC.UNDEFINED_FRAME)

    def __get_top_lframe(self):
        if self.__frames_not_empty():
            return self.__frames.top()
        else:
            RC().exit_e(RC.UNDEFINED_FRAME)

    def __push_frame(self):
        if self.__tframe_exists():
            self.__frames.push(self.__tframe)
            self.__tframe = None
        else:
            RC().exit_e(RC.UNDEFINED_FRAME)

    def __pop_frame(self):
        self.__tframe = self.__get_top_lframe()
        self.__frames.pop()

    def __get_frame(self, f: str) -> Frame | None:
        if f == 'GF':
            return self.__gframe
        elif f == 'LF':
            return self.__get_top_lframe()
        elif f == 'TF':
            return self.__get_tframe()
        else:
            return None

    @staticmethod
    def __update_variable(self, f: Frame, var: Variable):
        f.update_var(var)

    """
    END BLOCK: FRAMES OPERATIONS
    """

    """
    START BLOCK: OPCODE ARGUMENTS
    """

    def __label_exists(self, label) -> True | False:
        return label in self.__labels

    def __jump_to(self, label):
        if self.__label_exists(label):
            self.__instructions.pos = self.__labels[label]
        else:
            RC().exit_e(RC.SEMANTIC)

    @staticmethod
    def __check_instruction_arguments(arguments: list, required: list):
        if len(arguments) != len(required):
            RC().exit_e(RC.BAD_XML_TREE)
        i = 0
        for arg in arguments:
            if isinstance(arg, required[i]): # noqa
                i += 1
            else:
                RC().exit_e(RC.SEMANTIC)
    """
    END BLOCK: OPCODE ARGUMENTS
    """

    """
    START BLOCK: INTERPRET BODY
    """

    def __get_instructions_list(self):
        # Get XML representation
        XML = XMLParse(sourcePath)

        # Get list of all instructions
        self.__instructions = XML.get_instructions()

        # self.__instructions.print()

        # self.__instructions here is an Object with type InstructionsList
        """
        END BLOCK: INTERPRET BODY
        """

    def __interpret_start(self):

        while True:
            instruction = self.__instructions.get_next_instruction()

            # instruction.print()
            if instruction is None:
                break

            if type(instruction) is CREATEFRAME:
                self.__delete_frame()
                self.__create_frame()

            elif type(instruction) is PUSHFRAME:
                self.__push_frame()

            elif type(instruction) is POPFRAME:
                self.__pop_frame()

            elif type(instruction) is RETURN:
                self.__instructions.return_pos()

            elif type(instruction) is BREAK:
                pass

            elif type(instruction) is DEFVAR:
                var = instruction.args[0]
                if isinstance(var, Variable):
                    # var.id, var.frame
                    frame = self.__get_frame(var.frame)
                    if frame.contains(var.id):
                        RC().exit_e(RC.SEMANTIC)
                    else:
                        frame.define_var(var)

            elif type(instruction) is POPS:
                var = instruction.args[0]
                frame = self.__get_frame(var.frame)
                if self.__datastack.is_empty():
                    RC().exit_e(RC.MISSING_VALUE)
                else:
                    symb = self.__datastack.pop()
                    frame.update_var(symb.type, symb.value, var.id)

            elif type(instruction) is PUSHS:
                symb = instruction.args[0]
                self.__datastack.push(symb)

            elif type(instruction) is WRITE:
                symb = instruction.args[0]
                if isinstance(symb, Variable):
                    frame = self.__get_frame(symb.frame)
                    if not frame.contains(symb.id):
                        RC().exit_e(RC.UNDEFINED_VARIABLE)
                    var = frame.get_var(symb.id)
                    print(var.value, end='')
                else:
                    print(symb.value, end='')

            elif type(instruction) is EXIT:
                symb = instruction.args[0]
                if symb.type != 'int':
                    RC().exit_e(RC.OPERAND_TYPE)
                if int(symb.value) < 0 or int(symb.value) > 49:
                    RC().exit_e(RC.OPERAND_VALUE)
                else:
                    RC().exit_e(int(symb.value))

            elif type(instruction) is DPRINT:
                symb = instruction.args[0]
                if isinstance(symb, Variable):
                    frame = self.__get_frame(symb.frame)
                    if not frame.contains(symb.id):
                        RC().exit_e(RC.UNDEFINED_VARIABLE)
                    symb = frame.get_var(symb.id)
                    sys.stderr.write(str(symb.value))
                else:
                    sys.stderr.write(str(symb.value))

            elif type(instruction) is CALL:
                self.__instructions.store_pos()
                label = instruction.args[0]
                self.__jump_to(label)

            elif type(instruction) is LABEL:
                label = instruction.args[0]
                if label in self.__labels:
                    RC().exit_e(RC.SEMANTIC)
                else:
                    self.__labels[label] = self.__instructions.pos

            elif type(instruction) is JUMP:
                label = instruction.args[0]
                self.__jump_to(label)

            elif type(instruction) is INT2CHAR:
                var = instruction.args[0]
                symb = instruction.args[1]
                if symb.type != 'int':
                    RC().exit_e(RC.SEMANTIC)
                try:
                    var.value = chr(symb.value)
                    var.type = 'string'
                except:
                    RC().exit_e(RC.SEMANTIC)
                frame = self.__get_frame(var.frame)
                frame.update_var(var.type, var.value, var.id)

            elif type(instruction) is STRLEN:
                var = instruction.args[0]
                symb = instruction.args[1]
                if symb.type != 'string':
                    RC().exit_e(RC.SEMANTIC)
                var.value = len(symb.value)
                var.type = 'int'
                frame = self.__get_frame(var.frame)
                frame.update_var(var.type, var.value, var.id)

            elif type(instruction) is TYPE:
                var = instruction.args[0]
                symb = instruction.args[1]
                frame = self.__get_frame(var.frame)
                if not frame.contains(var.id):
                    RC().exit_e(RC.UNDEFINED_VARIABLE)
                if isinstance(symb, Variable):
                    frame = self.__get_frame(symb.frame)
                    if not frame.contains(symb.id):
                        var.value = ''
                        var.type = 'string'
                    else:
                        symb = frame.get_var(symb.id)
                        var.value = symb.type
                        var.type = 'string'
                        varFrame = self.__get_frame(var.frame)
                        varFrame.update_var(var.type, var.value, var.id)
                else:
                    frame = self.__get_frame(var.frame)
                    var.value = symb.type
                    var.type = 'string'
                    frame.update_var(var.type, var.value, var.id)

            elif type(instruction) is MOVE:
                var = instruction.args[0]
                symb = instruction.args[1]
                frame = self.__get_frame(var.frame)
                if not frame.contains(var.id):
                    RC().exit_e(RC.UNDEFINED_VARIABLE)
                if isinstance(symb, Const):
                    frame.update_var(symb.type, symb.value, var.id)
                elif isinstance(symb, Variable):
                    symbFrame = self.__get_frame(symb.frame)
                    if not symbFrame.contains(symb.id):
                        RC().exit_e(RC.UNDEFINED_VARIABLE)
                    else:
                        symb = symbFrame.get_var(symb.id)
                        frame.update_var(symb.type, symb.value, var.id)

            elif type(instruction) is READ:
                pass

            elif type(instruction) is NOT:
                var = instruction.args[0]
                symb = instruction.args[1]
                if symb.type != 'bool':
                    RC().exit_e(RC.SEMANTIC)
                else:
                    frame = self.__get_frame(var.frame)
                    if not frame.contains(var.id):
                        RC().exit_e(RC.SEMANTIC)
                    var.type = 'bool'
                    if symb.value:
                        var.value = False
                    else:
                        var.value = True
                    frame.update_var(var.type, var.value, var.id)

interpret = Interpret()
