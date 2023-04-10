from interpret_classes.Symbol import Symbol


class Const(Symbol):

    def __init__(self, type, value):
        super().__init__(type, value)

    def print(self):
        print("\t\tConst: type " + self.type +
              "\n\t\tvalue: " + str(self.value))