class Stack:
    def __init__(self):
        self.__items = []
        
    # Push given object on top of the stack
    def push(self, object):
        self.__items.append(object)
    
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
