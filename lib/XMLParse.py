import xml.etree.ElementTree as et # !!!
from lib.Instruction import *
from lib.ReturnCodes import ReturnCodes as RC
from lib.InstructionsList import InstructionsList


class XMLParse:
    def __init__(self, path):
        self.__path = path
        self.__instructions = InstructionsList()
        self.__knownOrders = []
        self.__args = {}

        self.__start()

    @property
    def instructions(self):
        return self.__instructions

    def __start(self):
        try:
            self.__tree = et.parse(self.__path)
        except (FileNotFoundError, Exception):
            RC(RC.NOT_WF_XML)

        self.__check_root()
        self.__collect_instructions()

    def __check_root(self):
        self.__root = self.__tree.getroot()
        for attr in self.__root.attrib:
            if attr not in ['language', 'name', 'description']:
                RC(RC.BAD_XML_TREE)

        if (self.__root.tag != 'program') or ('language' not in self.__root.attrib) or self.__root.attrib['language'].upper() != 'IPPCODE23':
            RC(RC.BAD_XML_TREE)

    def __collect_instructions(self):
        for e in self.__root:
            self.__inst = self.__process_element(e)

            for sub in e:
                self.__process_subelement(sub)

            d = dict(sorted(self.__args.items()))
            if 1 not in d and len(d) != 0:
                RC(RC.BAD_XML_TREE)

            self.__inst.set_args(list(d.values()))
            self.__instructions.append(self.__inst)
            self.__args = {}

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

    def __process_subelement(self, sub):
        if not sub.tag.startswith('arg') or sub.tag[3] not in ['1', '2', '3']:
            RC(RC.BAD_XML_TREE)

        self.__process_arg(sub)

    def __process_arg(self, sub):
        type = sub.attrib['type']
        value = sub.text
        if type == 'var':
            frame, id = value.split("@")
            arg = Variable(id=id, type=None, value=None, frame=frame)
        elif type == 'label':
            arg = Label(id=value)
        elif type == 'int':
            try:
                arg = Const(type=type, value=int(value))
            except ValueError:
                RC(RC.BAD_XML_TREE)
        elif type == 'bool':
            if value == 'true':
                arg = Const(type=type, value='true')
            else:
                arg = Const(type=type, value='false')
        elif type == 'string':
            if value is None:
                value = ''
            arg = Const(type=type, value=str(value))
        elif type == 'nil':
            if value != 'nil':
                RC(RC.BAD_XML_TREE)
            else:
                arg = Const(type=type, value=value)
        elif type == 'type':
            arg = Type(value=value)
        else:
            RC(RC.BAD_XML_TREE)

        self.__args[int(sub.tag[3])] = arg
