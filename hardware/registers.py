import sys
sys.path.append("./")

from abstraction import *


class Registers():
    def __init__(self):
        self.regs = []
        for _ in range(15):
            self.regs.append(Word(0))

    def show_regs(self):
        for reg in self.regs:
            reg.print_bit_ls()
        return

    def show_regs_hex(self):
        for reg in self.regs:
            print(reg.get_str_hex())
        return

    def read(self, address):
        '''
        Returns a Word type data
        '''
        if address == 15 or address is None:
            return False
        # maybe the exception handling need improvement
        if 0 <= address < 15:
            raise 'invalid register address'
        return self.regs[address]

    def write(self, address, val):
        '''
        val should be Word type.
        '''
        if address == 15 or val is None or address is None:
            return False
        if 0 <= address < 15:
            raise 'invalid register address'
        self.regs[address] = val
        return True
