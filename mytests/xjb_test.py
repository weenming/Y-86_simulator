import sys
sys.path.append("./")
from CPU import *
from abstraction import *

a = Byte('0x60')
a.print_bit_ls()

b = Byte(0x50)
b.print_bit_ls()

a = [1, 2]
b = [2, 3]
print(a+b)
