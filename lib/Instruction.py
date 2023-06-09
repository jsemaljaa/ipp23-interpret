import sys

from lib.DataStructures import *
import re


class Instruction:
    def __init__(self, order: int) -> None:
        self.__order = order
        self.__args = []
        self.__required = []

        self.__check_order()

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
        sys.stderr.write("Instruction: \'{}\' with order: {}".format(str(type(self)), str(self.__order)))
        self.__print_args()

    def __print_args(self):
        i = 1
        for a in self.args:
            sys.stderr.write("\t{}. type: \'{}\'".format(str(i), str(type(a))))
            a.print()
            i += 1

    def set_args(self, args: list):
        self.__args = args
        self.check_instruction_arguments()

    def __check_order(self):
        if not isinstance(self.order, int) or self.order < 1:
            RC(RC.BAD_XML_TREE)

    def check_instruction_arguments(self):
        if len(self.args) != len(self.required):
            RC(RC.BAD_XML_TREE)
        i = 0
        for arg in self.args:
            if isinstance(arg, self.required[i]): # noqa
                i += 1
            else:
                RC(RC.BAD_XML_TREE)


class ZeroArgs(Instruction):
    def __init__(self, order):
        super().__init__(order)
        self.required = []


class CREATEFRAME(ZeroArgs): pass
class PUSHFRAME(ZeroArgs): pass
class POPFRAME(ZeroArgs): pass
class RETURN(ZeroArgs): pass
class BREAK(ZeroArgs): pass


class OneVariable(Instruction):
    def __init__(self, order):
        super().__init__(order)
        self.required = [Variable]


class DEFVAR(OneVariable): pass
class POPS(OneVariable): pass


class OneSymbol(Instruction):
    def __init__(self, order):
        super().__init__(order)
        self.required = [Symbol]


class PUSHS(OneSymbol): pass
class WRITE(OneSymbol): pass
class EXIT(OneSymbol): pass
class DPRINT(OneSymbol): pass


class OneLabel(Instruction):
    def __init__(self, order):
        super().__init__(order)
        self.required = [Label]


class CALL(OneLabel): pass
class LABEL(OneLabel): pass
class JUMP(OneLabel): pass


class VarSymb(Instruction):
    def __init__(self, order):
        super().__init__(order)
        self.required = [Variable, Symbol]


class INT2CHAR(VarSymb):
    @staticmethod
    def exec(v: Variable, s: Symbol) -> Variable:
        if s.type != 'int':
            RC(RC.OPERAND_TYPE)
        v.type = 'string'
        try:
            v.value = chr(s.value)
        except ValueError:
            RC(RC.BAD_STRING)

        return v


class STRLEN(VarSymb):
    @staticmethod
    def exec(v: Variable, s: Symbol):
        if s.type != 'string':
            RC(RC.OPERAND_TYPE)
        v.value = len(s.value)
        v.type = 'int'
        return v


class TYPE(VarSymb):
    @staticmethod
    def exec(v: Variable, s: Symbol) -> Variable:
        v.type = 'string'
        if s.type is None:
            v.value = ''
        else:
            v.value = s.type

        return v


class MOVE(VarSymb):
    @staticmethod
    def exec(v: Variable, s: Symbol) -> Variable:
        v.type = s.type
        v.value = s.value
        return v


class NOT(VarSymb):
    @staticmethod
    def exec(v: Variable, s: Symbol):
        if s.type != 'bool':
            RC(RC.OPERAND_TYPE)
        v.type = 'bool'
        if s.value == 'true':
            v.value = 'false'
        else:
            v.value = 'true'

        return v


class READ(Instruction):
    def __init__(self, order):
        super().__init__(order)
        self.required = [Variable, Type]

    @staticmethod
    def exec(input, reqType, v: Variable) -> Variable:
        if reqType == 'int':
            try:
                v.value = int(input)
                v.type = 'int'
            except ValueError:
                v.value = 'nil'
                v.type = 'nil'
        elif reqType == 'string':
            v.value = input
            v.type = 'string'
        elif reqType == 'bool':
            v.type = 'bool'
            if re.match(r'^true$', input, re.IGNORECASE):
                v.value = 'true'
            else:
                if input == '':
                    v.value = 'nil'
                    v.type = 'nil'
                else:
                    v.value = 'false'
        return v


class VarSymbSymb(Instruction):
    def __init__(self, order):
        super().__init__(order)
        self.required = [Variable, Symbol, Symbol]


class CONCAT(VarSymbSymb):
    @staticmethod
    def exec(v: Variable, s1: Symbol, s2: Symbol) -> Variable:
        if s1.type != 'string' or s2.type != 'string':
            RC(RC.OPERAND_TYPE)
        v.type = 'string'
        v.value = s1.value + s2.value
        return v


class GETCHAR(VarSymbSymb):
    @staticmethod
    def exec(v: Variable, s1: Symbol, s2: Symbol) -> Variable:
        if s1.type != 'string' or s2.type != 'int' or int(s2.value) < 0:
            RC(RC.OPERAND_TYPE)

        try:
            v.value = s1.value[int(s2.value)]
        except IndexError:
            RC(RC.BAD_STRING)

        return v


class SETCHAR(VarSymbSymb):
    @staticmethod
    def exec(v: Variable, s1: Symbol, s2: Symbol) -> Variable:
        if v.type != 'string' or s1.type != 'int' or s1.value < 0 or s2.type != 'string':
            RC(RC.OPERAND_TYPE)

        if s2.value == '':
            RC(RC.BAD_STRING)

        try:
            tmp = list(v.value)
            tmp[int(s1.value)] = s2.value[0]
            v.value = ''.join(tmp)
        except IndexError:
            RC(RC.BAD_STRING)

        return v


class STRI2INT(VarSymbSymb):
    @staticmethod
    def exec(v: Variable, s1: Symbol, s2: Symbol) -> Variable:
        if s1.type != 'string' or s2.type != 'int' or s2.value < 0:
            RC(RC.OPERAND_TYPE)

        try:
            v.type = 'int'
            v.value = ord(s1.value[int(s2.value)])
        except IndexError:
            RC(RC.BAD_STRING)

        return v


class Arithmetics(VarSymbSymb):
    @staticmethod
    def _check_sem(s1: Symbol, s2: Symbol):
        if s1.type != 'int' or s2.type != 'int':
            RC(RC.OPERAND_TYPE)


class ADD(Arithmetics):
    def exec(self, v: Variable, s1: Symbol, s2: Symbol) -> Variable:
        self._check_sem(s1, s2)
        v.value = s1.value + s2.value
        v.type = 'int'
        return v


class SUB(Arithmetics):
    def exec(self, v: Variable, s1: Symbol, s2: Symbol) -> Variable:
        self._check_sem(s1, s2)
        v.value = s1.value - s2.value
        v.type = 'int'
        return v


class MUL(Arithmetics):
    def exec(self, v: Variable, s1: Symbol, s2: Symbol) -> Variable:
        self._check_sem(s1, s2)
        v.value = s1.value * s2.value
        v.type = 'int'
        return v


class IDIV(Arithmetics):
    def exec(self, v: Variable, s1: Symbol, s2: Symbol) -> Variable:
        self._check_sem(s1, s2)
        if s2.value == 0:
            RC(RC.OPERAND_VALUE)
        v.value = s1.value // s2.value
        v.type = 'int'
        return v


class Relation(VarSymbSymb):
    @staticmethod
    def _check_sem(s1: Symbol, s2: Symbol):
        if s1.type != s2.type:
            RC(RC.OPERAND_TYPE)


class LT(Relation):
    def exec(self, v: Variable, s1: Symbol, s2: Symbol):
        self._check_sem(s1, s2)
        v.type = 'bool'
        if s1.type == 'bool':
            v.value = 'true' if s1.value == 'false' and s2.value == 'true' else 'false'
        elif s1.type == 'string':
            v.value = 'true' if s1.value < s2.value else 'false'
        elif s1.type == 'int':
            v.value = 'true' if int(s1.value) < int(s2.value) else 'false'
        else:
            RC(RC.OPERAND_TYPE)

        return v


class GT(Relation):
    def exec(self, v: Variable, s1: Symbol, s2: Symbol):
        self._check_sem(s1, s2)
        v.type = 'bool'
        if s1.type == 'bool':
            v.value = 'true' if s1.value == 'true' and s2.value == 'false' else 'false'
        elif s1.type == 'string':
            v.value = 'true' if s1.value > s2.value else 'false'
        elif s1.type == 'int':
            v.value = 'true' if int(s1.value) > int(s2.value) else 'false'
        else:
            RC(RC.OPERAND_TYPE)

        return v


class EQ(Relation):
    @staticmethod
    def exec(v: Variable, s1: Symbol, s2: Symbol):
        if s1.type == 'nil' or s2.type == 'nil':
            v.type = 'bool'
            v.value = 'true' if s1.value == 'nil' and s2.value == 'nil' else 'false'
            return v

        if s1.type != s2.type:
            RC(RC.OPERAND_TYPE)

        v.type = 'bool'
        if s1.type == 'bool':
            v.value = 'true' if s1.value == s2.value else 'false'
        elif s1.type == 'string':
            v.value = 'true' if s1.value == s2.value else 'false'
        elif s1.type == 'int':
            v.value = 'true' if int(s1.value) == int(s2.value) else 'false'

        return v


class Logic(VarSymbSymb):
    @staticmethod
    def _check_sem(s1: Symbol, s2: Symbol):
        if s1.type != 'bool' or s2.type != 'bool':
            RC(RC.OPERAND_TYPE)


class AND(Logic):
    def exec(self, v: Variable, s1: Symbol, s2: Symbol) -> Variable:
        self._check_sem(s1, s2)

        v.type = 'bool'
        v.value = 'true' if s1.value == 'true' and s2.value == 'true' else 'false'

        return v


class OR(Logic):
    def exec(self, v: Variable, s1: Symbol, s2: Symbol) -> Variable:
        self._check_sem(s1, s2)

        v.type = 'bool'
        v.value = 'true' if s1.value == 'true' or s2.value == 'true' else 'false'

        return v


class LabelSymbSymb(Instruction):
    def __init__(self, order):
        super().__init__(order)
        self.required = [Label, Symbol, Symbol]

    @staticmethod
    def _check_sem(s1: Symbol, s2: Symbol):
        if not (s1.type == 'nil' or s2.type == 'nil' or s1.type == s2.type):
            RC(RC.OPERAND_TYPE)


class JUMPIFEQ(LabelSymbSymb):
    def exec(self, s1: Symbol, s2: Symbol) -> bool:
        self._check_sem(s1, s2)

        if s1.value == s2.value:
            return True
        else:
            return False


class JUMPIFNEQ(LabelSymbSymb):
    def exec(self, s1: Symbol, s2: Symbol) -> bool:
        self._check_sem(s1, s2)

        if s1.value != s2.value:
            return True
        else:
            return False


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