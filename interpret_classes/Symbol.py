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