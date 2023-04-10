import xml.etree.ElementTree as et # !!!
from lib.Instruction import *
from lib.ReturnCodes import ReturnCodes as RC
from lib.InstructionsList import InstructionsList

class XMLParse:

    def __init__(self, path):
        self.__tree = None
        self.__root = None
        self.__path = path
        self.__instructions = InstructionsList()

        self.__check_tree()
        self.__collect_instructions()
        self.__print_instructions_list()

    def __check_tree(self):
        try:
            self.__tree = et.parse(self.__path)
            self.__check_root()
        except (FileNotFoundError, Exception):
            RC().exit_e(RC.BAD_XML_TREE)

    def __check_root(self):
        try:
            self.__root = self.__tree.getroot()
            if (self.__root.tag != 'program') or ('language' not in self.__root.attrib):
                RC().exit_e(RC.NOT_WF_XML)
            for attr in self.__root.attrib:
                if attr not in ['language', 'name', 'description']:
                    RC().exit_e(RC.BAD_XML_TREE)
            if self.__root.attrib['language'].upper() != 'IPPCODE23':
                RC().exit_e(RC.NOT_WF_XML)
        except Exception:
            RC().exit_e(RC.NOT_WF_XML)

    def __collect_instructions(self):
        for e in self.__root:
            givenInst = e.attrib['opcode'].upper()
            givenOrder = int(e.attrib['order'])
            if givenInst in knownInstructions:
                inst = knownInstructions[givenInst](givenOrder)
            else:
                RC().exit_e(RC.BAD_XML_TREE)

            for sub in e:
                inst.add_argument(sub.attrib['type'], sub.text)

            self.__instructions.append(inst)
            # inst.print()

    def __print_instructions_list(self):
        for i in self.__instructions.get_list():
            i.print()

    def get_instructions(self):
        return self.__instructions
