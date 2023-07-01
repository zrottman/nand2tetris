//push constant 7

    // D=i
    @7
    D=A
    // RAM[SP]=i
    @SP
    A=M
    M=D
    // SP++
    @SP
    M=M+1

//push constant 8

    // D=i
    @8
    D=A
    // RAM[SP]=D=i
    @SP
    A=M
    M=D
    // SP++
    @SP
    M=M+1

//add

    // SP--
    @SP
    M=M-1
    // RAM[R13]=RAM[SP]
    A=M
    D=M
    @R13
    M=D
    // SP--
    @SP
    M=M-1
    // D=RAM[SP]
    A=M
    D=M
    // D=D-RAM[R13]
    @R13
    D=D-M
    // RAM[SP]=D
    @SP
    A=M
    M=D
    // SP++
    @SP
    M=M+1
