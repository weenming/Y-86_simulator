'''
This python file needs to include system path './../' 
in order to import packages to test
'''
import sys
sys.path.append('./../')


from hardware import *
from abstraction import *


def test_data():
    # init with str
    data = DataArb('01011010001')
    data.print_val_ls()
    print(data.get_value_int10())

    # init with int
    data = DataArb(721)
    data.print_val_ls()
    print(data.get_value_int10())

    # init with str ls
    data = DataArb(['0', '1', '0', '1', '1', '0', '1', '0', '0', '0', '1'])
    data.print_val_ls()
    print(data.get_value_int10())

    # init with int ls
    data = DataArb([0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1])
    data.print_val_ls()
    print(data.get_value_int10())


def test_byte():
    # init with str
    data = Byte('01011010')
    data.print_val_ls()
    print(data.get_value_int10())

    # init with int
    data = Byte(90)
    data.print_val_ls()
    print(data.get_value_int10())

    # init with str ls
    data = Byte(['0', '1', '0', '1', '1', '0', '1', '0'])
    data.print_val_ls()
    print(data.get_value_int10())

    # init with int ls
    data = Byte([0, 1, 0, 1, 1, 0, 1, 0])
    data.print_val_ls()
    print(data.get_value_int10())


def test_word():
    # init with str
    data = Word('01011010' * 8)
    data.print_val_ls()
    print(data.get_value_int10())

    # init with int
    data = Word(90)
    data.print_val_ls()
    print(data.get_value_int10())

    # init with str ls
    data = Word(['0', '1', '0', '1', '1', '0', '1', '0'] * 8)
    data.print_val_ls()
    print(data.get_value_int10())

    # init with int ls
    data = Word([0, 1, 0, 1, 1, 0, 1, 0] * 8)
    data.print_val_ls()
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
