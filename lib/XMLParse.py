import xml.etree.ElementTree as et # !!!
from lib.Instruction import *
from lib.ReturnCodes import ReturnCodes as RC
from lib.InstructionsList import InstructionsList


class XMLParse:

    def __init__(self, path):
        self.__tree = None
        self.__root = None
        self.__path = path

        self.__inst = None
        self.__instructions = InstructionsList()
        self.__knownOrders = []
        self.__args = {}

        self.__check_tree()
        self.__collect_instructions()

    def __save_order(self, order) -> int:
        try:
            order = int(order)
        except ValueError:
            RC(RC.BAD_XML_TREE)

        if order in self.__knownOrders:
            RC(RC.BAD_XML_TREE)
        else:
            self.__knownOrders.append(order)
            return order

    def __check_tree(self):
        try:
            self.__tree = et.parse(self.__path)
        except (FileNotFoundError, Exception):
            RC(RC.NOT_WF_XML)

        self.__check_root()

    def __check_root(self):
        self.__root = self.__tree.getroot()
        for attr in self.__root.attrib:
            if attr not in ['language', 'name', 'description']:
                RC(RC.BAD_XML_TREE)

        if (self.__root.tag != 'program') or ('language' not in self.__root.attrib) or self.__root.attrib['language'].upper() != 'IPPCODE23':
            RC(RC.BAD_XML_TREE)

    def __process_element(self, elem) -> Instruction:
        if elem.tag != 'instruction' or 'order' not in elem.attrib or 'opcode' not in elem.attrib:
            RC(RC.BAD_XML_TREE)

        instruction = elem.attrib['opcode'].upper()

        order = self.__save_order(elem.attrib['order'])

        if instruction in knownInstructions:
            self.__inst = knownInstructions[instruction](order)
        else:
            RC(RC.BAD_XML_TREE)

        return self.__inst

    def __process_subelement(self, sub, inst):
        if not sub.tag.startswith('arg') or sub.tag[3] not in ['1', '2', '3']:
            RC(RC.BAD_XML_TREE)

        self.__args[int(sub.tag[3])] = inst.process_arg(sub.attrib['type'], sub.text)

    def __collect_instructions(self):
        for e in self.__root:
            self.__inst = self.__process_element(e)

            for sub in e:
                self.__process_subelement(sub, self.__inst)

            d = dict(sorted(self.__args.items()))
            if 1 not in d and len(d) != 0:
                RC(RC.BAD_XML_TREE)

            self.__inst.set_args(list(d.values()))

            self.__inst.check_instruction_arguments()

            self.__instructions.append(self.__inst)
            self.__args = {}
            # inst.print()

    def get_instructions(self) -> InstructionsList:
        return self.__instructions
