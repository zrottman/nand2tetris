//push constant 17
    // D=i
    @17
    D=A
    // RAM[SP]=D=i
    @SP
    A=M
    M=D
    // SP++
    @SP
    M=M+1
//push constant 17
    // D=i
    @17
    D=A
    // RAM[SP]=D
    @SP
    A=M
    M=D
    // SP++
    @SP
    M=M+1
//eq
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
    // D==0? JUMP to D=-1, else D=0
    @IFTRUE_j                           // j: incrementer to ensure jump dests are unique
    D;JEQ
    D=0
    @ENDIF_j
    0;JMP
    (IFTRUE_j)
    D=-1
    (ENDIF_j)
    // SP[RAM]=D
    @SP
    A=M
    M=D
    // SP++
    @SP
    M=M+1

//push constant 17
//push constant 16
//eq
//push constant 16
//push constant 17
//eq
//push constant 892
//push constant 891
//lt
//push constant 891
//push constant 892
//lt
//push constant 891
//push constant 891
//lt
//push constant 32767
//push constant 32766
//gt
//push constant 32766
//push constant 32767
//gt
//push constant 32766
//push constant 32766
//gt
//push constant 57
//push constant 31
//push constant 53
//add
//push constant 112
//sub
//neg
//and
//push constant 82
//or
//not
