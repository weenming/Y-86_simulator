#include <stdio>

typedef unsigned long long u64;

#define STACK_SIZE 8192
#define AOK 1 // 正常操作
#define HLT 2 // 遇到halt指令
#define ADR 3 // 遇到非法地址
#define INS 4 // 遇到非法指令
#define HLT_STR "Error: Halt instruction encountered at %ld.", pc
#define ADR_STR "Error: Invalid address encountered at %ld.", pc
#define INS_STR "Error: Invalid instruction encountered at %ld.", pc

static struct RegF{
    long rax;
    long rcx;
    long rdx;
    long rbx;
    long rsp;
    long rbp;
    long rsi;
    long rdi;
    long r8;
    long r9;
    long r10;
    long r11;
    long r12;
    long r13;
    long r14;
    long f;
} __REG;
struct RegF* reg = &__REG;

static struct ConC{
    int ZF;
    int SF;
    int OF;
} __CC;
struct ConC* cc = &__CC;

char stat;

char* pc;

u64* base_stack = malloc(STACK_SIZE);
u64* stack = base_stack + STACK_SIZE;

int fetch(){
    char icode = *pc;
    char ifun = *(pc+1);
    switch (icode){
        case '0': stat = (ifun == '0') ? halt() : INS; break;
        case '1': stat = (ifun == '0') ? nop() : INS; break;
        case '2': comvXX(ifun); break;
        case '3': stat = (ifun == '0') ? irmovq() : INS; break;
        case '4': stat = (ifun == '0') ? rmmovq() : INS; break;
        case '5': stat = (ifun == '0') ? mrmovq() : INS; break;
        case '6': OPq(ifun); break;
        case '7': jXX(ifun); break;
        case '8': stat = (ifun == '0') ? call() : INS; break;
        case '9': stat = (ifun == '0') ? ret() : INS; break;
        case 'a': stat = (ifun == '0') ? pushq() : INS; break;
        case 'b': stat = (ifun == '0') ? popq() : INS; break;
        default: stat = INS;
    }
    if (stat == INS) assert(INS_STR);
    return 0;
}

int cmovXX(char ifun){
    switch (ifun){
        case '0': rrmovq(); break;
        case '1': cmovle(); break;
        case '2': cmovl(); break;
        case '3': cmove(); break;
        case '4': cmovne(); break;
        case '5': cmovge(); break;
        case '6': cmovg(); break;
        default: stat = INS; assert(INS_STR);
    }
    return AOK;
}

int OPq(char ifun){
    switch (ifun){
        case '0': addq(); break;
        case '1': subq(); break;
        case '2': andq(); break;
        case '3': xorq(); break;
        default: stat = INS; assert(INS_STR);
    }
    return AOK;
}

int jXX(char ifun){
    switch (ifun){
        case '0': jmp(); break;
        case '1': jle(); break;
        case '2': jl(); break;
        case '3': je(); break;
        case '4': jne(); break;
        case '5': jge(); break;
        case '6': jg(); break;
        default: stat = INS; assert(INS_STR);
    }
    return AOK;
}

int nop(){
    pc += 2;
    return AOK;
}

int ret(){
    // if......指针越界
    pc = *stack;
    stack++;
    rsp += 8;
    return AOK;
}

int call(){
    long valC = (u64*)(pc+2);
    long valP = pc + 18;
    *stack
}