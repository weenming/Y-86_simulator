from hardware import *
from abstraction import *
from sequence import *
import error


class CPU():
    '''
    Abstraction level of the CPU, see components like memory, c.c.,
    ALU and regs as 'black boxes'
    Wires are, however, visible here. Therefore the data transmission
     should be explicitly modeled. Some complicated functions can be called
     from the module 'sequence'.
    '''

    def __init__(self, mem: Memory, get_ins=None, debug=False):
        # debug mode: print a lot of info, should not be used in test.py
        self.debug=debug
        self.ALU = ALU()
        self.cond_code = CondCode()
        self.stat = Stat()
        # need to read memory (for programs) from external file
        self.memory = mem
        self.registers = Registers(Word(mem.max_adr))
        # 'artificially' divide instruction men and run-time mem
        self.instruct_mem = InstructMem()
        self.get_ins = get_ins
        self.PC = Word(0)
        self._clear_tmp()
        if get_ins == None:  # default: get instructions from memory
            self.get_ins = self.memory.get_ins
        self.cycle_gen = self.cycle()
        self.cycle_gen.send(None)
        if self.debug:
            print('CPU init finished')
    

    def cycle(self):
        # when trying to run the cpu with an error stat code, raise error.
        is_cycle = yield ''
        stages = [self.fetch_stage, self.decode_stage, self.execute_stage, self.memory_stage,\
              self.write_back_stage, self.update_PC]
        while True:
            for stage in stages:
                try:
                    stage()
                    if not is_cycle:
                        is_cycle = yield ''
                except error.Halt as e:
                    self.icode, self.ifun = 0, 0
                    self.stat.set(2, self)
                    err_msg = e.err_msg
                except error.AddressError as e:
                    if self.debug:
                        print('address out of range!', e.err_msg)
                    self.stat.set(3, self)
                    err_msg = e.err_msg
                except error.InstructionError as e:
                    if self.debug:
                        print('instruction error:', e.err_msg)
                    self.stat.set(4, self)
                    err_msg = e.err_msg
                finally:
                    if not self.stat.is_ok():
                        if self.debug:
                            print('bad stat code, throwing error')
                        yield err_msg
            # cycle: yield after a whole cycle
            if is_cycle:
                is_cycle = yield ''


    def run(self, cycle=True):
        # if not cycle, execute step by step
        if self.stat.is_ok():
            err_msg = self.cycle_gen.send(cycle)
            return err_msg
        else:
            return f'This CPU has stopped, stat: {self.stat.val}'

    def fetch_stage(self):
        # Whether or not get valC
        ins = self.get_ins(self.PC)
        self.icode, self.ifun = self.instruct_mem.update(ins)
        # rA and rB are the ADDRESSES of the registers and they are INTs!!!
        self.rA, self.rB = self.instruct_mem.get_reg_address()
        # given the current instruction, calculate the next PC,
        # valP is INT!!!!
        self.valP = self.instruct_mem.calc_valP(self.PC)
        self.valC = self.instruct_mem.get_valC()
        return

    def decode_stage(self):
        r1, r2 = decode.select_read_reg_srcs(self)
        self.valA, self.valB = self.registers.read_2_ports(r1, r2)
        return

    def execute_stage(self):
        op1, op2, operator = execute.select_operation(self)
        # ALU computes cond code as well as valE
        self.valE, cc_info = self.ALU.op64(operator, op1, op2)
        if execute.do_update_cc(self):  # OPq or iaddq
            self.cond_code.set(cc_info)
        if execute.do_update_cnd(self):  # cmovq or jXX
            self.cnd = self.cond_code.is_condition(self.icode, self.ifun)
        return

    def memory_stage(self):
        write_dest_adr, write_val = memory.select_write(self)
        read_src_adr = memory.select_read(self)
        # memory adr is a Word, and so is write_val
        self.memory.write(write_dest_adr, write_val)
        self.valM = self.memory.read(read_src_adr)
        return

    def write_back_stage(self):
        reg_adr, val = write_back.select_write_back(self)
        self.registers.write(reg_adr, val)
        # MAY write back twice
        reg_adr, val = write_back.select_write_back_2nd(self)  # popq only
        self.registers.write(reg_adr, val)
        return

    def update_PC(self):
        # PC = valP or other values
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


    def show_cpu(self, show_values=False, show_regs=False):
        print('ins name:', self.instruct_mem.get_instruction_name())
        if show_values:
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

            print('valP:', self.valP.get_str_hex())
            print('rA:', self.rA)
            print('rB:', self.rB)

        print('PC:', self.PC.get_str_hex())

        if show_regs:
            self.registers.show_regs_hex(show_zero=True)
        else:
            print('\%rsp:', self.registers.show_rsp())
        self.cond_code.show()

    def get_cpu_vals(self):
        vals = [self.valA, self.valB, self.valC, self.valE, self.valM, self.valP, self.rA, self.rB]
        for val, i in zip(vals, list(range(len(vals)))):
            if val is not None and i < 6:
                vals[i] = val.get_str_hex()
            if i == 6:
                vals[i] = Word(val).get_str_hex()
        return {'valA':vals[0], 'valB':vals[1], 'valC':vals[2], 'valE':vals[3], 'valM':vals[4], 'valP': vals[5], 'rA':vals[6], 'rB':vals[7]}
