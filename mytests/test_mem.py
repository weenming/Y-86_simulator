import sys
sys.path.append("./")
from CPU import *
from abstraction import *
from hardware import *


def test_sz():
    byte_ls = []
    for _ in range(0x10):
        byte_ls.append(Byte(0x23))

    mem = Memory(byte_ls)
    mem.write(0x15, Word('0xa129384273'))

    mem.show_mem(show_ins=True, show_zero=False)


if __name__ == '__main__':
    test_sz()
