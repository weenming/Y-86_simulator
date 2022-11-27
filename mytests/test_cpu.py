import sys
sys.path.append("./")
from CPU import *
from abstraction import *


def get_ins_test(PC):
    nop = DataArb('0x10')
    rrmovq = DataArb('0x20f1')
    halt = DataArb('0x00')
    ins = [nop, rrmovq, halt]
    return ins[PC]


def test0():
    cpu = CPU(get_ins=get_ins_test)
    cpu.fetch_stage()
    cpu.show_cpu()
    cpu.decode_stage()
    cpu.show_cpu()
    cpu.execute_stage()
    cpu.show_cpu()
    cpu.memory_stage()
    cpu.show_cpu()
    cpu.write_back_stage()
    cpu.show_cpu()
    cpu.decode_stage()


def test1():
    cpu = CPU(get_ins=get_ins_test)
    cpu.PC = 1
    cpu.fetch_stage()
    cpu.show_cpu()
    cpu.decode_stage()
    cpu.show_cpu()
    cpu.execute_stage()
    cpu.show_cpu()
    cpu.memory_stage()
    cpu.show_cpu()
    cpu.write_back_stage()
    cpu.show_cpu()
    cpu.decode_stage()


if __name__ == '__main__':
    test1()
