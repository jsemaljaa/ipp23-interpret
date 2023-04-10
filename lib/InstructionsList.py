from lib.Instruction import Instruction
from lib.Stack import Stack

class InstructionsList:
    def __init__(self):
        self.__list = []
        self.__counter = 0
        self.__current = 1
        self.__callStack = Stack()
        self.__labels = []

    def get_list(self):
        return self.__list

    def get_size(self):
        return self.__counter

    def append(self, i: Instruction):
        self.__counter += 1
        self.__list.append(i)

    def get_next_instruction(self) -> Instruction:
        if self.__current <= self.__counter:
            self.__current += 1
            return self.__list[self.__current]

    def add_position(self):
        self.__callStack.push(self.__current)

    def get_position(self):
        if not self.__callStack.is_empty():
            self.__current = self.__callStack.pop()
        # else:
        # error with empty callstack