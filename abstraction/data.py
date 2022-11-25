class DataArb:
    def __init__(self, s):
        '''
        When initializing with int, may NOT have expected bit number
        because cannot auto complete starting zeros
        '''
        self._value = None
        if type(s) == str:
            self._load_str(s)
            return
        elif type(s) == int:
            self._load_int10(s)
            return
        elif type(s) == list:
            self._load_list(s)

    def _load_str(self, string):
        self._value = []
        for s in string:
            assert s in ['0', '1'], 'must be binary'
            self._value.append(int(s))
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

    def _load_list(self, ls):
        self._value = []
        if type(ls[0]) == int:
            for i in ls:
                assert type(i) == int and i in [0, 1], 'bad input for data'
            self._value = ls
        elif type(ls[0]) == str:
            for i in ls:
                assert type(i) == str and i in ['0', '1']
                self._value.append(int(i))
        else:
            assert 0, 'bad input for data'

    def print_val_ls(self):
        print(self._value)

    def get_value_int10(self):
        # returns a decimal equal to the value of the data
        res = 0
        for b in self._value:
            res *= 2
            res += b
        return res

    def get_bit_len(self):
        return len(self._value)

    def get_byte_len(self):
        return len(int(len(self._value)))

    def get_nth_byte(self, n):
        assert (n + 1) * 8 <= len(self._value), 'exceed range'
        b = Byte(self._value[n * 8: (n + 1) * 8])
        return b


class Word(DataArb):
    def __init__(self, s):
        '''
        initialize data using string
        '''
        assert type(s) in [str, list, int], 'bad input type for Word'
        assert (type(s) in [str, list] and len(s) == 64) or (
            type(s) == int and s < 2 ** 64), 'bad input value for Word'
        self._value = None
        super().__init__(s)

    def _load_int10(self, x):
        self._value = []
        while x > 0:
            self._value.insert(0, x % 2)
            # not sure if safe
            x >>= 1
        for _ in range(64 - len(self._value)):
            self._value.insert(0, 0)


class Byte(DataArb):
    def __init__(self, s):
        assert type(s) in [str, list, int], 'bad input type for Byte'
        assert (type(s) in [str, list] and len(s) == 8) or (
            type(s) == int and s < 2 ** 8), 'bad input value for Byte'
        self._value = None
        super().__init__(s)

    def _load_int10(self, x):
        self._value = []
        while x > 0:
            self._value.insert(0, x % 2)
            # not sure if safe
            x >>= 1
        for _ in range(8 - len(self._value)):
            self._value.insert(0, 0)
