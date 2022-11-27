from hardware import *
from abstraction import *
import sequence.fetch


def get_instruction():
    '''
    get instruction code after processing a given file
    returns a DataArb type instance
    '''
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
        # 'artificially' divide instruction men and run-time mem
        self.instruct_mem = InstructMem()

        self.PC = 0

    def fetch_stage(self):
        # Whether or not get valC
        self.instruct_mem.update(get_instruction(self.PC))
        # get icode and ifun internally
        # self.icode, self.ifun = self.instruct_mem.fetch()

        # rA and rB are the ADDRESSES of the registers
        self.rA, self.rB = self.instruct_mem.get_reg_address()
        # given the current instruction, calculate the next PC
        self.valP = self.PC + self.instruct_mem.calc_valP()

        self.valC = self.instruct_mem.get_valC()
        self.name = self.instruct_mem.get_instruction_name()
        return

    def decode_stage(self):
        # if some instructions
        self.valA = self.registers.read(self.rA)
        # if some other instructions
        self.valB = self.registers.read(self.rB)

        return

    def execute_stage(self):
        op1, op2 = sequence.execute.select_operands(
            self.instruct_mem, self.valA, self.valB, self.valC)
        operator = sequence.execute.select_operator(self.instruct_mem)
        self.valE, cc_info = self.ALU.op64(operator, op1, op2)
        if self.instruct_mem.do_update_cc():
            self.cond_code.set(cc_info)

        return

    def memory_stage(self):
        write_dest = sequence.memory.select_write_dest(self.instruct_mem, )
        write_val = sequence.memory.select_write_val(self.instruct_mem)
        read_src = sequence.memory.select_write_val(self.instruct_mem)
        self.memory.write(self.valE, self.valA)
        self.valM = self.memory.read(self.valE)
        return

    def write_back_stage(self):
        if self.name in ['cmovXX', 'jXX']:
            self.cnd = self.instruct_mem.get_cnd(self.cond_code)
        if self.name != 'jXX' or self.cnd == 1:
            self.registers.write(self.valE, self.rB)
        self.registers.write(self.valM, self.rA)
        return

    def update_PC(self):
        # PC = ...
        if self.name == 'jXX':
            if self.cnd:
                self.PC = self.valC
            else:
                self.PC = self.valP
        elif self.name == 'call':
            self.PC = self.valC
        elif self.name == 'ret':
            self.PC = self.valM
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
