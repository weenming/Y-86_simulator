import sys
sys.path.append("./")
from abstraction import *


def select_write(cpu):
    if cpu.icode in [4, 10]:  # pushq or rmmovq
        return cpu.valE, cpu.valA
    elif cpu.icode == 8:
        return cpu.valE, Word(cpu.valP)  # callq
    else:
        return None, None


def select_read(cpu):
    if cpu.icode == 5:  # mrmovq
        return cpu.valE
    elif cpu.icode in [9, 11]:  # popq, ret
        return cpu.valA
    else:
        return None
