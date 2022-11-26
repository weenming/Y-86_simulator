from hardware import *
from abstraction import *
import sequence.fetch


def get_instruction():
    '''get instruction code after processing a given file'''
    return


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
        self.cond_code = CondCode()
        self.memory = Memory()
        self.registers = Registers()
        self.instruct_mem = InstructMem()

        self.PC = 0

    def fetch_stage(self):
        # Whether or not get valC
        self.instruct_mem.update(get_instruction(self.PC))
        self.icode, self.ifun = self.instruct_mem.fetch()
        # rA and rB are the ADDRESSES of the registers
        self.rA, self.rB = self.instruct_mem.get_reg_add()
        # given the current instruction, calculate the next PC
        self.valP = self.instruct_mem.calc_valP()

        if self.instruct_mem.do_get_valC():
            self.valC = self.memory.get_valC()
        return

    def decode_stage(self):
        # if some instructions
        self.valA = self.registers.read(self.rA)
        # if some other instructions
        self.valB = self.registers.read(self.rB)

        return

    def execute_stage(self):
        op1, op2 = sequence.execute.select_operands(
            self.icode, self.ifun, self.valA, self.valB, self.valC)
        operator = sequence.execute.select_operator(self.icode, self.ifun)
        self.valE, cc_info = self.ALU.op64(operator, op1, op2)
        self.cond_code.set(cc_info)

        return

    def memory_stage(self):
        self.memory.write(self.valE, self.valA)
        self.valM = self.memory.read(self.valE)
        return

    def write_back_stage(self):
        self.registers.write(self.valM, self.rA)
        return

    def update_PC(self):
        # PC = ...
        if self.cnd is not None:
            if self.cnd:
                self.PC = self.valC
            else:
                self.PC = self.valP
        return

    def clear_tmp(self):
        self.valA = self.valB = self.valC = None
        self.rA = self.rB = None
        self.valE = self.valF = None
        self.valP = None
        self.valM = None
        # ...
