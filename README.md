# Y86 Simulator

## Backend
### File structure
backend
 ┣ abstraction
 ┃ ┣ data.py
 ┃ ┗ __init__.py
 ┣ hardware
 ┃ ┣ ALU.py
 ┃ ┣ Clock.py
 ┃ ┣ InstructMem.py
 ┃ ┣ Memory.py
 ┃ ┣ Registers.py
 ┃ ┗ __init__.py
 ┣ mytests
 ┃ ┣ test_cpu.py
 ┃ ┣ test_data.py
 ┃ ┣ test_error.py
 ┃ ┣ test_mem.py
 ┃ ┣ test_regs.py
 ┃ ┗ x**_test.py
 ┣ sequence
 ┃ ┣ decode.py
 ┃ ┣ execute.py
 ┃ ┣ fetch.py
 ┃ ┣ memory.py
 ┃ ┣ update_PC.py
 ┃ ┣ write_back.py
 ┃ ┗ __init__.py
 ┣ CPU.py
 ┣ error.py
 ┣ simulator.py
 ┣ simulator_local_test.py
 ┗ __init__.py


#### Sequential Y86 处理器的实现
- 因为数据是根据二补码表示的，涉及到位级操作时较为复杂，所以我们定义数据抽象类`ArbData`和子类`Word`, `Byte`实现相关操作，储存在`abstraction`子包中
  - `ArbData`是任意长度的二进制数据，用各个元素为`0`或`1`的python list实现。
    - 初始化：可以使用16进制`str`*或*10进制`int`
    - 方法：可以以16进制`str`*或*10进制`int`*或*2进制list of `int`输出；也可以指定ArbData中的某几个`Byte`，返回list of `Byte`s.
    - 主要在Instruction Memory中使用
    - 由于没有固定的长度，不能以有符号数解释，也不可以由有符号数字初始化
  - `Word`是64位的二进制数据，继承自`ArbData`
    - 由于有固定的长度，可以解释成有符号数字，可以由有符号数字初始化
  - `Byte`是8位的二进制数据，继承自`DataArb`
    - 主要在内存中使用

- 我们将寄存器，时钟，内存、ALU和指令内存的读、写等操作在相应的类中实现。我们将其封装成hardware子包，对应源文件在hardware目录下。
  - Register 类实现了寄存器的数据存储以及读写端口
    - 用一个长度为15的元素为`Word`的列表
  - Memory 类实现了内存的数据储存和读写接口
    - 内存是由`Byte`的列表实现的。由于内存使用小端法储存，这样的实现更符合直觉一些。
    - 写入方法中，只需要将`Word`转换成`Byte`s的列表并逆序储存即可，保持了数据抽象；读取也是类似的
  - InstructMem 类

#### 复用：以指令`iaddq`为例

#### 异常处理
- 根据异常状态码，我们使用3个Error类进行异常处理
  - Halt
  - InstructionError
  - AddressError
- 错误发生时，程序将抛出异常，并被CPU类的run方法中的异常处理语句接收
  - 由于状态回退至异常发生的*一步*^[cycle]之前，我们
#### 测试用例
- 异常和停止


# 收获和感悟
> 第一次感受到`git`的精彩--我当然不会自称git大师，但是即使是我这样的弱智也能


[^stage]: 指的是stage, 比如fetch stage, decode stage, etc.