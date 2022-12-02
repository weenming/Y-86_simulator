class DataArb:
    def __init__(self, s):
        '''
        Data with arbitrary length

        When initializing with int, may NOT have intended bit number
        because cannot auto complete starting zeros
        int: decimal
        str: hex
        '''
        self._value = None
        if type(s) == str and s[0: 2] == '0x':
            self._load_str_hex(s)
            return
        elif type(s) == str:
            self._load_str_b(s)
        elif type(s) == int:
            self._load_int10(s)
            return
        elif isinstance(s, DataArb):
            self._load_list(s.get_bit_ls())
        elif type(s) == list:
            self._load_list(s)

    def _load_str_b(self, string):
        self._value = []
        for s in string:
            assert s in ['0', '1'], 'must be binary'
            self._value.append(int(s))
        return

    def _load_str_hex(self, h):
        self._load_int10(int(h, 16))
        self._add_zeros_for_hex((len(h) - 2) * 4)  # len except '0x'
        return

    def _load_int10(self, x):
        # Convert decimal int to list of "binary" numbers (still decimal but
        # has an either 0 or 1 value)
        # keep the value same
        self._value = []
        while x > 0:
            self._value.insert(0, x % 2)
            # not sure if safe
            x >>= 1
        return True

    def _add_zeros_for_hex(self, target_len):
        for _ in range(target_len - len(self._value)):
            self._value.insert(0, 0)

    def _load_list(self, ls):
        self._value = []
        if type(ls[0]) == int:
            for i in ls:
                assert type(i) == int and i in [0, 1], 'bad input for data'
            self._value = ls.copy()
        else:
            assert 0, 'bad input type for data'

    def print_bit_ls(self):
        print(self._value)

    def get_value_int10(self):
        # returns a unsigned decimal number equal to the value of the data
        res = 0
        for b in self._value:
            res *= 2
            res += b
        return res

    def get_str_hex(self):
        return hex(self.get_value_int10())

    def get_bit_ls(self):
        return self._value

    def get_bit_len(self):
        return len(self._value)

    def get_byte_len(self):
        return len(int(len(self._value)))

    def get_nth_byte(self, n):
        assert (n + 1) * 8 <= len(self._value), 'exceed range'
        b = Byte(self._value[n * 8: (n + 1) * 8])
        return b

    def get_bits(self, start, end):
        assert start >= 0 and end <= self.get_bit_len()
        return DataArb(self._value[start: end])

    def append_byte(self, s):
        assert type(s) == Byte
        try:
            self._value += s.get_bit_ls()
            assert self._check_validity()
        except AssertionError:
            print('Exception: can not append!')
            return False

    def _check_validity(self):
        return True

    def is_zero(self):
        if self._get_value_int10() == 0:
            return True
        else:
            return False


class Word(DataArb):
    def __init__(self, s):
        '''
        initialize data using string
        '''
        self.neg = False
        self._value = None
        # use only the same name binding, but in the cur frame, so all rewritten methods are substituted
        super().__init__(s)
        self._add_zeros()
        assert self._check_validity(), 'bad input Word!'
        if self._value[0] == 1:
            self.neg = True

    def _add_zeros(self):
        for _ in range(64 - len(self._value)):
            self._value.insert(0, 0)

    def _check_validity(self):
        if self._value is not None and self.get_bit_len() == 64:
            return True
        else:
            return False

    def _load_int10(self, x):
        # Convert decimal int to list of "binary" numbers (still decimal but
        # has an either 0 or 1 value)
        # keep the value same
        self._value = []
        if x < 0:
            self.neg = True
            x = -x - 1
            while x > 0:
                self._value.insert(0, x % 2)
                # not sure if safe
                x >>= 1
            self._add_zeros()
            self._value = self._get_inv_bits()
        else:
            while x > 0:
                self._value.insert(0, x % 2)
                # not sure if safe
                x >>= 1
            self._add_zeros()
        return True

    def _get_inv_bits(self):
        bits = []
        for b in self._value:
            bits.append(b)
        return bits

    def get_signed_value_int10(self):
        # returns signed decimal number
        print(self.neg)
        if self.neg:
            res = 0
            tmp_bits = self._get_inv_bits()
            for b in tmp_bits[1:]:
                res *= 2
                res += b
            res = -res - 1
        else:
            res = 0
            for b in self._value[1:]:
                res *= 2
                res += b
        return res


class Byte(DataArb):
    def __init__(self, s):
        self._value = None
        super().__init__(s)
        self._add_zeros()
        assert self._check_validity(), 'bad input Byte!'

    def _add_zeros(self):
        for _ in range(8 - len(self._value)):
            self._value.insert(0, 0)

    def _check_validity(self):
        if self._value is not None and self.get_bit_len() == 8:
            return True
        else:
            return False


class UnsignedWord(DataArb):
    def __init__(self, s):
        '''
        initialize data using string
        '''
        # use only the same name binding, but in the cur frame, so all rewritten methods are substituted
        super().__init__(s)
        self.neg = False
