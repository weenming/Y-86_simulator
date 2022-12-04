from abstraction import *


def select_write_back(cpu):
    if cpu.icode in [2, 3, 6]:
        return cpu.rB, cpu.valE
    elif cpu.icode == 5:  # mrmovq
        return cpu.rA, cpu.valM
    elif cpu.icode in [8, 9, 10, 11]:
        return cpu.registers.get_rsp(), cpu.valE
    elif cpu.icode in [0, 1, 4, 7]:  # hlt, nop, rmmovq, jXX
        return None, None
    return


def do_write_back_two(cpu):
    if cpu.icode == 11:
        return True


def select_write_back_2nd(cpu):
    if cpu.icode == 11:
        return cpu.rA, cpu.valM

    else:
        return None, None
