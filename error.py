class Error(Exception):
    def __init__(self, msg): 
        super().__init__() 
        self.err_msg = msg


class AddressError(Error):
    pass


class Halt(Error):
    def __init__(self): 
        super().__init__('Halt!') 


class InstructionError(Error):
    pass
