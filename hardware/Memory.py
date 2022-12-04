import sys
sys.path.append("./")

from abstraction import *
import error


class Memory:
    def __init__(self, byte_ls, max_adr=0x100):
        '''
        stack frame: subtracted starting from 0x100
        ins_mem: added starting from 0x0
        '''
        assert len(byte_ls) <= max_adr
        print('init mem')

        # stack frame cannot grow into space of program code
        self.rsp_min = len(byte_ls) + 8 - len(byte_ls) % 8
        while len(byte_ls) < max_adr:
            byte_ls.append(Byte(0))
        self.mem_bytes = byte_ls
        self.max_adr = max_adr
        return

    def read(self, adr: Word):
        '''
        Returns a Word type: red EIGHT BYTES from adr, and convert little endian
        data into Word type (big endian, I think)
        '''
        if adr is None:
            return Word(0)

        adr = adr.get_signed_value_int10()
        if adr < 0 or adr + 8 > self.max_adr:  # 'invalid mem adr when reading'
            raise error.AddressError

        # be: big endian; le: little endian
        byte_ls_le = self.mem_bytes[adr: adr + 8]
        bit_ls_be = self._reverse_byte_to_bit(byte_ls_le)
        return Word(bit_ls_be)

    def _reverse_byte_to_bit(self, byte_ls):
        '''
        reverse big/little endian byte (Byte type) list into little/big endian bit(int 0 or 1) list
        '''
        bit_ls = []
        for byte in byte_ls:
            bit_ls = byte.get_bit_ls() + bit_ls
        return bit_ls

    def write(self, adr: Word, val: Word):
        '''
        Convert a Word type into 8 bytes arranged in the little endian order
        and then write it to memory
        adr and val should both be words
        '''
        if adr is None or val is None:
            return

        adr = adr.get_signed_value_int10()
        if adr + 8 > self.max_adr:  # 'invalid mem adr: too big'
            raise error.AddressError
        if adr < self.rsp_min:  # 'invalid mem adr: access to read-only denied'
            raise error.AddressError

        for i in range(8):
            byte = val.get_nth_byte(7 - i)
            self.mem_bytes[adr + i] = byte
        return

    def get_ins(self, PC):
        byte_0th = self.mem_bytes[PC]
        if PC >= self.rsp_min:
            raise error.AddressError

        icode = byte_0th.get_bits(0, 4).get_value_int10()
        if icode in [0, 1, 9]:
            ins_bits = byte_0th.get_bit_ls()
        elif icode in [2, 6, 10, 11]:
            if PC + 1 >= self.rsp_min:
                raise error.AddressError
            ins_bits = byte_0th.get_bit_ls(
            ) + self.mem_bytes[PC + 1].get_bit_ls()
        elif icode in [3, 4, 5]:  # ir, rm, mrmovq
            if PC + 9 >= self.rap_min:
                raise error.AddressError
            val_byte_ls_le = self.mem_bytes[PC + 2: PC + 10]
            val_bit_ls_be = self._reverse_byte_to_bit(val_byte_ls_le)
            byte_1th_ls = self.mem_bytes[PC + 1]
            # icode, ifun | rA, rB | V(D) - big endian
            ins_bits = byte_0th.get_bit_ls() + byte_1th_ls.get_bit_ls() + val_bit_ls_be
        elif icode in [7, 8]:  # jXX, call
            if PC + 8 >= self.rsp_min:
                raise error.AddressError
            val_byte_ls_le = self.mem_bytes[PC + 1: PC + 9]
            val_bit_ls_be = self._reverse_byte_to_bit(val_byte_ls_le)
            # icode, ifun | Dest - big endian
            ins_bits = byte_0th.get_bit_ls() + val_bit_ls_be
        else:
            raise error.InstructionError
        return DataArb(ins_bits)

    def show_mem(self, show_ins=False, show_zero=False):
        res = {}
        if show_ins:
            for adr in range(0, self.rsp_min, 8):
                b = self._get_word(adr)
                res[adr] = b.get_str_hex()

        if show_zero:
            for adr in range(self.rsp_min, self.max_adr, 8):
                b = self._get_word(adr)
                res[adr] = b.get_str_hex()
        else:
            for adr in range(self.rsp_min, self.max_adr, 8):
                b = self._get_word(adr)
                if not b.is_zero():
                    res[adr] = b.get_str_hex()

        print(res)

    def _get_word(self, adr):
        assert adr < self.max_adr and adr >= 0
        bytes8 = self.mem_bytes[adr: adr + 8]
        bit_ls = []
        for byte in bytes8:
            bit_ls += byte.get_bit_ls()
        return Word(bit_ls)
