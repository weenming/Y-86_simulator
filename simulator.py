from CPU import *
from abstraction import *
import error
import re
import json

def get_ins():
    with open('./test/prog1.yo', 'r') as f:
        text = f.read()
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




if __name__ == '__main__':
    adr_ls, ins_str_ls = str_to_byte_ls(get_ins())
    byte_ls = []
    for ins_str, adr in zip(ins_str_ls, adr_ls):
        assert len(byte_ls) <= adr
        # The instructions are not necessarily 'tightly' arranged in memory.
        # So we need to check and shift the adr when initiallizing it.
        while len(byte_ls) < adr:
            byte_ls.append(Byte(0x0))
        for i in range(0, len(ins_str), 2):
            byte_ls.append(Byte('0x' + ins_str[i: i + 2]))

    '''
    in machine code the value is already stored by little endian....
    val_byte_ls = []
    for i in range(val_start, len(ins_str), 2):
        val_byte_ls.append(Byte('0x' + ins_str[i: i + 2]))
    val_byte_ls.reverse()
    '''

    print([byte.get_str_hex() for byte in byte_ls])
    print(len(byte_ls))
    mem = Memory(byte_ls)
    print(mem.mem_bytes[0x37].get_str_hex())
    cpu = CPU(mem)
    cpu_info_dict_ls = []

    while True:
        try:
            cpu.run(cycle=True)
            cpu.show_cpu(show_regs=True)
            cpu.memory.show_mem()
            print('\n')
            cpu_info_dict_ls.append(build_json_dic(cpu))
        except error.Error:
            break

    with open('./out.json', 'w') as fw:
        json.dump(cpu_info_dict_ls, fw)
    

