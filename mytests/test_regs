import sys
sys.path.append("./")

from hardware import *
from abstraction import *


def test0():
    regs = Registers()
    regs.write(0, Word('0x7120bac182'))
    regs.write(14, Word('0xffffffff' + 'ffffffff'))
    try:
        regs.write(12, Word('0xffffffff' + 'ffffffff' + 'f'))
        print('write 65 bits success')
    except AssertionError:
        print('write 65 bits failure: assertion error')
    try:
        regs.write(13, Word(regs.read(14).get_value_int10() + 1))
        print('write 2^64 success')
    except AssertionError:
        print('write 65 bits failure: assertion error')

    try:
        regs.write(13, Word(regs.read(14).get_value_int10()))
        print('write 2^64 - 1 success')
    except AssertionError:
        print('write 65 bits failure: assertion error')
    # regs.show_regs()
    print('show regs:')
    regs.show_regs_hex()


if __name__ == '__main__':
    test0()
