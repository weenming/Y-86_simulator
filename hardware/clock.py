

class CondCode:
    def __init__(self):
        # initialize conditional codes
        # self.ZF =
        # self.SF =
        # self.OF =
        return

    def set(self, cc_info):
        if cc_info is None:
            return
        self.ZF = cc_info['ZF']
        self.SF = cc_info['SF']
        self.OF = cc_info['OF']
        return

    def eval():
        return


class Stat():
    def __init__(self):
        return
