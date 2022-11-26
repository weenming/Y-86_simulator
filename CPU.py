from hardware import *
from abstraction import *
import sequence.fetch


class CPU():
    '''
    Abstraction level of the CPU, see components like memory, c.c.,
    ALU and regs as 'black boxes'
    Wires are, however, visible here. Therefore the data transmission
     should be explicitly modeled. Some complicated functions can be called 
     from the module 'sequence'.
    '''

    def __init__(self):
        self.ALU = ALU()
        self.clock = clock()
        self.cond_code = cond_code()
        self.memory = memory()
        self.registers = registers()
        self.instruct_mem = instruct_mem()

    def fetch_stage():
        return

    def decode_stage():
        return

    def execute_stage():
        return

    def memory_stage():
        return

    def write_back_stage():
        return

    def update_PC():
        return
