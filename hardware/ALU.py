import sys
sys.path.append("./")

from abstraction import *


class ALU():
    def __init__(self):
        return

    def op64(operator, operand1, operand2):
        cc_info = None

        if operator == '+':
            x1 = operand1.get_value_int10()
            x2 = operand2.get_value_int10()
            w = Word(x1 + x2)
        elif operator == '-':
            x1 = operand1.get_value_int10()
            x2 = operand2.get_value_int10()
            w = Word(x1 - x2)
        elif operator == '&':
            ls1 = operand1.get_bit_ls()
            ls2 = operand2.get_bit_ls()
            ls_res = []
            for b1, b2 in zip(ls1, ls2):
                if b1 and b2:
                    ls_res.append(1)
                else:
                    ls_res.append(0)
            w = Word(ls_res)
        elif operator == '|':
            pass

        assert w._check_validity()

        return w, cc_info
