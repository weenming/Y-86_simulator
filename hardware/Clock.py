import sys
sys.path.append("./")
# If trying to import CPU here, circular importing problem occurs.
import error

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
            res = 1
        elif ifun == 1:  # le
            # python does not have suitable bitwise not...
            res = (self.SF ^ self.OF) | (self.ZF)
        elif ifun == 2:  # l
            res = self.SF ^ self.OF
        elif ifun == 3:  # e
            res = self.ZF
        elif ifun == 4:  # ne
            res = ~self.ZF
        elif ifun == 5:  # ge
            res = ~(self.SF ^ self.OF)
        elif ifun == 6:  # g
            res = ~(self.SF ^ self.OF) & ~self.ZF
        if res == 0:
            return False
        else:
            return True

    def show(self):
        print('ZF:', self.ZF)
        print('SF:', self.SF)
        print('OF:', self.OF)


class Stat():
    def __init__(self):
        self.val = 1
        self.name_ls = ['AOK', 'HLT', 'ADR', 'INS']
        return

    def set(self, val, cpu):
        self.val = val
        print('cpu status before termination:')
        cpu.show_cpu()
        print(cpu.stat.name_ls[val - 1])


    def get_name(self):
        return self.name_ls[self.val - 1]

    def is_ok(self):
        if self.val == 1:
            return True
        else:
            return False

    def raise_error(self):
        if self.val == 2:
            raise error.Halt
        elif self.val == 3:
            raise error.AddressError
        elif self.val == 4:
            raise error.InstructionError
        else:
            print('STAT: raise error: should not run here')