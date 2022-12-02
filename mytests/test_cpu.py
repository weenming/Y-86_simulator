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


def test0():  # nop
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


def test_rrmovq():
    def get_ins_rrmovq(PC):
        return DataArb('0x2001')
    cpu = CPU(Memory([Byte('0x00')], 0x100), get_ins=get_ins_rrmovq)
    cpu.PC = 0
    cpu.registers.write(0, Word('0xa0a6adbc709'))
    cpu.fetch_stage()
    print("\nAfter fetch:")
    cpu.show_cpu()
    cpu.memory.show_mem(show_zero=True, show_ins=True)

    cpu.decode_stage()
    print("\nAfter decode:")
    cpu.show_cpu()
    cpu.memory.show_mem(show_zero=True, show_ins=True)

    cpu.execute_stage()
    print("\nAfter execute:")
    cpu.show_cpu()
    cpu.memory.show_mem(show_zero=True, show_ins=True)

    cpu.memory_stage()
    print("\nAfter memory:")
    cpu.show_cpu()
    cpu.memory.show_mem(show_zero=True, show_ins=True)

    cpu.write_back_stage()
    print("\nAfter write back:")
    cpu.show_cpu()
    cpu.registers.show_regs_hex()
    cpu.memory.show_mem(show_zero=True, show_ins=True)

    cpu.update_PC()
    print("\nAfter update PC:")
    cpu.show_cpu()
    cpu.memory.show_mem(show_zero=True, show_ins=True)


def test_irmovq():
    # def get_ins_rrmovq(PC):
    #     return DataArb('0x')
    mem = Memory([Byte(0x30), Byte(0xf1), Byte(
        0x12), Byte(0x34), Byte(0x56), Byte(0x78), Byte(0x9a), Byte(0xbc), Byte(0xde), Byte(0xf0)])
    cpu = CPU(mem, get_ins=None)
    cpu.PC = 0
    cpu.registers.write(0, Word('0xa0a6adbc709'))

    cpu.fetch_stage()
    print("\nAfter fetch:")
    cpu.show_cpu()
    cpu.memory.show_mem(show_zero=True, show_ins=True)

    cpu.decode_stage()
    print("\nAfter decode:")
    cpu.show_cpu()
    cpu.memory.show_mem(show_zero=True, show_ins=True)

    cpu.execute_stage()
    print("\nAfter execute:")
    cpu.show_cpu()
    cpu.memory.show_mem(show_zero=True, show_ins=True)

    cpu.memory_stage()
    print("\nAfter memory:")
    cpu.show_cpu()
    cpu.memory.show_mem(show_zero=True, show_ins=True)

    cpu.write_back_stage()
    print("\nAfter write back:")
    cpu.show_cpu()
    cpu.registers.show_regs_hex()
    cpu.memory.show_mem(show_zero=True, show_ins=True)

    cpu.update_PC()
    print("\nAfter update PC:")
    cpu.show_cpu()
    cpu.memory.show_mem(show_zero=True, show_ins=True)


def test_rmmovq():
    # def get_ins_rrmovq(PC):
    #     return DataArb('0x')
    mem = Memory([Byte(0x40), Byte(0x01), Byte(
        0x20), Byte(0x00), Byte(0x0), Byte(0x00), Byte(0x0), Byte(0x0), Byte(0x0), Byte(0x0)])  # D = 0x20
    cpu = CPU(mem, get_ins=None)
    cpu.PC = 0
    cpu.registers.write(0, Word('0xabcdef'))  # val to move to mem = 0xabcdef
    cpu.registers.write(1, Word(0x2))  # adr to write += 0x2, adr is 0x22 now

    cpu.fetch_stage()
    print("\nAfter fetch:")
    cpu.show_cpu()
    cpu.memory.show_mem(show_zero=False, show_ins=True)

    cpu.decode_stage()
    print("\nAfter decode:")
    cpu.show_cpu()
    cpu.memory.show_mem(show_zero=False, show_ins=True)

    cpu.execute_stage()
    print("\nAfter execute:")
    cpu.show_cpu()
    cpu.memory.show_mem(show_zero=False, show_ins=True)

    cpu.memory_stage()
    print("\nAfter memory:")
    cpu.show_cpu()
    cpu.memory.show_mem(show_zero=False, show_ins=True)

    cpu.write_back_stage()
    print("\nAfter write back:")
    cpu.show_cpu()
    cpu.registers.show_regs_hex()
    cpu.memory.show_mem(show_zero=False, show_ins=True)

    cpu.update_PC()
    print("\nAfter update PC:")
    cpu.show_cpu()
    cpu.memory.show_mem(show_zero=False, show_ins=True)


def test_mrmovq():
    def get_ins_rrmovq(PC):
        return DataArb('0x2001')
    cpu = CPU(get_ins=get_ins_rrmovq)
    cpu.PC = 0
    cpu.fetch_stage()
    print("after fetch:")
    cpu.show_cpu()
    cpu.decode_stage()
    print("after decode:")
    cpu.show_cpu()
    cpu.execute_stage()
    print("after execute:")
    cpu.show_cpu()
    cpu.memory_stage()
    print("after memory:")
    cpu.show_cpu()
    cpu.write_back_stage()
    print("after write back:")
    cpu.show_cpu()
    cpu.update_PC()
    print("after update PC:")
    cpu.show_cpu()


def test_OPq():
    def get_ins_rrmovq(PC):
        return DataArb('0x2001')
    cpu = CPU(get_ins=get_ins_rrmovq)
    cpu.PC = 0
    cpu.fetch_stage()
    print("after fetch:")
    cpu.show_cpu()
    cpu.decode_stage()
    print("after decode:")
    cpu.show_cpu()
    cpu.execute_stage()
    print("after execute:")
    cpu.show_cpu()
    cpu.memory_stage()
    print("after memory:")
    cpu.show_cpu()
    cpu.write_back_stage()
    print("after write back:")
    cpu.show_cpu()
    cpu.update_PC()
    print("after update PC:")
    cpu.show_cpu()


def test_jXX():
    def get_ins_rrmovq(PC):
        return DataArb('0x2001')
    cpu = CPU(get_ins=get_ins_rrmovq)
    cpu.PC = 0
    cpu.fetch_stage()
    print("after fetch:")
    cpu.show_cpu()
    cpu.decode_stage()
    print("after decode:")
    cpu.show_cpu()
    cpu.execute_stage()
    print("after execute:")
    cpu.show_cpu()
    cpu.memory_stage()
    print("after memory:")
    cpu.show_cpu()
    cpu.write_back_stage()
    print("after write back:")
    cpu.show_cpu()
    cpu.update_PC()
    print("after update PC:")
    cpu.show_cpu()


def test_call():
    def get_ins_rrmovq(PC):
        return DataArb('0x2001')
    cpu = CPU(get_ins=get_ins_rrmovq)
    cpu.PC = 0
    cpu.fetch_stage()
    print("after fetch:")
    cpu.show_cpu()
    cpu.decode_stage()
    print("after decode:")
    cpu.show_cpu()
    cpu.execute_stage()
    print("after execute:")
    cpu.show_cpu()
    cpu.memory_stage()
    print("after memory:")
    cpu.show_cpu()
    cpu.write_back_stage()
    print("after write back:")
    cpu.show_cpu()
    cpu.update_PC()
    print("after update PC:")
    cpu.show_cpu()


def test_ret():
    def get_ins_rrmovq(PC):
        return DataArb('0x2001')
    cpu = CPU(get_ins=get_ins_rrmovq)
    cpu.PC = 0
    cpu.fetch_stage()
    print("after fetch:")
    cpu.show_cpu()
    cpu.decode_stage()
    print("after decode:")
    cpu.show_cpu()
    cpu.execute_stage()
    print("after execute:")
    cpu.show_cpu()
    cpu.memory_stage()
    print("after memory:")
    cpu.show_cpu()
    cpu.write_back_stage()
    print("after write back:")
    cpu.show_cpu()
    cpu.update_PC()
    print("after update PC:")
    cpu.show_cpu()


def test_pushq():
    def get_ins_rrmovq(PC):
        return DataArb('0x2001')
    cpu = CPU(get_ins=get_ins_rrmovq)
    cpu.PC = 0
    cpu.fetch_stage()
    print("after fetch:")
    cpu.show_cpu()
    cpu.decode_stage()
    print("after decode:")
    cpu.show_cpu()
    cpu.execute_stage()
    print("after execute:")
    cpu.show_cpu()
    cpu.memory_stage()
    print("after memory:")
    cpu.show_cpu()
    cpu.write_back_stage()
    print("after write back:")
    cpu.show_cpu()
    cpu.update_PC()
    print("after update PC:")
    cpu.show_cpu()


def test_popq():
    def get_ins_rrmovq(PC):
        return DataArb('0x2001')
    cpu = CPU(get_ins=get_ins_rrmovq)
    cpu.PC = 0
    cpu.fetch_stage()
    print("after fetch:")
    cpu.show_cpu()
    cpu.decode_stage()
    print("after decode:")
    cpu.show_cpu()
    cpu.execute_stage()
    print("after execute:")
    cpu.show_cpu()
    cpu.memory_stage()
    print("after memory:")
    cpu.show_cpu()
    cpu.write_back_stage()
    print("after write back:")
    cpu.show_cpu()
    cpu.update_PC()
    print("after update PC:")
    cpu.show_cpu()


if __name__ == '__main__':
    test_rmmovq()
