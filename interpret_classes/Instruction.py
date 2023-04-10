from interpret_classes.Argument import Argument
from interpret_classes.ReturnCodes import ReturnCodes as RC
from interpret_classes.Variable import Variable
from interpret_classes.Const import Const
from interpret_classes.Frame import Frame
from interpret_classes.Symbol import Symbol


class Instruction:
    def __init__(self, name: str, order: int) -> None:
        self.__name = name
        self.__order = order
        self.__args = []

        self.__check_order()

    @property
    def name(self):
        return self.__name

    @property
    def order(self):
        return self.__order

    @property
    def args(self):
        return self.__args

    def print(self):
        print("Instruction name: " + self.__name + " with order: " + str(self.__order))

    def print_args(self):
        i = 1
        for a in self.args:
            print("\t" + str(i) + ". type: " + str(type(a)))
            a.print()
            i += 1

    def add_argument(self, type, value):
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
        self.__args.append(arg)

    def __check_order(self):
        if self.order < 1:
            print("AAA")
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


class OneArgumentInst(Instruction):
    # inst = OneArgumentInst(name, order)
    def __init__(self, name, order):
        super().__init__(name, order)
        super()._check_args(1)


class TwoArgumentInst(Instruction):
    def __init__(self, name, order):
        super().__init__(name, order)
        super()._check_args(2)


class ThreeArgumentInst(Instruction):
    def __init__(self, name, order):
        super().__init__(name, order)
        super()._check_args(3)


class DEFVAR(OneArgumentInst):
    def __init__(self, name, order):
        super().__init__(name, order)
        self._check_variable(self.args[0])


class POPS(OneArgumentInst):
    def __init__(self, name, order):
        super().__init__(name, order)
        self._check_variable(self.args[0])


class PUSHS(OneArgumentInst):
    def __init__(self, name, order):
        super().__init__(name, order)
        self._check_symb(self.args[0])


class WRITE(OneArgumentInst):
    def __init__(self, name, order):
        super().__init__(name, order)
        self._check_symb(self.args[0])


class EXIT(OneArgumentInst):
    def __init__(self, name, order):
        super().__init__(name, order)
        self._check_symb(self.args[0])


class DPRINT(OneArgumentInst):
    def __init__(self, name, order):
        super().__init__(name, order)
        self._check_symb(self.args[0])


class CALL(OneArgumentInst):
    def __init__(self, name, order):
        super().__init__(name, order)
        self._check_label(self.args[0])


class LABEL(OneArgumentInst):
    def __init__(self, name, order):
        super().__init__(name, order)
        self._check_label(self.args[0])


class JUMP(OneArgumentInst):
    def __init__(self, name, order):
        super().__init__(name, order)
        self._check_label(self.args[0])