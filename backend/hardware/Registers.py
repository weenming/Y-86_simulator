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
        # rsp should be initialized to 0x0?
        self._write(self.get_rsp_adr(), Word(0))

    def show_regs(self):
        for reg in self.regs:
            reg.print_bit_ls()
        return

    def show_regs_hex(self, show_zero=True):
        for i in range(len(self.regs)):
            if show_zero or self.regs[i].get_value_int10():
                print(f'{self.names[i]}({i}):', self.regs[i].get_str_hex())
        return

    def _read(self, address:Byte):
        '''
        Returns a Word type data
        '''
        address = address.get_value_int10()
        if  address == 15:
            # skip or access no reg
            return Word(0)
        
        # invalid reg adr
        if 0 > address or address > 15:
            raise error.AddressError('invalid register address')

        assert isinstance(self.regs[address], Word), 'not initialized reg! (should not run here)'
        return self.regs[address]

    def read_2_ports(self, address1, address2):
        '''
        Returns a Word type data
        '''
        return self._read(address1), self._read(address2)

    def _write(self, address:Byte, val):
        '''
         val should both be Word type.
        '''
        address = address.get_value_int10()
        if address == 15:
            # skip or access no reg
            return False
        # invalid reg adr
        if 0 > address or address > 15:
            raise error.AddressError('invalid register address')
        self.regs[address] = val
        return True

    def write_2_ports(self, adr1:Byte, adr2:Byte, val1:Word, val2:Word):
        self._write(adr1, val1)
        self._write(adr2, val2)

    @classmethod
    def get_rsp_adr(self):
        return Byte(4)

    def show_rsp(self):
        return self.regs[self.get_rsp()].get_str_hex()
    
    @classmethod
    def get_null_adr(self):
        return Byte(15)

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