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
        self.__knownOrders = []

        self.__check_tree()
        self.__collect_instructions()
        # self.__print_instructions_list()

    def __order_exists(self, order: int) -> True | False:
        return order in self.__knownOrders

    def __check_tree(self):
        try:
            self.__tree = et.parse(self.__path)
            self.__check_root()
        except (FileNotFoundError, Exception):
            RC().exit_e(RC.NOT_WF_XML)

    def __check_root(self):
        try:
            self.__root = self.__tree.getroot()
            if (self.__root.tag != 'program') or ('language' not in self.__root.attrib):
                RC().exit_e(RC.BAD_XML_TREE)
            for attr in self.__root.attrib:
                if attr not in ['language', 'name', 'description']:
                    RC().exit_e(RC.BAD_XML_TREE)
            if self.__root.attrib['language'].upper() != 'IPPCODE23':
                RC().exit_e(RC.BAD_XML_TREE)
        except Exception:
            RC().exit_e(RC.BAD_XML_TREE)

    def __collect_instructions(self):
        for e in self.__root:
            if e.tag != 'instruction' or 'order' not in e.attrib or 'opcode' not in e.attrib:
                RC().exit_e(RC.BAD_XML_TREE)
            instruction = e.attrib['opcode'].upper()
            order = int(e.attrib['order'])
            if self.__order_exists(order):
                RC().exit_e(RC.BAD_XML_TREE)
            self.__knownOrders.append(order)
            if instruction in knownInstructions:
                inst = knownInstructions[instruction](order)
            else:
                RC().exit_e(RC.BAD_XML_TREE)

            for sub in e:
                if sub.tag == 'arg1':
                    inst.add_argument(1, sub.attrib['type'], sub.text)
                elif sub.tag == 'arg2':
                    inst.add_argument(2, sub.attrib['type'], sub.text)
                elif sub.tag == 'arg3':
                    inst.add_argument(1, sub.attrib['type'], sub.text)
                else:
                    RC().exit_e(RC.BAD_XML_TREE)

            inst.check_instruction_arguments()
            if type(inst) is LABEL:
                self.__instructions.save_label(inst.args[0], inst.order)

            self.__instructions.append(inst)
            # inst.print()

    def get_instructions(self) -> InstructionsList:
        return self.__instructions
