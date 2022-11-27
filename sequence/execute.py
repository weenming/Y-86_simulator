import sys
sys.path.append("./")
from abstraction import *


def select_operation(cpu):
    icode = cpu.icode
    if icode in [0, 1]:
        assert 0, 'bad icode: should not run here'
    elif icode == 6:  # OPq
        op1 = cpu.valB
        op2 = cpu.valA
        ifun = cpu.ifun
        assert ifun is not None, 'ifun should have been initialized'
        if ifun == 0:
            operator = '+'
        elif ifun == 1:
            operator = '-'
        elif ifun == 2:
            operator = '&'
        elif ifun == 3:
            operator = '^'
        else:
            assert 0, 'bad ifun, should have been handled'
    elif icode == 2:  # rrmovq
        operator = '+'
        op1 = Word(0)
        op2 = cpu.valA
    elif icode == 3:  # irmovq
        operator = '+'
        op1 = Word(0)
        op2 = cpu.valC
    elif icode in [4, 5]:  # rmmov, mrmov
        operator = '+'
        op1 = cpu.valB
        op2 = cpu.valC
    elif icode == 10:  # pushq
        operator = '+'
        op1 = cpu.valB
        op2 = Word(-8)
    elif icode == 1:  # popq
        operator = '+'
        op1 = cpu.valB
        op2 = Word(8)
    elif icode == 7:  # jXX
        operator = None
        op1 = None
        op2 = None
    else:
        assert 0, 'should not run here'
    return op1, op2, operator


def do_update_cc(cpu):
    if cpu.icode == 6:
        return True
    else:
        return False


def do_update_cnd(cpu):
    if cpu.icode in [2, 7]:  # jXX or cmovq
        return True
    else:
        return False
