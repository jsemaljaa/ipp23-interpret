# Allowed libraries
import sys
import argparse
import os
import codecs
import re

# Implemented libraries with classes
from lib.ReturnCodes import ReturnCodes as RC
from lib.XMLParse import XMLParse
from lib.Stack import Stack
from lib.Frame import Frame
from lib.DataTypes import *
from lib.Instruction import *


aparser = argparse.ArgumentParser()
aparser.add_argument("--source", nargs=1, help="Missing parameter with source file")
aparser.add_argument("--input", nargs=1, help="Missing parameter with input file")

args = vars(aparser.parse_args())

if args['input'] is None and args['source'] is None:
    RC.exit_e(RC.BAD_ARGUMENT)
else:
    if args['input'] is None:
        fileInput = ""
        # print("*** WAITING FOR INPUT ***")
        # while True:
        #     fileInput = sys.stdin.read()
        #     if "\n" == fileInput:
        #         break
    else:
        fileInput = args['input']

    if args['source'] is None:
        sourcePath = ""
        # print("*** WAITING FOR SOURCE ***")
        # while True:
        #     sourcePath = sys.stdin.read()
        #     if "\n" == sourcePath:
        #         break
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

        # self.__instructions here is an Object with type InstructionsList
        """
        END BLOCK: INTERPRET BODY
        """

    def __interpret_start(self):
        while True:
            instruction = self.__instructions.get_next_instruction()

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
                print(symb.value, end='')
            elif type(instruction) is EXIT:
                pass
            elif type(instruction) is DPRINT:
                pass
            elif type(instruction) is CALL:
                pass
            elif type(instruction) is LABEL:
                label = instruction.args[0]
                if label in self.__labels:
                    RC().exit_e(RC.SEMANTIC)
                else:
                    self.__labels[label] = self.__instructions.pos
            elif type(instruction) is JUMP:
                pass


interpret = Interpret()
