from lib.ReturnCodes import ReturnCodes as RC
import sys


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

    def print(self):
        sys.stderr.write("\tConst\n"
                         "\t\ttype {} with value \'{}\'\n".format(self.type, str(self.value)))


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
        sys.stderr.write("\tVariable: {} in {} frame\n"
                         "\t\ttype \'{}\' with value: \'{}\'\n"
                         "".format(self.id,
                                   self.__frame,
                                   (str(self.type) if self.type is not None else 'none'),
                                   (str(self.value) if self.value is not None else 'none')))


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
        sys.stderr.write("\t--- Stack bottom")
        for i in self.__items:
            i.print()
        sys.stderr.write("\tStack top ---")


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
            sys.stderr.write("\tNo.{}:".format(n))
            i.print()
            n += 1

    # Returns size of the frame
    def size(self) -> int:
        return len(self.__items)

    def define_var(self, var: Variable):
        if not self.contains(var.id):
            self.__items.append(var)
        else:
            RC(RC.SEMANTIC)

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
            RC(RC.UNDEFINED_VARIABLE)

    def update_var(self, type, value, id=None):
        if self.contains(id):
            for var in self.__items:
                if var.id == id:
                    var.type = type
                    var.value = value
        else:
            RC(RC.UNDEFINED_VARIABLE)