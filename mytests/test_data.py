'''
This python file needs to include system path './../'
in order to import packages to test
'''
# Open this project in VS Code from the root dir
# when run using the run button, VS Code runs this file from the root dir,
# and thus the cur path is "Y-86_Simulator/".
import sys
sys.path.append("./")

from hardware import *
from abstraction import *


def test_data():
    # init with str
    data = DataArb('01011010001')
    data.print_bit_ls()
    print(data.get_value_int10())

    # init with str, hex
    data = DataArb('0x2d1')
    data.print_bit_ls()
    print(data.get_value_int10())
    print(data.get_str_hex())

    # init with int
    data = DataArb(721)
    data.print_bit_ls()
    print(data.get_value_int10())

    # init with int ls
    data = DataArb([0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1])
    data.print_bit_ls()
    print(data.get_value_int10())
    print(data.get_str_hex())


def test_byte():
    # init with str
    data = Byte('01011010')
    data.print_bit_ls()
    print(data.get_value_int10())

    # init with str, hex
    data = Byte('0x5a')
    data.print_bit_ls()
    print(data.get_value_int10())
    print(data.get_str_hex())

    # init with int
    data = Byte(90)
    data.print_bit_ls()
    print(data.get_value_int10())

    # init with int ls
    data = Byte([0, 1, 0, 1, 1, 0, 1, 0])
    data.print_bit_ls()
    print(data.get_value_int10())

    print("init with class Byte")
    data = DataArb('01011010001')
    w = Byte(data.get_nth_byte(0))
    print(w.get_bit_ls())
    print(w.get_value_int10())

    print("init with class DataArb")
    data = DataArb('0101101')
    b = Byte(data)
    print(b.get_bit_ls())
    print(b.get_value_int10())

    print("cannot append byte to byte")
    b = Byte('01001010')
    print(b.append_byte(b))


def test_word():
    # init with str
    data = Word('01011010' * 8)
    data.print_bit_ls()
    print(data.get_value_int10())

    print("init with int")
    data = Word(90)
    data.print_bit_ls()
    print(data.get_value_int10())

    print("init with int ls")
    data = Word([0, 1, 0, 1, 1, 0, 1, 0] * 8)
    data.print_bit_ls()
    print(data.get_value_int10())


def test_ragged():
    data_arb = DataArb('0110100101')
    print(data_arb.get_nth_byte(0).get_value_int10())


hello()

if __name__ == '__main__':
    test_data()
    test_byte()
    test_word()
    test_ragged()
    mem = memory()
