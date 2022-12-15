from abstraction import *


def select_PC_val(cpu):
    if cpu.icode == 7:  # jXX
        if cpu.cnd == 1:  # cnd is true
            return cpu.valC
        else:
            return cpu.valP
    elif cpu.icode == 8:  # call
        return cpu.valC
    elif cpu.icode == 9:  # ret
        return cpu.valM
    else:
        return cpu.valP
