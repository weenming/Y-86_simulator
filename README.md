# Y86 Simulator

## Backend

#### 接口
`simulator.py`中提供
- `init_CPU`，传入汇编代码字符串，返回初始化完成的`CPU`实例
  - 通过正则表达式将字符串转换为数据，从而初始化内存
- `run_CPU`，传入参数指定执行1 stage还是1 cycle，返回这步完成后的状态json，和其他信息，如异常消息、`valA`等中间值



#### 异常处理
- 根据异常状态码，我们使用3个Error类进行异常处理
  - `Halt`
  - `InstructionError`
  - `AddressError`
- 错误发生时，程序将抛出异常，并被CPU类的run方法中的异常处理语句接收。由于状态回退至异常发生的*一步*[^stage]之前，处理器的状态一定是即将发生错误的状态。更具体地说，我们的处理器
  - 不会允许*写入*错误的地址/*读取*错误的指令，在进行非法操作的尝试后停止运行
  - 读取Halt指令*后*停止运行
  
#### 测试用例
- 请在项目的根目录下运行 `python test.py --bin "python backend/simulator.py"`来进行测试。所有测试需要大约5秒。
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



[^stage]: stage, 比如fetch stage, decode stage, etc. 请参见`hardware/CPU`中的`CPU.cycle`方法