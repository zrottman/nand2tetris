//push constant 111
    // D=i
    @111
    D=A
    // RAM[SP]=i
    @SP
    A=M
    M=D
    // SP++
    @SP
    M=M+1

//push constant 333
    
    // D=i
    @333
    D=A
    // RAM[SP]=i
    @SP
    M=A
    M=D
    // SP++
    @SP
    M=M+1
    
//push constant 888
    
    // D=i
    @888
    D=A
    // RAM[SP]=i
    @SP
    A=M
    M=D
    // SP++
    @SP
    M=M+1

//pop static 8 -> pop top of stack to RAM[16+8]

    // SP--
    @SP
    M=M-1
    // RAM[R13]=16+i -> dest address for popped
    @16
    D=A
    @8
    D=D+A                           // D=24
    @R13
    M=D
    // D=RAM[SP]
    @SP
    A=M
    D=M
    // RAM[16+i]=popped
    @R13
    A=M
    M=D
    
//pop static 3

    // SP--
    @SP
    M=M-1
    // RAM[R13]=16+i -> dest address for popped
    @16
    D=A
    @3
    D=D+A
    @R13
    M=D
    // D=RAM[SP]
    @SP
    A=M
    D=M
    // RAM[16+i]=popped
    @R13
    A=M
    M=D

//pop static 1
//push static 3

    // D=RAM[16+i]
    @16
    D=A
    @3
    D=D+1
    // RAM[SP]=RAM[16+i]
    @SP
    A=M
    M=D
    // SP++
    @SP
    M=M+1

//push static 1
//sub
//push static 8
//add
