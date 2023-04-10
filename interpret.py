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
from lib.Argument import Argument


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
        self.__XML = None
        self.__instructions = []
        self.__datastack = Stack()

        self.get_instructions_list()
        # self.parse_instructions()

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

    def get_frame(self, f: str) -> Frame | None:
        if f == 'GF':
            return self.__gframe
        elif f == 'LF':
            return self.__get_top_lframe()
        elif f == 'TF':
            return self.__get_tframe()
        else:
            return None
    """
    END BLOCK: FRAMES OPERATIONS
    """

    """
    START BLOCK: OPCODE ARGUMENTS
    """

    @staticmethod
    def arg_is_var(a: Argument):
        return a.type == 'var'

    @staticmethod
    def transform_argument(a: Argument):
        return a.value.split("@")

    def get_parsed_variable(self, a: Argument) -> Variable:
        # USE PARSE VARIABLE IN CASES WHERE THIS VARIABLE WAS CERTAINLY DEFINED
        frame, id = self.transform_argument(a)
        frame = self.get_frame(frame)
        if frame.contains(id):
            return frame.get_var(id)
        else:
            RC().exit_e(RC.UNDEFINED_VARIABLE)

    def parse_const(self, a: Argument) -> Const:
        return Const(a.type, a.value)

    def check_math_symbs(self, s1: Argument, s2: Argument):
        if self.arg_is_var(s1):
            symb1 = self.get_parsed_variable(s1)
        else:
            symb1 = self.parse_const(s1)

        if self.arg_is_var(s2):
            symb2 = self.get_parsed_variable(s2)
        else:
            symb2 = self.parse_const(s2)

        if symb1.type != 'int' or symb2.type != 'int':
            RC().exit_e(RC.SEMANTIC)

        return int(symb1.value), int(symb2.value)


    """
    END BLOCK: OPCODE ARGUMENTS
    """


    """
    START BLOCK: INTERPRET BODY
    """

    def get_instructions_list(self):
        # Get XML representation
        self.__XML = XMLParse(sourcePath)

        # Get list of all instructions
        self.__instructions = self.__XML.get_instructions()

    def parse_instructions(self):
        self.get_instructions_list()
        # Iterate through instructions
        for i in self.__instructions:
            if i.name.upper() == 'CREATEFRAME':
                self.__delete_frame()
                self.__create_frame()
            if i.name.upper() == 'PUSHFRAME':
                self.__push_frame()
            if i.name.upper() == 'POPFRAME':
                self.__pop_frame()
            if i.name.upper == 'BREAK':
                pass
            if i.name.upper() == 'MOVE':
                # MOVE <var> <symb>
                # Copy the value of <symb> to the <var>
                # Example: MOVE LF@par GF@var

                if self.arg_is_var(i.args[0]):
                    frame, id = self.transform_argument(i.args[0])
                    frame = self.get_frame(frame)
                    if frame.contains(id):
                        if self.arg_is_var(i.args[1]):
                            frame2, id2 = self.transform_argument(i.args[1])
                            frame2 = self.get_frame(frame2)
                            if frame2.contains(id2):
                                var2 = frame2.get_var(id2)
                                frame.update_var(id, var2.type, var2.value)
                            else:
                                RC().exit_e(RC.UNDEFINED_VARIABLE)
                        else:
                            frame.get_var(id).print()
                            const = self.parse_const(i.args[1])
                            frame.update_var(id, const.type, const.value)
                    else:
                        RC().exit_e(RC.UNDEFINED_VARIABLE)
            if i.name.upper() == 'DEFVAR':
                if self.arg_is_var(i.args[0]):
                    frame, id = self.transform_argument(i.args[0])
                    frame = self.get_frame(frame)
                    var = Variable(id, None, None)
                else:
                    RC().exit_e(RC.SEMANTIC)

                if frame.contains(var):
                    RC().exit_e(RC.SEMANTIC)
                else:
                    frame.define_var(var)
            # if i.name.upper() == 'CALL':
            # if i.name.upper() == 'RETURN':
            if i.name.upper() == 'PUSHS':
                if self.arg_is_var(i.args[0]):
                    symb = self.get_parsed_variable(i.args[0])
                else:
                    symb = self.parse_const(i.args[0])
                self.__datastack.push(symb)
            if i.name.upper() == 'POPS':
                if self.arg_is_var(i.args[0]):
                    frame, id = self.transform_argument(i.args[0])
                    frame = self.get_frame(frame)
                    if frame.contains(id):
                        val = self.__datastack.pop()
                        frame.update_var(id, val.type, val.value)
                    else:
                        RC().exit_e(RC.UNDEFINED_VARIABLE)
                else:
                    RC().exit_e(RC.SEMANTIC)
            if i.name.upper() == 'ADD':
                if self.arg_is_var(i.args[0]):
                    frame, id = self.transform_argument(i.args[0])
                    frame = self.get_frame(frame)
                    if frame.contains(id):
                        s1, s2 = self.check_math_symbs(i.args[1], i.args[2])
                        result = s1 + s2
                        var = frame.get_var(id)
                        var.print()

                        frame.update_var(id, 'int', result)

                        var = frame.get_var(id)
                        var.print()
                    else:
                        RC().exit_e(RC.UNDEFINED_VARIABLE)
                else:
                    RC().exit_e(RC.SEMANTIC)
            if i.name.upper() == 'SUB':
                if self.arg_is_var(i.args[0]):
                    frame, id = self.transform_argument(i.args[0])
                    frame = self.get_frame(frame)
                    if frame.contains(id):
                        s1, s2 = self.check_math_symbs(i.args[1], i.args[2])
                        result = s2 - s1
                        frame.update_var(id, 'int', result)
                    else:
                        RC().exit_e(RC.UNDEFINED_VARIABLE)
                else:
                    RC().exit_e(RC.SEMANTIC)
            if i.name.upper() == 'MUL':
                if self.arg_is_var(i.args[0]):
                    frame, id = self.transform_argument(i.args[0])
                    frame = self.get_frame(frame)
                    if frame.contains(id):
                        s1, s2 = self.check_math_symbs(i.args[1], i.args[2])
                        result = s1 * s2
                        frame.update_var(id, 'int', result)
                    else:
                        RC().exit_e(RC.UNDEFINED_VARIABLE)
                else:
                    RC().exit_e(RC.SEMANTIC)
            if i.name.upper() == 'IDIV':
                if self.arg_is_var(i.args[0]):
                    frame, id = self.transform_argument(i.args[0])
                    frame = self.get_frame(frame)
                    if frame.contains(id):
                        s1, s2 = self.check_math_symbs(i.args[1], i.args[2])
                        if s2 == 0:
                            RC().exit_e(RC.OPERAND_VALUE)
                        result = s2 // s1
                        frame.update_var(id, 'int', result)
                    else:
                        RC().exit_e(RC.UNDEFINED_VARIABLE)
                else:
                    RC().exit_e(RC.SEMANTIC)
        """
        END BLOCK: INTERPRET BODY
        """

interpret = Interpret()
