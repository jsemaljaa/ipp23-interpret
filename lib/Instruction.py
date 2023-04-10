from lib.Argument import Argument
from lib.ReturnCodes import ReturnCodes as RC
from lib.Frame import Frame
from lib.DataTypes import *

class Instruction:
    def __init__(self, order: int) -> None:
        self.__order = order
        self.__args = []
        self.__check_order()

    @property
    def order(self):
        return self.__order

    @property
    def args(self):
        return self.__args

    def print(self):
        print("Instruction: " + str(type(self)) + " with order: " + str(self.__order))
        self.print_args()

    def print_args(self):
        i = 1
        for a in self.args:
            print("\t" + str(i) + ". type: " + str(type(a)))
            a.print()
            i += 1

    def add_argument(self, type, value):
        arg = None
        if type == 'var':
            frame, id = value.split("@")
            arg = Variable(id, None, None, frame)
        elif type == 'label':
            arg = Symbol('label', value)
        else:
            if type in ['int', 'bool', 'string', 'nil']:
                arg = Const(type, value)
            else:
                RC().exit_e(RC.BAD_XML_TREE)

        if arg is None:
            exit(1)
        self.__args.append(arg)

    def __check_order(self):
        if self.order < 1:
            RC().exit_e(RC.BAD_XML_TREE)

    def _check_args(self, num: int):
        if len(self.args) != num:
            # TODO: check if error return code is correct
            RC().exit_e(RC.SEMANTIC)

    @staticmethod
    def _check_variable(a):
        if not isinstance(a, Variable):
            RC().exit_e(RC.SEMANTIC)

    @staticmethod
    def _check_symb(s):
        if not isinstance(s, Symbol):
            RC().exit_e(RC.SEMANTIC)

    @staticmethod
    def _check_const(c):
        if not isinstance(c, Const):
            RC().exit_e(RC.SEMANTIC)

    def _check_label(self, l):
        self._check_symb(l)
        if l.type != 'label':
            RC().exit_e(RC.SEMANTIC)


class ZeroArgumentInst(Instruction):
    def __init__(self, order):
        super().__init__(order)


class OneArgumentInst(Instruction):
    # inst = OneArgumentInst(name, order)
    def __init__(self, order):
        super().__init__(order)


class TwoArgumentInst(Instruction):
    def __init__(self, order):
        super().__init__(order)


class ThreeArgumentInst(Instruction):
    def __init__(self, order):
        super().__init__(order)


class CREATEFRAME(ZeroArgumentInst):
    def __init__(self, order):
        super().__init__(order)


class PUSHFRAME(ZeroArgumentInst):
    def __init__(self, order):
        super().__init__(order)


class POPFRAME(ZeroArgumentInst):
    def __init__(self, order):
        super().__init__(order)


class RETURN(ZeroArgumentInst):
    def __init__(self, order):
        super().__init__(order)


class BREAK(ZeroArgumentInst):
    def __init__(self, order):
        super().__init__(order)


class DEFVAR(OneArgumentInst):
    def __init__(self, order):
        super().__init__(order)


class POPS(OneArgumentInst):
    def __init__(self, order):
        super().__init__(order)


class PUSHS(OneArgumentInst):
    def __init__(self, order):
        super().__init__(order)


class WRITE(OneArgumentInst):
    def __init__(self, order):
        super().__init__(order)


class EXIT(OneArgumentInst):
    def __init__(self, order):
        super().__init__(order)


class DPRINT(OneArgumentInst):
    def __init__(self, order):
        super().__init__(order)


class CALL(OneArgumentInst):
    def __init__(self, order):
        super().__init__(order)


class LABEL(OneArgumentInst):
    def __init__(self, order):
        super().__init__(order)


class JUMP(OneArgumentInst):
    def __init__(self, order):
        super().__init__(order)


class INT2CHAR(TwoArgumentInst):
    def __init__(self, order):
        super().__init__(order)


class STRLEN(TwoArgumentInst):
    def __init__(self, order):
        super().__init__(order)


class TYPE(TwoArgumentInst):
    def __init__(self, order):
        super().__init__(order)


class MOVE(TwoArgumentInst):
    def __init__(self, order):
        super().__init__(order)


class NOT(TwoArgumentInst):
    def __init__(self, order):
        super().__init__(order)


class READ(TwoArgumentInst):
    def __init__(self, order):
        super().__init__(order)


class CONCAT(ThreeArgumentInst):
    def __init__(self, order):
        super().__init__(order)


class GETCHAR(ThreeArgumentInst):
    def __init__(self, order):
        super().__init__(order)


class SETCHAR(ThreeArgumentInst):
    def __init__(self, order):
        super().__init__(order)


class STRI2INT(ThreeArgumentInst):
    def __init__(self, order):
        super().__init__(order)


class ADD(ThreeArgumentInst):
    def __init__(self, order):
        super().__init__(order)


class SUB(ThreeArgumentInst):
    def __init__(self, order):
        super().__init__(order)


class MUL(ThreeArgumentInst):
    def __init__(self, order):
        super().__init__(order)


class IDIV(ThreeArgumentInst):
    def __init__(self, order):
        super().__init__(order)


class LT(ThreeArgumentInst):
    def __init__(self, order):
        super().__init__(order)


class GT(ThreeArgumentInst):
    def __init__(self, order):
        super().__init__(order)


class EQ(ThreeArgumentInst):
    def __init__(self, order):
        super().__init__(order)


class AND(ThreeArgumentInst):
    def __init__(self, order):
        super().__init__(order)


class OR(ThreeArgumentInst):
    def __init__(self, order):
        super().__init__(order)


class JUMPIFEQ(ThreeArgumentInst):
    def __init__(self, order):
        super().__init__(order)


class JUMPIFNEQ(ThreeArgumentInst):
    def __init__(self, order):
        super().__init__(order)

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