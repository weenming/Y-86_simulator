class Error(Exception):
    pass


class AddressError(Error):
    print('address out of range!')
    pass


class Halt(Error):
    pass


class InstructionError(Error):
    pass
