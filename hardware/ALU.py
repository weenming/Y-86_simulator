import sys
sys.path.append("./")

from abstraction import *


class ALU():
    def __init__(self):
        return

    def op64(self, operator, operand1, operand2):
        cc_info = None
        if operator is None:
            return None, None
        if operator == '+':
            x1 = operand1.get_signed_value_int10()
            x2 = operand2.get_signed_value_int10()
            w = Word(x1 + x2)
            cc_info = self._get_cc_info_alg(operand1, operand2, w)
        elif operator == '-':
            x1 = operand1.get_signed_value_int10()
            x2 = operand2.get_signed_value_int10()
            w = Word(x1 - x2)
            cc_info = self._get_cc_info_alg(operand1, operand2, w)
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
            cc_info = self._get_cc_info_log(operand1, operand2, w)
        elif operator == '^':
            ls1 = operand1.get_bit_ls()
            ls2 = operand2.get_bit_ls()
            ls_res = []
            for b1, b2 in zip(ls1, ls2):
                if (b1 and b2) or (not b1 and not b2):
                    ls_res.append(0)
                else:
                    ls_res.append(1)
            w = Word(ls_res)
            cc_info = self._get_cc_info_log(operand1, operand2, w)

        assert w._check_validity()

        return w, cc_info

    def _get_cc_info_alg(self, a: Word, b: Word, t: Word):
        # print(a.neg, b.neg, t.neg)
        info = {}
        if t.is_zero():
            info['ZF'] = 1
        else:
            info['ZF'] = 0
        if t.neg:
            info['SF'] = 1
        else:
            info['SF'] = 0
        if (t.neg != a.neg) and (a.neg == b.neg):
            info['OF'] = 1
        else:
            info['OF'] = 0
        return info

    def _get_cc_info_log(self, a: Word, b: Word, t: Word):
        info = {}
        if t.is_zero():
            info['ZF'] = 1
        else:
            info['ZF'] = 0
        if t.neg:
            info['SF'] = 1
        else:
            info['SF'] = 0
        info['OF'] = 0
        return info
