from lib.ReturnCodes import ReturnCodes as RC
import re


class Symbol:
    # <symb> is either a const or variable

    # <var> => [LF|TF|GF]@ID
    # <const> => [int|bool|string|nil]@VALUE

    def __init__(self, type=None, value=None, id=None):
        self._id = id
        self._type = type
        self._value = value

    def print(self):
        print("\t\tSymbol id: " + str(self._id) +
              "\n\t\ttype: " + self._type +
              "\n\t\tvalue: " + self._value)

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, type):
        self._type = type

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value


class Type(Symbol):
    def __init__(self, value):
        super().__init__(type='type', value=value)

    def print(self):
        print("\t\tType: ")


class Label(Symbol):
    def __init__(self, id):
        super().__init__(id=id, type='label')

    def print(self):
        print("\t\tLabel: " + self.id)


class Const(Symbol):
    # <const> => [int|bool|string|nil]@VALUE

    def __init__(self, type, value):
        super().__init__(type=type, value=value)
        # if type == 'string':
            # self.value.encode().decode("utf-8", "strict")
            # print(self.value)

    def print(self):
        print("\t\tConst: type " + self.type +
              "\n\t\tvalue: " + str(self.value))


class Variable(Symbol):
    # <var> is a variable
    # <var> => [LF|TF|GF]@ID

    def __init__(self, id, type, value, frame):
        super().__init__(type=type, value=value, id=id)
        self.__frame = frame

    @property
    def frame(self):
        return self.__frame

    def print(self):
        print("\t\tVariable name: " + self.id +
              "\n\t\ttype: " + (str(self.type) if self.type is not None else 'none') +
              "\n\t\tvalue: " + (str(self.value) if self.value is not None else 'none') +
              "\n\t\tframe: " + self.__frame)


class Stack:
    def __init__(self):
        self.__items = []

    # Push given object on top of the stack
    def push(self, obj):
        self.__items.append(obj)

    # Pop an object from the stack
    def pop(self):
        return self.__items.pop()

    # Returns size of a stack
    def size(self):
        return len(self.__items)

    # Returns object on top of the stack
    def top(self):
        return self.__items[-1]

    def is_empty(self):
        return self.size() == 0

    def print(self):
        print("\t-- stack bottom")
        for i in self.__items:
            i.print()
        print("\tstack top --")


class Frame:

    def __init__(self):
        """
        Frame containing list of defined variables
        Format: [Variable var1, Variable var2, ...]
        """
        self.__items = []

    def print(self):
        n = 1
        for i in self.__items:
            print(n)
            i.print()
            n += 1

    # Returns size of the frame
    def size(self):
        return len(self.__items)

    def define_var(self, var: Variable):
        if not self.contains(var.id):
            self.__items.append(var)
        else:
            RC().exit_e(RC.SEMANTIC)

    def contains(self, id: str) -> True | False:
        for var in self.__items:
            if var.id == id:
                return True
        return False

    def get_var(self, id: str) -> Variable:
        if self.contains(id):
            for i in self.__items:
                if i.id == id:
                    return i
        else:
            RC().exit_e(RC.UNDEFINED_VARIABLE)

    def update_var(self, type, value, id=None):
        if self.contains(id):
            for var in self.__items:
                if var.id == id:
                    var.type = type
                    var.value = value
        else:
            RC().exit_e(RC.UNDEFINED_VARIABLE)