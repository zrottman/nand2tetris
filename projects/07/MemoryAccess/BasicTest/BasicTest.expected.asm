// push constant 10

    // D=10
    @10                     // @i
    D=A                     //D=i
    // RAM[SP]=10
    @SP
    A=M
    M=D
    // SP++
    @SP
    M=M+1

//pop local 0

    // SP--
    @SP
    M=M-1
    // RAM[R13]=LCL+i  -> dest address for popped
    @0                      // @i
    D=A                     // D=i
    @LCL
    D=D+A                   // D=LCL+i
    @R13
    M=D
    // D=RAM[SP] -> value to pop
    @SP
    A=M
    D=M                     // D=RAM[SP]
    // RAM[LCL + i]=popped
    @R13
    A=M
    M=D
    
//push constant 21

    // D=21
    @21
    D=A
    // RAM[SP]=21
    @SP
    A=M
    M=D
    // SP++
    @SP
    M=M+1

//push constant 22

    // D=22
    @22
    D=A
    // RAM[SP]=22
    @SP
    A=M
    M=D
    // SP++
    @SP
    M=M+1

//pop argument 2

    // SP--
    @SP
    M=M-1
    // RAM[R13]=ARG+i -> dest address for popped
    @2
    D=A
    @ARG
    D=D+A
    @R13
    M=D
    // D=RAM[SP] -> value to pop
    @SP
    A=M
    D=M
    // RAM[ARG+i]=popped
    @R13
    A=M
    M=D
    
//pop argument 1

    // SP--
    @SP
    M=M-1
    // RAM[R13]=ARG+1 -> dest address for popped
    @1
    D=A
    @ARG
    D=D+A
    @R13
    M=D
    // D=RAM[SP] -> value to pop
    @SP
    A=M
    D=M
    // RAM[ARG+i]=popped
    @R13
    A=M
    M=D

//push constant 36
//pop this 6
//push constant 42
//push constant 45
//pop that 5
//pop that 2
//push constant 510
//pop temp 6
//push local 0
//push that 5
//add  -> RAM[SP-1] + RAM[SP]

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
    // RAM[R14]=RAM[SP]
    A=M
    D=M
    @R14
    M=D
    // D=RAM[R13]+RAM[R14]
    @R13
    D=M
    @R14
    D=D+M
    // RAM[SP]=D
    @SP
    A=M
    M=D

//push argument 1
//sub -> RAM[SP-1]/item2 - RAM[SP]/item1

    // SP--
    @SP
    M=M-1
    // RAM[R13]=RAM[SP]=item1
    A=M
    D=M
    @R13
    M=D
    // SP--
    @SP
    M=M-1
    // D=RAM[SP]=item2
    A=M
    D=M
    // D=item2-item1=D-RAM[R13]
    @R13
    D=D-M
    // RAM[SP]=D
    @SP
    A=M
    M=D
    // SP++
    @SP
    M=M+1

//push this 6
//push this 6
//add
//sub
//push temp 6
//add
