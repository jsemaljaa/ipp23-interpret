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

    def add_args_list(self, args: list):
        self.__args = args

    def process_arg(self, type, value, order=None):
        arg = None
        if type == 'var':
            frame, id = value.split("@")
            arg = Variable(id=id, type=None, value=None, frame=frame)
        elif type == 'label':
            arg = Label(id=value)
        elif type == 'int':
            try:
                arg = Const(type=type, value=int(value))
            except ValueError:
                RC().exit_e(RC.BAD_XML_TREE)
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
                RC().exit_e(RC.BAD_XML_TREE)
            else:
                arg = Const(type=type, value=value)
        elif type == 'type':
            arg = Type(value=value)
        else:
            RC().exit_e(RC.BAD_XML_TREE)

        return arg
        # self.__args.append(arg)
        # self.__args.insert(order-1, arg)

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
                RC().exit_e(RC.BAD_XML_TREE)


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

    def exec(self, v: Variable, s: Symbol) -> Variable:
        if s.type != 'int':
            RC().exit_e(RC.OPERAND_TYPE)
        v.type = 'string'
        try:
            v.value = chr(s.value)
        except ValueError:
            RC().exit_e(RC.BAD_STRING)

        return v


class STRLEN(Instruction):
    def __init__(self, order):
        super().__init__(order)
        self.required = [Variable, Symbol]

    def exec(self, v: Variable, s: Symbol):
        if s.type != 'string':
            RC().exit_e(RC.OPERAND_TYPE)
        v.value = len(s.value)
        v.type = 'int'
        return v


class TYPE(Instruction):
    def __init__(self, order):
        super().__init__(order)
        self.required = [Variable, Symbol]

    def exec(self, v: Variable, s: Symbol) -> Variable:
        v.type = 'string'
        if s.type is None:
            v.value = ''
        else:
            v.value = s.type

        return v


class MOVE(Instruction):
    def __init__(self, order):
        super().__init__(order)
        self.required = [Variable, Symbol]

    def exec(self, v: Variable, s: Symbol) -> Variable:
        v.type = s.type
        v.value = s.value
        return v


class NOT(Instruction):
    def __init__(self, order):
        super().__init__(order)
        self.required = [Variable, Symbol]

    def exec(self, v: Variable, s: Symbol):
        if s.type != 'bool':
            RC().exit_e(RC.OPERAND_TYPE)
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

    def exec(self, input, reqType, v: Variable) -> Variable:
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


class CONCAT(Instruction):
    def __init__(self, order):
        super().__init__(order)
        self.required = [Variable, Symbol, Symbol]

    def exec(self, v: Variable, s1: Symbol, s2: Symbol) -> Variable:
        if s1.type != 'string' or s2.type != 'string':
            RC().exit_e(RC.OPERAND_TYPE)
        v.type = 'string'
        v.value = s1.value + s2.value
        return v


class GETCHAR(Instruction):

    def __init__(self, order):
        super().__init__(order)
        self.required = [Variable, Symbol, Symbol]

    def exec(self, v: Variable, s1: Symbol, s2: Symbol) -> Variable:
        if s1.type != 'string' or s2.type != 'int' or int(s2.value) < 0:
            RC().exit_e(RC.OPERAND_TYPE)

        try:
            v.value = s1.value[int(s2.value)]
        except IndexError:
            RC().exit_e(RC.BAD_STRING)

        return v


class SETCHAR(Instruction):
    def __init__(self, order):
        super().__init__(order)
        self.required = [Variable, Symbol, Symbol]

    def exec(self, v: Variable, s1: Symbol, s2: Symbol) -> Variable:
        if v.type != 'string' or s1.type != 'int' or s1.value < 0 or s2.type != 'string':
            RC().exit_e(RC.OPERAND_TYPE)

        if s2.value == '':
            RC().exit_e(RC.BAD_STRING)

        try:
            tmp = list(v.value)
            tmp[int(s1.value)] = s2.value[0]
            v.value = ''.join(tmp)
        except IndexError:
            RC().exit_e(RC.BAD_STRING)

        return v


class STRI2INT(Instruction):
    def __init__(self, order):
        super().__init__(order)
        self.required = [Variable, Symbol, Symbol]

    def exec(self, v: Variable, s1: Symbol, s2: Symbol) -> Variable:
        if s1.type != 'string' or s2.type != 'int' or s2.value < 0:
            RC().exit_e(RC.OPERAND_TYPE)

        try:
            v.type = 'int'
            v.value = ord(s1.value[int(s2.value)])
        except IndexError:
            RC().exit_e(RC.BAD_STRING)

        return v


class Arithmetics(Instruction):
    def __init__(self, order):
        super().__init__(order)
        self.required = [Variable, Symbol, Symbol]

    def _check_sem(self, s1: Symbol, s2: Symbol):
        if s1.type != 'int' or s2.type != 'int':
            RC().exit_e(RC.OPERAND_TYPE)

class ADD(Arithmetics):
    def __init__(self, order):
        super().__init__(order)

    def exec(self, v: Variable, s1: Symbol, s2: Symbol) -> Variable:
        self._check_sem(s1, s2)
        v.value = s1.value + s2.value
        v.type = 'int'
        return v


class SUB(Arithmetics):
    def __init__(self, order):
        super().__init__(order)

    def exec(self, v: Variable, s1: Symbol, s2: Symbol) -> Variable:
        self._check_sem(s1, s2)
        v.value = s1.value - s2.value
        v.type = 'int'
        return v


class MUL(Arithmetics):
    def __init__(self, order):
        super().__init__(order)

    def exec(self, v: Variable, s1: Symbol, s2: Symbol) -> Variable:
        self._check_sem(s1, s2)
        v.value = s1.value * s2.value
        v.type = 'int'
        return v


class IDIV(Arithmetics):
    def __init__(self, order):
        super().__init__(order)

    def exec(self, v: Variable, s1: Symbol, s2: Symbol) -> Variable:
        self._check_sem(s1, s2)
        if s2.value == 0:
            RC().exit_e(RC.OPERAND_VALUE)
        v.value = s1.value // s2.value
        v.type = 'int'
        return v


class Relation(Instruction):
    def __init__(self, order):
        super().__init__(order)
        self.required = [Variable, Symbol, Symbol]

    def _check_sem(self, s1: Symbol, s2: Symbol):
        if s1.type != s2.type:
            RC().exit_e(RC.OPERAND_TYPE)


class LT(Relation):
    def __init__(self, order):
        super().__init__(order)

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
            RC().exit_e(RC.OPERAND_TYPE)

        return v


class GT(Relation):
    def __init__(self, order):
        super().__init__(order)

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
            RC().exit_e(RC.OPERAND_TYPE)

        return v


class EQ(Relation):
    def __init__(self, order):
        super().__init__(order)

    def exec(self, v: Variable, s1: Symbol, s2: Symbol):
        if s1.type == 'nil' or s2.type == 'nil':
            v.type = 'bool'
            v.value = 'true' if s1.value == 'nil' and s2.value == 'nil' else 'false'
            return v

        if s1.type != s2.type:
            RC().exit_e(RC.OPERAND_TYPE)


        v.type = 'bool'
        if s1.type == 'bool':
            v.value = 'true' if s1.value == s2.value else 'false'
        elif s1.type == 'string':
            v.value = 'true' if s1.value == s2.value else 'false'
        elif s1.type == 'int':
            v.value = 'true' if int(s1.value) == int(s2.value) else 'false'

        return v

class Logic(Instruction):
    def __init__(self, order):
        super().__init__(order)
        self.required = [Variable, Symbol, Symbol]

    def _check_sem(self, s1: Symbol, s2: Symbol):
        if s1.type != 'bool' or s2.type != 'bool':
            RC().exit_e(RC.OPERAND_TYPE)

class AND(Logic):
    def __init__(self, order):
        super().__init__(order)
        self.required = [Variable, Symbol, Symbol]

    def exec(self, v: Variable, s1: Symbol, s2: Symbol) -> Variable:
        self._check_sem(s1, s2)

        v.type = 'bool'
        v.value = 'true' if s1.value == 'true' and s2.value == 'true' else 'false'

        return v


class OR(Logic):
    def __init__(self, order):
        super().__init__(order)
        self.required = [Variable, Symbol, Symbol]

    def exec(self, v: Variable, s1: Symbol, s2: Symbol) -> Variable:
        self._check_sem(s1, s2)

        v.type = 'bool'
        v.value = 'true' if s1.value == 'true' or s2.value == 'true' else 'false'

        return v

# class ConditionJumps(Instruction):


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