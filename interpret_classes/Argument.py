

class Argument:
    """
    Class for instructions arguments:
        type could be either symbol (therefore var or const), var, const and label
        value is none for label type of argument
    """
    def __init__(self, type, value):
        self.__type = type
        self.__value = value

    def print(self):
        if self.__value is None:
            self.__value = ''
        print("\tArgument type: " + self.__type + " with value: " + self.__value)

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, type):
        self.__type = type

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value