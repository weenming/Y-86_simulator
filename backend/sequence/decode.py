import sys
sys.path.append("./")


def select_read_reg_srcs(cpu):
    rsp_adr = cpu.registers.get_rsp_adr()
    null_adr = cpu.registers.get_null_adr()
    if cpu.icode == 0:
        assert 0, 'bad icode: halt should have been dealt with earlier'
    elif cpu.icode in [1, 7]:  # nop or jXX
        return null_adr, null_adr
    elif cpu.icode in [2, 3, 4, 5, 6, 12]:
        # in fact some of these instructions, like
        # rrmovq, does not read both valA and valB,
        # but there should be no problem because later selections
        # will prevent writing back to wrong regs
        return cpu.rA, cpu.rB
    elif cpu.icode == 10:  # pushq
        return cpu.rA, rsp_adr
    elif cpu.icode in [9, 11]:  # popq, ret
        return rsp_adr, rsp_adr
    elif cpu.icode == 8:  # call
        return null_adr, rsp_adr
    else:
        assert 0, 'bad icode'
