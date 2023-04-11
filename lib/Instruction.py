from lib.ReturnCodes import ReturnCodes as RC
from lib.DataStructures import *

class Instruction:
    def __init__(self, order: int) -> None:
        self.__order = order
        self.__args = []
        self.__check_order()
        self.__required = []

    @property
    def required(self):
        return self.__required

    @required.setter
    def required(self, req: list):
        self.__required = req

    @property
    def order(self):
        return self.__order

    @property
    def args(self):
        return self.__args

    def print(self):
        print("Instruction: " + str(type(self)) + " with order: " + str(self.__order))
        self.__print_args()

    def __print_args(self):
        i = 1
        for a in self.args:
            print("\t" + str(i) + ". type: " + str(type(a)))
            a.print()
            i += 1

    def add_argument(self, order: int, type, value):
        arg = None
        if type == 'var':
            frame, id = value.split("@")
            arg = Variable(id=id, type=None, value=None, frame=frame)
        elif type == 'label':
            arg = Label(id=value)
        elif type == 'int':
            arg = Const(type=type, value=int(value))
        elif type == 'bool':
            if value == 'true':
                arg = Const(type=type, value=True)
            else:
                arg = Const(type=type, value=False)
        elif type == 'string':
            if value is None:
                value = ''
            arg = Const(type=type, value=str(value))
        elif type == 'nil':
            if value != 'nil':
                RC().exit_e(RC.BAD_XML_TREE)
            else:
                arg = Const(type=type, value=value)
        elif type == 'type':
            arg = Type(value=value)
        else:
            RC().exit_e(RC.BAD_XML_TREE)

        # self.__args.append(arg)
        self.__args.insert(order - 1, arg)

    def __check_order(self):
        if not isinstance(self.order, int) or self.order < 1:
            RC().exit_e(RC.BAD_XML_TREE)

    def check_instruction_arguments(self):
        if len(self.args) != len(self.required):
            RC().exit_e(RC.BAD_XML_TREE)
        i = 0
        for arg in self.args:
            if isinstance(arg, self.required[i]): # noqa
                i += 1
            else:
                RC().exit_e(RC.SEMANTIC)


class CREATEFRAME(Instruction):
    def __init__(self, order):
        super().__init__(order)
        self.required = []


class PUSHFRAME(Instruction):
    def __init__(self, order):
        super().__init__(order)
        self.required = []


class POPFRAME(Instruction):
    def __init__(self, order):
        super().__init__(order)
        self.required = []


class RETURN(Instruction):
    def __init__(self, order):
        super().__init__(order)
        self.required = []


class BREAK(Instruction):
    def __init__(self, order):
        super().__init__(order)
        self.required = []


class DEFVAR(Instruction):
    def __init__(self, order):
        super().__init__(order)
        self.required = [Variable]

class POPS(Instruction):
    def __init__(self, order):
        super().__init__(order)
        self.required = [Variable]


class PUSHS(Instruction):
    def __init__(self, order):
        super().__init__(order)
        self.required = [Symbol]


class WRITE(Instruction):
    def __init__(self, order):
        super().__init__(order)
        self.required = [Symbol]


class EXIT(Instruction):
    def __init__(self, order):
        super().__init__(order)
        self.required = [Symbol]


class DPRINT(Instruction):
    def __init__(self, order):
        super().__init__(order)
        self.required = [Symbol]


class CALL(Instruction):
    def __init__(self, order):
        super().__init__(order)
        self.required = [Label]


class LABEL(Instruction):
    def __init__(self, order):
        super().__init__(order)
        self.required = [Label]


class JUMP(Instruction):
    def __init__(self, order):
        super().__init__(order)
        self.required = [Label]


class INT2CHAR(Instruction):
    def __init__(self, order):
        super().__init__(order)
        self.required = [Variable, Symbol]

class STRLEN(Instruction):
    def __init__(self, order):
        super().__init__(order)
        self.required = [Variable, Symbol]


class TYPE(Instruction):
    def __init__(self, order):
        super().__init__(order)
        self.required = [Variable, Symbol]


class MOVE(Instruction):
    def __init__(self, order):
        super().__init__(order)
        self.required = [Variable, Symbol]


class NOT(Instruction):
    def __init__(self, order):
        super().__init__(order)
        self.required = [Variable, Symbol]


class READ(Instruction):
    def __init__(self, order):
        super().__init__(order)
        self.required = [Variable, Type]


class CONCAT(Instruction):
    def __init__(self, order):
        super().__init__(order)
        self.required = [Variable, Symbol, Symbol]


class GETCHAR(Instruction):
    def __init__(self, order):
        super().__init__(order)
        self.required = [Variable, Symbol, Symbol]


class SETCHAR(Instruction):
    def __init__(self, order):
        super().__init__(order)
        self.required = [Variable, Symbol, Symbol]


class STRI2INT(Instruction):
    def __init__(self, order):
        super().__init__(order)
        self.required = [Variable, Symbol, Symbol]


class ADD(Instruction):
    def __init__(self, order):
        super().__init__(order)
        self.required = [Variable, Symbol, Symbol]


class SUB(Instruction):
    def __init__(self, order):
        super().__init__(order)
        self.required = [Variable, Symbol, Symbol]


class MUL(Instruction):
    def __init__(self, order):
        super().__init__(order)
        self.required = [Variable, Symbol, Symbol]


class IDIV(Instruction):
    def __init__(self, order):
        super().__init__(order)
        self.required = [Variable, Symbol, Symbol]


class LT(Instruction):
    def __init__(self, order):
        super().__init__(order)
        self.required = [Variable, Symbol, Symbol]


class GT(Instruction):
    def __init__(self, order):
        super().__init__(order)
        self.required = [Variable, Symbol, Symbol]


class EQ(Instruction):
    def __init__(self, order):
        super().__init__(order)
        self.required = [Variable, Symbol, Symbol]


class AND(Instruction):
    def __init__(self, order):
        super().__init__(order)
        self.required = [Variable, Symbol, Symbol]


class OR(Instruction):
    def __init__(self, order):
        super().__init__(order)
        self.required = [Variable, Symbol, Symbol]


class JUMPIFEQ(Instruction):
    def __init__(self, order):
        super().__init__(order)
        self.required = [Label, Symbol, Symbol]

class JUMPIFNEQ(Instruction):
    def __init__(self, order):
        super().__init__(order)
        self.required = [Label, Symbol, Symbol]


knownInstructions = {
    "CREATEFRAME": CREATEFRAME,
    "PUSHFRAME": PUSHFRAME,
    "POPFRAME": POPFRAME,
    "RETURN": RETURN,
    "BREAK": BREAK,
    "DEFVAR": DEFVAR,
    "POPS": POPS,
    "PUSHS": PUSHS,
    "WRITE": WRITE,
    "EXIT": EXIT,
    "DPRINT": DPRINT,
    "CALL": CALL,
    "LABEL": LABEL,
    "JUMP": JUMP,
    "INT2CHAR": INT2CHAR,
    "STRLEN": STRLEN,
    "TYPE": TYPE,
    "MOVE": MOVE,
    "NOT": NOT,
    "READ": READ,
    "CONCAT": CONCAT,
    "GETCHAR": GETCHAR,
    "SETCHAR": SETCHAR,
    "STRI2INT": STRI2INT,
    "ADD": ADD,
    "SUB": SUB,
    "MUL": MUL,
    "IDIV": IDIV,
    "LT": LT,
    "GT": GT,
    "EQ": EQ,
    "AND": AND,
    "OR": OR,
    "JUMPIFEQ": JUMPIFEQ,
    "JUMPIFNEQ": JUMPIFNEQ
}