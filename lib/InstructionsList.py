from lib.Instruction import Instruction
from lib.DataStructures import Stack
from lib.ReturnCodes import ReturnCodes as RC


class InstructionsList:
    def __init__(self):
        self.__list = []
        self.__size = 0
        self.__pos = 0
        self.__callStack = Stack()
        self.__labels = {}

    @property
    def pos(self):
        return self.__pos

    @pos.setter
    def pos(self, new_pos: int):
        if new_pos <= 0:
            RC().exit_e(RC.SEMANTIC)
        else:
            self.__pos = new_pos

    @property
    def size(self):
        return self.__size

    @property
    def list(self):
        return self.__list

    def append(self, i: Instruction):
        self.__size += 1
        self.__list.append(i)

    def print(self):
        for i in self.__list:
            i.print()

    def get_next_instruction(self) -> Instruction | None:
        # print("pos is " + str(self.__pos) + " size is " + str(self.__size))
        if self.__pos >= self.__size:
            return None
        else:
            self.__pos += 1
            return self.__list[self.__pos - 1]

    def store_pos(self):
        self.__callStack.push(self.__pos)

    def return_pos(self):
        if self.__callStack.is_empty():
            RC().exit_e(RC.MISSING_VALUE)
        else:
            self.__pos = self.__callStack.pop()
