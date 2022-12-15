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
- 我们将寄存器，时钟，内存、ALU和指令内存的读、写等操作在相应的类中实现。我们将其封装成hardware子模块，对应源文件在hardware目录下。
  - Register 类实现了给定 src\dst 后对寄存器的读写操作

#### 复用：以指令`iaddq`为例

#### 封装
我们将backend封装一个Python module，由simulator.py提供前端访问的接口。

#### 测试用例
- 异常和停止
