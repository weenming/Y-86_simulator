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
    rsp_min = cpu.memory.rsp_min
    dic = cpu.build_json_dic(format)
    dic.update({"rsp_min":rsp_min})
    return dic, err_msg, cpu.get_cpu_vals()

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
    mem = Memory(byte_ls)
    cpu = CPU(mem)
    
    rsp_min = cpu.memory.rsp_min
    dic = cpu.build_json_dic('str')
    dic.update({"rsp_min":rsp_min})
    return cpu, dic, '', cpu.get_cpu_vals()

def last_step(cpu:CPU):
    # load last cycle!
    return cpu.last_cycle()

if __name__ == '__main__':
    cpu, _, _ = init_cpu(get_ins_from_stdin(), debug=False)
    '''
    In machine code the value is already stored by little endian....
    val_byte_ls = []
    for i in range(val_start, len(ins_str), 2):
        val_byte_ls.append(Byte('0x' + ins_str[i: i + 2]))
    val_byte_ls.reverse()
    '''
    cpu_info_dict_ls = []

    while True:
        dic, err_msg, _ = run_cpu(cpu, True)
        cpu_info_dict_ls.append(cpu.build_json_dic('int'))
        # Determine termination by the returned err_msg
        # In fact, the instance of CPU will not run after an error occurs.
        # see CPU.run for details
        if err_msg != '':
            break
        
    # output the json file to stdout
    json.dump(cpu_info_dict_ls, sys.stdout)
    

