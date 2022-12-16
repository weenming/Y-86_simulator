# Y86 Simulator

## Backend

#### 接口
`simulator.py`中提供
- `init_CPU`，传入汇编代码字符串，返回初始化完成的`CPU`实例
  - 通过正则表达式将字符串转换为数据，从而初始化内存
- `run_CPU`，传入参数指定执行1 stage还是1 cycle，返回这步完成后的状态json，和其他信息，如异常消息、`valA`等中间值

#### Sequential Y86 处理器的实现
- 因为数据是根据二补码表示的，涉及到位级操作时较为复杂，所以我们定义数据抽象类`DataArb`和子类`Word`, `Byte`实现相关操作，储存在`abstraction`子包中
  - `DataArb`是任意长度的二进制数据，用各个元素为`0`或`1`的python list实现。
    - 初始化：可以使用16进制`str`*或*10进制`int`
    - 方法：可以以16进制`str`*或*10进制`int`*或*2进制list of `int`输出；也可以指定ArbData中的某几个`Byte`，返回list of `Byte`s.
    - 主要在Instruction Memory中使用
    - 由于没有固定的长度，不能以有符号数解释，也不可以由有符号数字初始化
  - `Word`是64位的二进制数据，继承自`DataArb`
    - 由于有固定的长度，可以解释成有符号数字，可以由有符号数字初始化
  - `Byte`是8位的二进制数据，继承自`DataArb`
    - 主要在内存中使用

- 我们将寄存器，时钟，内存、ALU和指令内存的读、写等操作在相应的类中实现。我们将其封装成hardware子包，对应源文件在hardware目录下。
  - `Register` 类实现了寄存器的数据存储以及读写端口
    - 用一个长度为15的元素为`Word`的列表
  - `Memory` 类实现了内存的数据储存和读写接口
    - 内存是由`Byte`的列表实现的。由于内存使用小端法储存，这样的实现更符合直觉一些。
    - 写入方法中，只需要将`Word`转换成`Byte`s的列表并逆序储存即可，保持了数据抽象；读取也是类似的
  - `InstructMem` 类
    - 实现了指令读取、非法指令的判断
  - `Stat` 类
  - `CondCode` 类
  - `ALU` 类
    - 实现算术和逻辑运算，将输入的`Word`实例转换成int进行计算或者利用二进制list逐元素逻辑运算
- 在`CPU.py`中，我们实现了`CPU`类，在SEQ各阶段中实现各个上述组件之间的通信。
  - 由于实现中的一些判断较冗长，我们将整理到`sequence`包的各个模块中。
  - 控制`CPU`实例运行的接口为`run` 方法，它将调用一个生成器成员函数`cycle`，通过生成器的`send`方法控制CPU运行一个stage或者一个cycle。

#### 复用：以指令`iaddq`为例
我们先实现了除了iaddq以外的所有指令，在测试时发现还有额外的这条指令。事实上，添加它几乎没有增加几行代码。只需要到各个SEQ阶段的选择判断函数中把`iaddq`对应的icode加到合适的条件里，就完成了。容易想象，在实际芯片设计中，新增这条指令大概利用了不少已有器件，从而增加了芯片的效率。但对于软件工程师来说，四处寻找散落的if else好像并不是什么美差。

#### 异常处理
- 根据异常状态码，我们使用3个Error类进行异常处理
  - `Halt`
  - `InstructionError`
  - `AddressError`
- 错误发生时，程序将抛出异常，并被CPU类的run方法中的异常处理语句接收。由于状态回退至异常发生的*一步*[^stage]之前，处理器的状态一定是即将发生错误的状态。更具体地说，我们的处理器
  - 不会允许*写入*错误的地址/*读取*错误的指令，在进行非法操作的尝试后停止运行
  - 读取Halt指令*后*停止运行
  
#### 测试用例
- 请在项目的根目录下运行 `python test.py --bin "python backend/simulator.py"`来进行测试。
- 我们的程序和`prog10.yo`的参考答案结果不同，最后一步中，我们的程序`rsp`为`0`，而参考答案为`-8`。如前所述，当出现地址错误时，我们的程序不会允许写入内存，而直接停止。由于Y86的约定是，先压栈再修改`rsp`，所以我们的程序停止时，`rsp`为`0`而非`-8`。这和测试用例所给答案不同，但我们认为我们的做法更合理些。

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


# 收获和感悟
### Git
第一次感受到`git`的精彩--我当然不会自称git大师，但是在较大的项目中使用恰当使用工作分支、发布分支和远程仓库，使得不管是本地开发、测试还是远程合作的效率都得到了较大的提高 

### 复用
在软件开发中过度追求"复用"有时可能并非最佳实践--这似乎在某种程度上增加了各个组件的耦合。但对芯片工程师来说，问题的答案就简单不少了，也许这是因为他们的产品并不需要时刻准备着修改？但我想，也不能说在器件数量和功能之间走钢丝不是一门艺术吧。


[^stage]: stage, 比如fetch stage, decode stage, etc. 请参见`hardware/CPU`中的`CPU.cycle`方法