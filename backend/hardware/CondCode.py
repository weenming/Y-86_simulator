import sys
sys.path.append("./")
# If trying to import CPU here, circular importing problem occurs.
import error

class CondCode:
    def __init__(self):
        # initialize conditional codes
        self.ZF = 1
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
        # Notice: did not specify the length of the number, so 
        # ~ does not behave properly. For example, ~1 = -2 but 
        # In our case, cc is 1-bit in length and thus -2 overflows.
        # (should be 0)
        # We are using 1 - instead
        assert icode in [2, 7]
        if ifun == 0:
            res = 1
        elif ifun == 1:  # le
            # python does not have suitable bitwise not...
            res = (self.SF ^ self.OF) | (self.ZF)
        elif ifun == 2:  # l
            res = self.SF ^ self.OF
        elif ifun == 3:  # e
            res = self.ZF
        elif ifun == 4:  # ne
            res = 1 - self.ZF
        elif ifun == 5:  # ge
            res = 1 - (self.SF ^ self.OF)
        elif ifun == 6:  # g
            res = (1 - (self.SF ^ self.OF)) & (1 - self.ZF)
        if res == 0:
            return 0
        else:
            return 1

    def show(self):
        print('ZF:', self.ZF)
        print('SF:', self.SF)
        print('OF:', self.OF)

    def get_CC_dict(self):
        d = {}
        d['ZF'] =  self.ZF
        d['SF'] =  self.SF
        d['OF'] =  self.OF
        return d

