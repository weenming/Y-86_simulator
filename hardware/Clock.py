import sys
sys.path.append("./")
# If trying to import CPU here, circular importing problem occurs.


class CondCode:
    def __init__(self):
        # initialize conditional codes
        self.ZF = 0
        self.SF = 0
        self.OF = 0
        return

    def set(self, cc_info):
        if cc_info is None:
            return
        # update those cc_info that are not None
        if cc_info['ZF'] is not None:
            cc_info['ZF']
            self.ZF = cc_info['ZF']
        if cc_info['SF'] is not None:
            self.SF = cc_info['SF']
        if cc_info['OF'] is not None:
            self.OF = cc_info['OF']
        return

    def is_condition(self, icode, ifun):
        # not tested
        assert icode in [2, 7]
        if ifun == 0:
            return 1
        elif ifun == 1:  # le
            # python does not have suitable bitwise not...
            return (self.SF ^ self.OF) | (self.ZF)
        elif ifun == 2:  # l
            return self.SF ^ self.OF
        elif ifun == 3:  # e
            return self.ZF
        elif ifun == 4:  # ne
            return ~self.ZF
        elif ifun == 5:  # ge
            return ~(self.SF ^ self.OF)
        elif ifun == 6:  # g
            return ~(self.SF ^ self.OF) & ~self.ZF

    def show(self):
        print('ZF:', self.ZF)
        print('SF:', self.SF)
        print('OF:', self.OF)


class Stat():
    def __init__(self):
        self.val = 1
        self.name_ls = ['AOK', 'HLT', 'ADR', 'INS']
        return

    def set(self, val):
        self.val = val

    def get_name(self):
        return self.name_ls[self.val - 1]
