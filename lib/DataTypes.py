class Symbol:

    # <var> is a variable
    # <symb> is either a const or variable

    # <var> => [LF|TF|GF]@ID
    # <const> => [int|bool|string|nil]@VALUE

    def __init__(self, type, value, id=None):
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


class Const(Symbol):

    def __init__(self, type, value):
        super().__init__(type, value)

    def print(self):
        print("\t\tConst: type " + self.type +
              "\n\t\tvalue: " + str(self.value))


class Variable(Symbol):
    # <var> is a variable
    # <symb> is either a const or variable

    # <var> => [LF|TF|GF]@ID
    # <const> => [int|bool|string|nil]@VALUE

    def __init__(self, id, type, value, frame):
        super().__init__(type, value, id)
        self.__frame = frame

    @property
    def frame(self):
        return self.__frame

    def print(self):
        print("\t\tVariable name: " + self.id +
              "\n\t\ttype: " + (str(self.type) if self.type is not None else 'none') +
              "\n\t\tvalue: " + (str(self.value) if self.value is not None else 'none') +
              "\n\t\tframe: " + self.__frame)