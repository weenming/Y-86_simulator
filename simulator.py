from CPU import *
from abstraction import *
import error
import re
import sys
import fileinput
import json

def get_ins(fname):
    with open(fname, 'r') as f:
        text = f.read()
    return text

def get_ins_from_stdin():
    text = ''
    with fileinput.input() as f:
        for line in f:
            text += line
            text += "\n"
            # # stop reading from stdin when typing an empty line
            # if line == '\n':
            #     break
    return text

def get_ins_test():
    return  '0x030:                      | stack:                # stack'


def str_to_byte_ls(input_str: str):
    str_lines = input_str.splitlines(False)
    adr_of_ins = []
    ins = []
    for ins_str in str_lines:
        try:
            this_adr = re.match("^0x(.*?):\s", ins_str).group(1)
            this_ins = re.match("^0x.*?:\s*(.*)\s*\|", ins_str).group(1).strip()
        except AttributeError:
            continue
        
        if this_ins is not None and this_ins != '':
            adr_of_ins.append(int(this_adr, base=16))
            ins.append(this_ins)
    return adr_of_ins, ins


def build_json_dic(cpu:CPU):
    cpu_info = {'PC':cpu.PC, 'REG':cpu.registers.get_reg_dict(), 'CC': cpu.cond_code.get_CC_dict()\
        , 'STAT': cpu.stat.val, 'MEM': cpu.memory.get_mem_dict()} # current state of the cpu stored in a python dict
    return cpu_info

def run_cpu(cpu:CPU, cycle, debug=False):
    '''
    Runs the cpu, a whole cycle or a single step (stage?) specified by user 
    
    @param  cycle: boolean, if False, run a single stage
    @return        a dictionary formatted as the project instruction
                   an error message containing descritions of the specific error happending
                      if there's no error, this would be an empty string
                   a dictionary containing tmp values of the CPU, or the signals in the wires I think
                      may contain None variables
    '''
    # empty msg: all good
    err_msg = ''
    try:
        cpu.run(cycle)
        # update to the state before termination
    except error.Halt as e:
        cpu.try_cycle()
        ins = cpu.get_ins(cpu.PC)
        cpu.icode, cpu.ifun = cpu.instruct_mem.update(ins)
        cpu.stat.set(2, cpu)
        err_msg = e.err_msg
    except error.AddressError as e:
        if cpu.debug:
            print('address out of range!')
        cpu.try_cycle()
        cpu.stat.set(3, cpu)
        err_msg = e.err_msg
    except error.InstructionError as e:
        if cpu.debug:
            print('instruction error:')
        cpu.stat.set(4, cpu)
        err_msg = e.err_msg
    finally:
        if not cpu.stat.is_ok():
            if cpu.debug:
                print('bad stat code, throwing error')
    # TODO: value A and so on
    return build_json_dic(cpu), err_msg, cpu.get_cpu_vals()

def init_cpu(ins:str, debug=False):
    '''
    Call this function to initialize the cpu
    
    @param  ins:    a string containing instructions
            debug:  a boolean specifying whether to print info for debugging
    @return cpu, an instance of the CPU class, initialized with memory containing the instrcutions passed in
    '''
    adr_ls, ins_str_ls = str_to_byte_ls(ins)
    byte_ls = []
    for ins_str, adr in zip(ins_str_ls, adr_ls):
        assert len(byte_ls) <= adr
        # The instructions are not necessarily 'tightly' arranged in memory.
        # So we need to check and shift the adr when initiallizing it.
        while len(byte_ls) < adr:
            byte_ls.append(Byte(0x0))
        for i in range(0, len(ins_str), 2):
            byte_ls.append(Byte('0x' + ins_str[i: i + 2]))
    if debug:
        print([byte.get_str_hex() for byte in byte_ls])
        print(len(byte_ls))
    mem = Memory(byte_ls)
    if debug:
        print(mem.mem_bytes[0x37].get_str_hex())
    cpu = CPU(mem)
    return cpu

if __name__ == '__main__':

    cpu = init_cpu(get_ins_from_stdin(), debug=False)
    '''
    in machine code the value is already stored by little endian....
    val_byte_ls = []
    for i in range(val_start, len(ins_str), 2):
        val_byte_ls.append(Byte('0x' + ins_str[i: i + 2]))
    val_byte_ls.reverse()
    '''
    cpu_info_dict_ls = []

    while True:
        dic, err_msg = run_cpu(cpu, True)
        # print('error message:', err_msg)
        # cpu.show_cpu(show_regs=True)
        # cpu.memory.show_mem()
        # print('\n')
        cpu_info_dict_ls.append(build_json_dic(cpu))
        if err_msg != '':
            break
        
    # output the json file to stdout
    json.dump(cpu_info_dict_ls, sys.stdout)
    

