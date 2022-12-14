import sys
sys.path.append("./")

from abstraction import *
import error


class Registers():
    def __init__(self, rsp_val=Word(0)):
        self.names = ['rax', 'rcx', 'rdx', 'rbx', 'rsp', 'rbp', 'rsi', 'rdi',
                      'r8', 'r9', 'r10', 'r11', 'r12', 'r13', 'r14']
        self.regs = []
        for _ in range(15):
            self.regs.append(Word(0))
        # rsp should be set to 0x0?
        self.write(self.get_rsp(), Word(0))

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
        
        # invalid reg adr
        if 0 > address or address > 15:
            raise error.AddressError('invalid register address')

        assert isinstance(self.regs[address], Word), 'not initialized reg! (should not run here)'
        return self.regs[address]

    def write(self, address, val):
        '''
         val should both be Word type.
        '''
        if val is None or address is None or address == 15:
            # skip or access no reg
            return False
        # invalid reg adr
        if 0 > address or address > 15:
            raise error.AddressError('invalid register address')
        self.regs[address] = val
        return True

    def get_rsp(self):
        return 4

    def show_rsp(self):
        return self.regs[self.get_rsp()].get_str_hex()

    def get_reg_dict(self, format='int'):
        d = {}
        for name, reg in zip(self.names, self.regs):
            if format == 'int':
                d[name] = reg.get_signed_value_int10()
            elif format == 'str':
                d[name] = reg.get_str_hex()
            else:
                assert False, 'should not run heres'
        return d