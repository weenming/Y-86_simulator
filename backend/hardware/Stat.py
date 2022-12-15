import sys
sys.path.append("./")
# If trying to import CPU here, circular importing problem occurs.
import error

class Stat():
    def __init__(self):
        self.val = 1
        self.name_ls = ['AOK', 'HLT', 'ADR', 'INS']
        return

    def set(self, val, cpu):
        self.val = val
        if cpu.debug:
            print('cpu status before termination:')
            cpu.show_cpu()
            print(cpu.stat.name_ls[val - 1])


    def get_name(self):
        return self.name_ls[self.val - 1]

    def is_ok(self):
        return self.val == 1

    def raise_error(self):
        if self.val == 2:
            raise error.Halt
        elif self.val == 3:
            raise error.AddressError
        elif self.val == 4:
            raise error.InstructionError
        else:
            print('STAT: raise error: should not run here')