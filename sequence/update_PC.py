from abstraction import *


def select_PC_val(cpu):
    if cpu.icode == 7:  # jXX
        return cpu.valP
    elif cpu.icode == 8:  # call
        return cpu.valC
    elif cpu.icode == 9:  # ret
        return cpu.valM
    else:
        return cpu.valP
