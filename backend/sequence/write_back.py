from abstraction import *

def select_write_back(cpu):
    null_adr = cpu.registers.get_null_adr()
    rsp_adr = cpu.registers.get_rsp_adr()
    if cpu.icode in [3, 6, 12]:
        return cpu.rB, null_adr
    elif cpu.icode == 2:
        if cpu.ifun == 0 or cpu.cnd == 1:
            return cpu.rB, null_adr
        else:
            return null_adr, null_adr
    elif cpu.icode == 5:  # mrmovq
        return null_adr, cpu.rA
    elif cpu.icode in [8, 9, 10]:
        return rsp_adr, null_adr
    elif cpu.icode in [11]:
        return rsp_adr, cpu.rA
    elif cpu.icode in [0, 1, 4, 7]:  # hlt, nop, rmmovq, jXX
        return null_adr, null_adr
    return
