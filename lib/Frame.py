from DataTypes import *
from ReturnCodes import ReturnCodes as RC

class Frame:

    def __init__(self):
        """
        Frame containing list of defined variables
        Format: [Variable var1, Variable var2, ...]
        """
        self.__items = []

    def print(self):
        for i in self.__items:
            i.print()

    # Returns size of the frame
    def size(self):
        return len(self.__items)

    def define_var(self, var: Variable):
        self.__items.append(var)

    def contains(self, id: str) -> True | False:
        for var in self.__items:
            if var.id == id:
                return True
        return False

    def get_var(self, id: str) -> Variable:
        for i in self.__items:
            if i.id == id:
                return i

    def update_var(self, type, value, id=None):
        if self.contains(id):
            for var in self.__items:
                if var.id == id:
                    var.type = type
                    var.value = value
        else:
            RC().exit_e(RC.SEMANTIC)