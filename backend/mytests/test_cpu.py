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
    extern_memory = Memory([Byte('0xff')])

    def get_ins_rrmovq(PC):
        return extern_memory.get_ins(PC)
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
    # mem.write(Word(0x100), Word(0xabcdef))
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
    mem = Memory([Byte(0x50), Byte(0x01), Byte(
        0x20), Byte(0x00), Byte(0x0), Byte(0x00), Byte(0x0), Byte(0x0), Byte(0x0), Byte(0x0)])  # D = 0x20
    cpu = CPU(mem, get_ins=None)
    cpu.PC = 0
    cpu.memory.write(Word(0x50), Word(0xabcdef))
    # adr to write += 0x30, memory adr to access is 0x50 now
    cpu.registers.write(1, Word(0x30))

    cpu.memory.show_mem(show_ins=True, show_zero=False)
    run(cpu)
    cpu.registers.show_regs_hex()
    cpu.show_cpu()

    try:
        print('begin testing mem range')
        mem = Memory([Byte(0x50), Byte(0x01), Byte(
            0xf0), Byte(0x00), Byte(0x0), Byte(0x00), Byte(0x0), Byte(0x0), Byte(0x0), Byte(0x0)])  # D = 0x20
        cpu = CPU(mem, get_ins=None)
        cpu.PC = 0
        cpu.memory.write(Word(0x100), Word(0xabcdef))
        cpu.memory.show_mem(show_ins=True, show_zero=False)
        run(cpu)
        cpu.registers.show_regs_hex()
        cpu.show_cpu()
    except error.AddressError:
        print('mem error?')


def test_OPq():
    mem = Memory([Byte('0x61'), Byte('0x33')])
    cpu = CPU(mem, get_ins=None)

    cpu.registers.write(2, Word('0x2'))
    cpu.registers.write(3, Word('0x10'))

    cpu.PC = 0
    cpu.fetch_stage()
    print("after fetch:")
    cpu.show_cpu()
    cpu.registers.show_regs_hex()

    cpu.decode_stage()
    print("after decode:")
    cpu.show_cpu()
    cpu.registers.show_regs_hex()

    cpu.execute_stage()
    print("after execute:")
    cpu.show_cpu()
    cpu.registers.show_regs_hex()

    cpu.memory_stage()
    print("after memory:")
    cpu.show_cpu()
    cpu.registers.show_regs_hex()

    cpu.write_back_stage()
    print("after write back:")
    cpu.show_cpu()
    cpu.registers.show_regs_hex()

    cpu.update_PC()
    print("after update PC:")
    cpu.show_cpu()
    cpu.registers.show_regs_hex()


def test_OOOOOOOP():
    mem = Memory([Byte('0x63'), Byte('0x32')])
    cpu = CPU(mem, get_ins=None)

    cpu.registers.write(2, Word('0xff00ff'))
    cpu.registers.write(3, Word('0xf0f0f0'))

    cpu.PC = 0
    run(cpu)

    cpu.show_cpu()
    cpu.registers.show_regs_hex()


def test_jXX():
    mem = Memory([Byte(0x70), Byte(0x0a), Byte(
        0x00), Byte(0x00), Byte(0x00), Byte(0x00), Byte(0x00), Byte(0x00), Byte(0x00), Byte(0x0)])  # D = 0x20
    cpu = CPU(mem, get_ins=None)
    cpu.PC = 0
    # cpu.memory.write(Word(0x50), Word(0xabcdef))
    # adr to write += 0x30, memory adr to access is 0x50 now
    # cpu.registers.write(1, Word(0x30))

    cpu.memory.show_mem(show_ins=True, show_zero=False)
    run(cpu)
    # cpu.registers.show_regs_hex()
    cpu.show_cpu(show_values=True)
    try:
        run(cpu)
    except error.Halt:
        print('Halt!')

def test_jne():
    mem = Memory([Byte(0x74), Byte(0x10)]+ [Byte(
        0x00)] * 7 + [Byte(0xff)] * 7 + [Byte(0x00)] + [Byte(0xff)] * 0x10)  # D = 0x20
    cpu = CPU(mem, get_ins=None)
    cpu.PC = 0
    # cpu.memory.write(Word(0x50), Word(0xabcdef))
    # adr to write += 0x30, memory adr to access is 0x50 now
    # cpu.registers.write(1, Word(0x30))

    cpu.memory.show_mem(show_ins=True, show_zero=False)
    cpu.cond_code.set({'ZF': 0, 'SF': None, 'OF': None})
    cpu.cycle()
    # cpu.registers.show_regs_hex()
    cpu.show_cpu(show_values=True)
    print('\n')
    
    cpu.cycle()
    cpu.show_cpu()
    return

def test_jle():
    return

def test_jge():
    return


def test_call():
    mem = Memory([Byte(0x00)] * 0x10 + [Byte(0x80)] +
                 [Byte(0x10)] + [Byte(0x00)] * 7)
    cpu = CPU(mem=mem)
    # print(cpu.memory.max_adr)
    cpu.PC = 0x10
    for _ in range(3):
        cpu.cycle()
        cpu.show_cpu(show_regs=True, show_values=True)
        cpu.memory.show_mem(show_ins=True, show_zero=False)
        print('\n')


def test_ret():
    '''
    the instructions are:
    0x10    call 0x1e 
    0x19    halt
    0x1a    invalid instruction
    0x1b    invalid instruction
    0x1c    invalid instruction
    0x1d    ret

    '''
    mem = Memory( [Byte(0xff)] * 0x10 + [Byte(0x80)] +
                 [Byte(0x1d)] + [Byte(0x00)] * 7 + [Byte(0x00)] + [Byte(0xff)] * 0x3  + [Byte(0x90)])
    cpu = CPU(mem=mem)
    # print(cpu.memory.max_adr)
    cpu.PC = 0x10
    print('call')
    cpu.cycle()
    cpu.show_cpu(show_regs=True, show_values=True)
    cpu.memory.show_mem(show_ins=True, show_zero=True)
    print('\n')
    print('ret')
    cpu.cycle()
    cpu.show_cpu(show_regs=True, show_values=True)
    cpu.memory.show_mem(show_ins=True, show_zero=True)
    print('\n')

    while True:
        if cpu.cycle():
            cpu.show_cpu(show_regs=True, show_values=True)
            print('\n')
        else:
            print('rsp (should be 0x100):', cpu.registers.show_rsp())
            print('rip (should be 0x19):', cpu.PC)
            print('Halt, correct!')
            break

def test_pushq():
    mem = Memory([Byte(0x00)] * 0x10 + [Byte(0xa0)] +
                 [Byte(0x0f)] + [Byte(0xff)] * 7)
    cpu = CPU(mem=mem)
    print('rsp:', cpu.registers.show_rsp())

    # print(cpu.memory.max_adr)
    cpu.registers.write(0, Word(0xabcdef))
    cpu.PC = 0x10
    cpu.cycle()
    cpu.show_cpu(show_regs=True, show_values=True)
    cpu.memory.show_mem(show_ins=True, show_zero=False)
    print('rsp:', cpu.registers.show_rsp())
    print('\n')
    

def test_popq():
    mem = Memory([Byte(0x00)] * 0x10 + [Byte(0xa0)] +
                 [Byte(0x0f)] + [Byte(0xb0), Byte(0x1f)])
    cpu = CPU(mem=mem)

    print('rsp:', cpu.registers.show_rsp())
    cpu.registers.write(0, Word(0xabcdef))
    cpu.PC = 0x10

    print('push:')
    cpu.cycle()
    print('pop:')
    cpu.cycle()

    cpu.show_cpu(show_regs=True, show_values=True)
    cpu.memory.show_mem(show_ins=True, show_zero=False)
    print('rsp:', cpu.registers.show_rsp())
    print('\n')

    print('halt:')
    cpu.cycle()


if __name__ == '__main__':
    test_jne()
