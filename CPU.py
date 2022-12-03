from hardware import *
from abstraction import *
from sequence import *
import error
print('importing cpu')


class CPU():
    '''
    Abstraction level of the CPU, see components like memory, c.c.,
    ALU and regs as 'black boxes'
    Wires are, however, visible here. Therefore the data transmission
     should be explicitly modeled. Some complicated functions can be called
     from the module 'sequence'.
    '''

    def __init__(self, mem: Memory, get_ins=None):
        self.ALU = ALU()
        self.cond_code = CondCode()
        self.stat = Stat()
        # need to read memory (for programs) from external file
        self.memory = mem
        self.registers = Registers(Word(mem.max_adr))
        # 'artificially' divide instruction men and run-time mem
        self.instruct_mem = InstructMem()
        self.get_ins = get_ins
        self.PC = 0
        self._clear_tmp()
        if get_ins == None:  # default: get instructions from memory
            self.get_ins = self.memory.get_ins

    def cycle(self):
        try:
            self.fetch_stage()
            self.decode_stage()
            self.execute_stage()
            self.memory_stage()
            self.write_back_stage()
            self.update_PC()
        except error.Halt:
            self.stat.set(2)
        except error.AddressError:
            self.stat.set(3)
        except error.InstructionError:
            self.stat.set(4)

    def fetch_stage(self):
        # Whether or not get valC
        ins = self.get_ins(self.PC)
        self.icode, self.ifun = self.instruct_mem.update(ins)
        if self.icode == 0:
            raise error.Halt
        # get icode and ifun internally
        # self.icode, self.ifun = self.instruct_mem.fetch()

        # rA and rB are the ADDRESSES of the registers and they are INTs!!!
        self.rA, self.rB = self.instruct_mem.get_reg_address()
        # given the current instruction, calculate the next PC,
        # valP is INT!!!!
        self.valP = self.PC + self.instruct_mem.calc_valP()

        self.valC = self.instruct_mem.get_valC()
        return

    def decode_stage(self):
        r1, r2 = decode.select_read_reg_srcs(self)

        self.valA = self.registers.read(r1)
        self.valB = self.registers.read(r2)
        return

    def execute_stage(self):
        op1, op2, operator = execute.select_operation(self)

        self.valE, cc_info = self.ALU.op64(operator, op1, op2)
        if execute.do_update_cc(self):  # OPq
            self.cond_code.set(cc_info)
        if execute.do_update_cnd(self):  # cmovq or jXX
            self.cnd = self.cond_code.is_condition(self.icode, self.ifun)
        return

    def memory_stage(self):
        write_dest_adr, write_val = memory.select_write(self)
        read_src_adr = memory.select_read(self)
        # memory adr is a Word, and so is val
        self.memory.write(write_dest_adr, write_val)
        self.valM = self.memory.read(read_src_adr)
        return

    def write_back_stage(self):
        reg_adr, val = write_back.select_write_back(self)
        self.registers.write(reg_adr, val)

        reg_adr, val = write_back.select_write_back_2nd(self)  # popq only
        self.registers.write(reg_adr, val)
        return

    def update_PC(self):
        # PC = ...
        val = update_PC.select_PC_val(self)
        self.PC = val
        return

    def _clear_tmp(self):
        self.valA = self.valB = self.valC = None
        self.rA = self.rB = None
        self.valE = self.valM = None
        self.valP = None
        self.valM = None
        # ...

    def show_cpu(self):
        print('ins name:', self.instruct_mem.get_instruction_name())
        if self.valA is not None:
            print('valA:', self.valA.get_str_hex())
        else:
            print('valA: None')

        if self.valB is not None:
            print('valB:', self.valB.get_str_hex())
        else:
            print('valB: None')

        if self.valC is not None:
            print('valC:', self.valC.get_str_hex())
        else:
            print('valC: None')

        if self.valE is not None:
            print('valE:', self.valE.get_str_hex())
        else:
            print('valE: None')

        if self.valM is not None:
            print('valM:', self.valM.get_str_hex())
        else:
            print('valM: None')

        print('valP:', self.valP)
        print('rA:', self.rA)
        print('rB:', self.rB)
        print('PC:', self.PC)
        self.cond_code.show()
