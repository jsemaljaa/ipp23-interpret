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

        # self.__instructions here is an Object with type InstructionsList
        """
        END BLOCK: INTERPRET BODY
        """

    def __interpret_start(self):


interpret = Interpret()
