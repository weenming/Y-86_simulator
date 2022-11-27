import sys
sys.path.append("./")

from abstraction import *
from hardware.Clock import *


class InstructMem():
    def __init__(self):
        self.icode = None
        self.ifun = None
        self.data = DataArb('0x00')
        return

    def update(self, data: DataArb):
        self.data = data
        self.len = self.data.get_bit_len()
        assert self.len % 8 == 0, 'instructions must be integer times of bytes!'
        assert self.len != 0, 'instructions cannot be empty!'
        # len in byte
        self.len /= 8

        # set icode and others if applicable
        self.icode = self.data.get_bits(0, 4).get_value_int10()
        self.ifun = self.data.get_bits(4, 8).get_value_int10()
        assert 0 <= self.icode < 12, 'invalid icode'

        return

    def get_instruction_name(self):
        names = ['halt', 'nop', 'rrmovq', 'irmovq', 'rmmovq', 'mrmovq',
                 'OPq', 'jXX', 'cmovXX', 'call', 'ret', 'pushq', 'popq']
        return names[self.icode]

    def get_valC(self):
        if self.icode in [3, 4, 5]:
            return Word(self.data.get_bits(16, 80))
        elif self.icode in [7, 8]:
            return Word(self.data.get_bits(8, 72))
        else:
            return None

    def get_reg_address(self) -> int:
        # not tested
        # notice: rA or rB == 16 means no access to regs
        if self.icode in [2, 3, 4, 5, 6, 10, 11]:
            rA = self.data.get_bits(8, 12).get_value_int10()
            rB = self.data.get_bits(12, 16).get_value_int10()
            return rA, rB
        elif self.icode in [0, 1, 7, 8, 9]:
            return None, None
        else:
            assert 0, 'bad icode'
            return

    def calc_valP(self):
        return self.len

    def is_condition(self, cc: CondCode):
        # not tested
        assert self.icode in [2, 7]
        if self.ifun == 0:
            return True
        elif self.ifun == 1:  # le
            # python does not have suitable bitwise not...
            return (cc.SF ^ cc.OF) | (cc.ZF)
        elif self.ifun == 2:  # l
            return cc.SF ^ cc.OF
        elif self.ifun == 3:  # e
            return cc.ZF
        elif self.ifun == 4:  # ne
            return ~cc.ZF
        elif self.ifun == 5:  # ge
            return ~(cc.SF ^ cc.OF)
        elif self.ifun == 6:  # g
            return ~(cc.SF ^ cc.OF) & ~cc.ZF
