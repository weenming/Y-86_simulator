cpu = {'PC': '0x0', 
    'REG': {'rax': '0x0', 
        'rcx': '0x0', 
        'rdx': '0x0', 
        'rbx': '0x0', 
        'rsp': '0x0', 
        'rbp': '0x0', 
        'rsi': '0x0', 
        'rdi': '0x0', 
        'r8': '0x0', 
        'r9': '0x0', 
        'r10': '0x0', 
        'r11': '0x0', 
        'r12': '0x0', 
        'r13': '0x0', 
        'r14': '0x0'}, 
    'CC': {'ZF': 1, 
        'SF': 0, 
        'OF': 0}, 
    'STAT': 1, 
    'MEM': {'0': 16839728, 
        '8': 188900986322944, 
        '16': 5742106704766566400}, 
    'valA': '0x0', 
    'valB': '0x0', 
    'valC': '0x100', 
    'valE': '0x100', 
    'valM': '0x0', 
    'valP': '0xa'}

for i in cpu['MEM']:
    print(type(i))
    a = hex(int(i))
    print(a)
    b = cpu.pop(i)
    cpu[a] = b

print(cpu)