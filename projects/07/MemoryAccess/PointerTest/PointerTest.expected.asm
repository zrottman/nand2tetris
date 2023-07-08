//push constant 3030

    // D=i
    @3030
    D=A
    // RAM[SP]=i
    @SP
    A=M
    M=D
    // SP++
    @SP
    M=M+1

//pop pointer 0

    // SP--
    @SP
    M=M-1
    // D=RAM[SP]
    A=M
    D=M
    // THIS=popped
    @THIS
    M=D

//push constant 3040

    // D=i
    @3040
    D=A
    // RAM[SP]=D
    @SP
    A=M
    M=D
    // SP++
    @SP
    M=M+1

//pop pointer 1

    // SP--
    @SP
    M=M-1
    // D=RAM[SP]
    A=M
    D=M
    // THAT=popped
    @THAT
    M=D

//push constant 32

    // D=i
    @22
    D=A
    // RAM[SP]=D
    @SP
    A=M
    M=D
    // SP++
    @SP
    M=M+1

//pop this 2

    // SP--
    @SP
    M=M-1
    // RAM[R13]=popped
    A=M
    D=M
    @R13
    M=D
    // RAM[R14]=THIS+i
    @THIS
    D=M
    @2
    D=D+A                   // D=THIS+i
    @R14
    M=D                     // RAM[R14]=THIS+i
    // RAM[THIS+i]=popped
    @R13
    D=M                     // D=RAM[R13]=popped
    @R14
    A=M                     // A=RAM[R14]=THIS+i
    M=D                     // RAM[THIS+i]=D=popped

//push constant 46

    // D=i
    @46
    D=A
    // RAM[SP]=i
    @SP
    A=M
    M=D
    // SP++
    @SP
    M=M+1
    
//pop that 6

    // SP--
    @SP
    M=M-1
    // RAM[R13]=RAM[SP]
    A=M
    D=M
    @R13
    M=D
    // RAM[R14]=THAT+i
    @THAT
    D=M
    @6
    D=D+A
    @R14
    M=D
    // RAM[THAT+i]=RAM[13]
    @R13
    D=M
    @R14
    A=M
    M=D

//push pointer 0

    // D=RAM[THIS]
    @THIS
    D=M
    // RAM[SP]=RAM[THAT]=D
    @SP
    A=M
    M=D
    // SP++
    @SP
    M=M+1

//push pointer 1

    // D=RAM[THAT]
    @THAT
    D=M
    // RAM[SP]=D=RAM[THAT]
    @SP
    A=M
    M=D
    // SP++
    @SP
    M=M+1

//add item2+item1
    
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
    // D=RAM[SP]
    A=M
    D=M
    // D=D+RAM[R13]
    @R13
    D=D+M
    // RAM[SP] = D
    @SP
    A=M
    M=D
    // SP++
    @SP
    M=M+1

//push this 2

    // D=THIS+2
    @THIS
    D=M
    @2
    D=D+A
    // RAM[SP]=RAM[THIS+2]=RAM[D]
    @SP
    A=M
    M=D
    // SP++
    @SP
    M=M+1

//sub -> RAM[SP-1]-RAM[SP]
    
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

//push that 6
//add
