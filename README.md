# Y86 Simulator

## How to Run
Use command `python setup.py` to invoke a local server at `http://127.0.0.1:5000`. You can visit this URL in a browser or click on the link shown in the command line window (if supported). On the webpage you can upload files containing machine code and then run the simulator in real time.

- The file should be formatted as those in the `./test/` folder. That is, after each line of code, insert `|` before assembly code or the next line.
- Make sure flask is installed in your python environment. Our frontend is implemented using flask framework.


## Local Tests
- To run the test, execute `python test.py --bin "python backend/simulator.py"` under the root directory of the project. The whole testing process takes about 5 seconds [^ourMachine].
- The results are consistent with the officially published answers. [^wrong?]


## Implementation of the simulator

#### API
In `simulator.py`
- String of assembly language code is passed in `init_CPU`, which returns the initialized instance of `CPU`.
  - Convert the string into digits with the regular expression to initialize the memory.
- `run_CPU` executes 1 stage or 1 cycle according to the argument passed in, and returns the state after this step as a JSON file, as well as other information, e.g. exceptions and intermediate values like `valA`.


#### Exception Handling
- Use 3 Error classes to handle exceptions
  - `Halt`
  - `InstructionError`
  - `AddressError`
- When an error occurs, an exception will be thrown and caught by the `run` method in `CPU`. Since the state is reverted back to *one step* [^stage] before the exception, the state of the CPU is before the error. More specifically, our CPU
  - Does not allow to *write into* a wrong address or *read* a wrong instruction
  - Stops *after* `Halt`.
  
## Implementation of the frontend


## File structure
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



[^stage]: stage, 比如fetch stage, decode stage, etc. Please refer to `CPU.cycle` in `hardware/CPU`.
[^ourMachine]: The CPU of Our machine is: AMD Ryzen R7-4800U
[^wrong?]:　Except the result of `prog10.yo` is different from the reference. In the last step, the `rsp` of our CPU is `0` but in the reference, it is `-8`. As stated, when an address error occurs, our CPU will not allow writing into the wrong memory location but will stop immediately. Since the Y-86 protocol updates `rsp` after pushing into the stack, our `rsp` will not update before the error occurs and hence is `-8` when the CPU halts. We believe our implementation is more reasonable.
