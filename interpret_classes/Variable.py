from interpret_classes.Symbol import Symbol


class Variable(Symbol):
    # <var> is a variable
    # <symb> is either a const or variable

    # <var> => [LF|TF|GF]@ID
    # <const> => [int|bool|string|nil]@VALUE

    def __init__(self, id, type, value, frame):
        super().__init__(type, value, id)
        self.__frame = frame

    def print(self):
        print("\t\tVariable name: " + self.id +
              "\n\t\ttype: " + (str(self.type) if self.type is not None else 'none') +
              "\n\t\tvalue: " + (str(self.value) if self.value is not None else 'none') +
              "\n\t\tframe: " + self.__frame)