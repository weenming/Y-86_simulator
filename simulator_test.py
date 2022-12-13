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
    @return        a json file formatted as the project instruction
    '''
    cpu.run(cycle)
    return build_json_dic(cpu)

def init_cpu(ins:str, debug=False):
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

    cpu = init_cpu(get_ins('./test/prog10.yo'), debug=True)
    '''
    in machine code the value is already stored by little endian....
    val_byte_ls = []
    for i in range(val_start, len(ins_str), 2):
        val_byte_ls.append(Byte('0x' + ins_str[i: i + 2]))
    val_byte_ls.reverse()
    '''
    cpu_info_dict_ls = []

    while True:
        ok = cpu.run(cycle=True)
        cpu.show_cpu(show_regs=True)
        cpu.memory.show_mem()
        print('\n')
        cpu_info_dict_ls.append(build_json_dic(cpu))
        if not ok:
            break
        
    # output the json file to stdout
    json.dump(cpu_info_dict_ls, sys.stdout)
    

