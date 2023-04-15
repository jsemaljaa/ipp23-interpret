from lib.Instruction import Instruction, LABEL
from lib.DataStructures import Stack
from lib.ReturnCodes import ReturnCodes as RC


class InstructionsList:
    def __init__(self):
        self.__list = {}
        self.__counter = 0
        self.__pos = 1
        self.__callStack = Stack()
        self.__labels = {}

    @property
    def labels(self):
        return self.__labels

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
    def list(self):
        return self.__list

    def append(self, i: Instruction):
        self.__counter += 1
        if type(i) is LABEL:
            if i.args[0].id in self.__labels:
                RC().exit_e(RC.SEMANTIC)
            self.__labels[i.args[0].id] = self.__counter
        self.__list[i.order-1] = i

    def print(self):
        print(self.__list)

    def transform_list(self):
        d = dict(sorted(self.__list.items()))
        self.__list = list(d.values())

    def get_next_instruction(self) -> Instruction | None:
        if self.__pos > len(self.__list):
            return None
        else:
            instruction = self.__list[self.__pos-1]
            self.__pos += 1
            return instruction

    def store_pos(self):
        self.__callStack.push(self.__pos)

    def return_pos(self):
        if self.__callStack.is_empty():
            RC().exit_e(RC.MISSING_VALUE)
        else:
            self.__pos = self.__callStack.pop()
