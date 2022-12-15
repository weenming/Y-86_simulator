import sys
sys.path.append("./")

from abstraction import *
import error


class InstructMem():
    def __init__(self):
        self.icode = None
        self.ifun = None
        self.data = DataArb('0x00')
        return

    def update(self, data: DataArb):
        # The adr/instant number in argument `data` should be big-endian if applicable
        # So that conversion from mem data in little-endian is not required
        self.data = data
        self.len = self.data.get_bit_len()
        assert self.len % 8 == 0, 'instructions must be integer times of bytes!'
        assert self.len != 0, 'instructions cannot be empty!'
        # len in byte: / is float division
        self.len //= 8

        # set icode and others if applicable
        self.icode = self.data.get_bits(0, 4).get_value_int10()
        self.ifun = self.data.get_bits(4, 8).get_value_int10()
        if 0 > self.icode or self.icode > 12: # invalid instruction
            raise error.InstructionError('invalid icode')
        if not self._check_validity():
            raise error.InstructionError('invalid instruction')
        if self.icode == 0: # halt
            raise error.Halt()
        return self.icode, self.ifun

    def _check_validity(self):
        return True

    def get_instruction_name(self):
        names = ['halt', 'nop', 'rrmovq', 'irmovq', 'rmmovq', 'mrmovq',
                 'OPq', 'jXX', 'call', 'ret', 'pushq', 'popq', 'iaddq']
        return names[self.icode]

    def get_valC(self):
        if self.icode in [3, 4, 5, 12]: # irmov, rmmov, mrmov, iadd
            return Word(self.data.get_bits(16, 80))
        elif self.icode in [7, 8]:
            return Word(self.data.get_bits(8, 72))
        else:
            return None

    def get_reg_address(self) -> int:
        # not tested
        # notice: rA or rB == 16 means no access to regs
        if self.icode in [2, 3, 4, 5, 6, 10, 11, 12]:
            rA = self.data.get_bits(8, 12).get_value_int10()
            rB = self.data.get_bits(12, 16).get_value_int10()
            return rA, rB
        elif self.icode in [0, 1, 7, 8, 9]:
            return 15, 15
        else:
            assert 0, 'bad icode'
            return

    def calc_valP(self, last_PC: Word):
        return Word(self.len + last_PC.get_signed_value_int10())


