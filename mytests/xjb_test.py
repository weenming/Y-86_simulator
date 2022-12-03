import sys
sys.path.append("./")
from CPU import *
from abstraction import *

def run(cpu):
    cpu.fetch_stage()
    cpu.decode_stage()
    cpu.execute_stage()
    cpu.memory_stage()
    cpu.write_back_stage()
    cpu.update_PC()

def test_xjb():
    mem = Memory([Byte(0x60), Byte(0x01)])
    cpu = CPU(mem, get_ins=None)

    cpu.registers.write(0, Word(0x8000000000000000))
    cpu.registers.write(1, Word(0x8000000000000000))

    cpu.PC = 0
    run(cpu)

    cpu.show_cpu()
    cpu.registers.show_regs_hex()

if __name__ == '__main__':
    test_xjb()
