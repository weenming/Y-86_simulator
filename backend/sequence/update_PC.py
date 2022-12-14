from abstraction import *


def select_PC_val(cpu):
    if cpu.icode == 7:  # jXX
        if cpu.cnd == 1:  # cnd is true
            return cpu.valC.get_signed_value_int10()
        else:
            return cpu.valP
    elif cpu.icode == 8:  # call
        return cpu.valC.get_signed_value_int10()
    elif cpu.icode == 9:  # ret
        return cpu.valM.get_signed_value_int10()
    else:
        return cpu.valP
