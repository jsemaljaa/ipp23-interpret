from interpret_classes.Variable import Variable

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
        return len(self.items)

    def define_var(self, var: Variable):
        self.__items.append(var)

    def contains(self, id) -> True | False:
        for i in self.__items:
            if i.id == id:
                return True
        return False

    def get_var(self, id) -> Variable:
        for i in self.__items:
            if i.id == id:
                return i

    def update_var(self, id, type, value):
        for i in self.__items:
            if i.id == id:
                i.type = type
                i.value = value
