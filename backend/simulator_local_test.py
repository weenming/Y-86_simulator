import sys
sys.path.append('./backend')
from CPU import *
from abstraction import *
import error
import re
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


def run_cpu(cpu:CPU, cycle, debug=False, format='str'):
    '''
    Runs the cpu, a whole cycle or a single step (stage?) specified by user 
    
    @param  cycle: boolean, if False, run a single stage
    @return        a dictionary formatted as the project instruction
                   an error message containing descriptions of the specific error happening
                      if there's no error, this would be an empty string
                   a dictionary containing tmp values of the CPU, or the signals in the wires I think
                      may contain None variables
    '''
    # empty msg: all good
    err_msg = cpu.run(cycle)
    return cpu.build_json_dic(format), err_msg, cpu.get_cpu_vals()

def init_cpu(ins:str, debug=False):
    '''
    Call this function to initialize the cpu
    
    @param  ins:    a string containing instructions
            debug:  a boolean specifying whether to print info for debugging
    @return cpu, an instance of the CPU class, initialized with memory containing the instructions passed in
    '''
    adr_ls, ins_str_ls = str_to_byte_ls(ins)
    byte_ls = []
    for ins_str, adr in zip(ins_str_ls, adr_ls):
        assert len(byte_ls) <= adr
        # The instructions are not necessarily 'tightly' arranged in memory.
        # So we need to check and shift the adr when initializing it.
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

def last_step(cpu:CPU):
    # load last cycle!
    return cpu.last_cycle()

if __name__ == '__main__':
    cpu = init_cpu(get_ins('./test/asumi.yo'), debug=False)
    '''
    in machine code the value is already stored by little endian....
    val_byte_ls = []
    for i in range(val_start, len(ins_str), 2):
        val_byte_ls.append(Byte('0x' + ins_str[i: i + 2]))
    val_byte_ls.reverse()
    '''
    cpu_info_dict_ls = []

    while True:
        execute_msg = input('run for next cycle; prev for prev cycle')
        if execute_msg == 'run':
            dic, err_msg, _ = run_cpu(cpu, True)
            print('error message:', err_msg)
            cpu.show_cpu(show_regs=True)
            print(cpu.get_cpu_vals())
            cpu.memory.show_mem()
            print('\n')
            cpu_info_dict_ls.append(cpu.build_json_dic('int'))
            if err_msg != '':
                print(err_msg)
        elif execute_msg == 'prev':
            cpu_last = last_step(cpu)
            if not cpu_last:
                print('empty stack!')
            else:
                print('prev step, PC:', cpu.PC.get_str_hex())
        elif execute_msg == 'run to end':
            err_msg = ''
            while err_msg == '':
                _, err_msg, _ = run_cpu(cpu, True)
        else:
            print('bad input')
    # output the json file to stdout
    json.dump(cpu_info_dict_ls, sys.stdout)
    

