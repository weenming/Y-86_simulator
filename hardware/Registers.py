import sys
sys.path.append("./")

from abstraction import *


class Registers():
    def __init__(self, rsp_val=Word(0)):
        self.names = ['rax', 'rcx', 'rdx', 'rbx', 'rsp', 'rbp', 'rsi', 'rdi',
                      'r8', 'r9', 'r10', 'r11', 'r12', 'r13', 'r14']
        self.regs = []
        for _ in range(15):
            self.regs.append(Word(0))
        self.write(self.get_rsp(), rsp_val)

    def show_regs(self):
        for reg in self.regs:
            reg.print_bit_ls()
        return

    def show_regs_hex(self, show_zero=True):
        for i in range(len(self.regs)):
            if show_zero or self.regs[i].get_value_int10():
                print(f'{self.names[i]}({i}):', self.regs[i].get_str_hex())
        return

    def read(self, address):
        '''
        Returns a Word type data
        '''
        if address is None or address == 15:
            # skip or access no reg
            return Word(0)
        # maybe the exception handling need improvement
        assert 0 <= address < 15, 'invalid register address'
        assert isinstance(self.regs[address], Word), 'not initialized reg!'
        return self.regs[address]

    def write(self, address, val):
        '''
         val should both be Word type.
        '''
        if val is None or address is None or address == 15:
            # skip or access no reg
            return False
        assert 0 <= address < 15, 'invalid register address'
        self.regs[address] = val
        return True

    def get_rsp(self):
        return 4

    def show_rsp(self):
        return self.regs[self.get_rsp()].get_str_hex()

    def get_reg_dict(self):
        d = {}
        for name, reg in zip(self.names, self.regs):
            d[name] = reg.get_signed_value_int10()
        return d