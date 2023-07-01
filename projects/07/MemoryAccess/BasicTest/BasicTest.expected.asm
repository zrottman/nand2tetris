// push constant 10
    // D = 10
    @10
    D=A
    // RAM[SP] = D = 10
    @SP
    A=M
    M=D
    // SP++
    @SP
    M=M+1

//pop local 0
    // D = 0
    @0
    D=A
    // A = LOCAL + D = LOCAL + 0 = LOCAL
    @LOCAL
    A=A+D
    // D = popped = 10
    @SP
    A=M
    D=M
    // RAM[LOCAL + 0] = D = popped = 10

    
    // D = LOCAL

    @LOCAL
    D=A
    //
    @
    
//push constant 21
//push constant 22
//pop argument 2
//pop argument 1
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
//add
//push argument 1
//sub
//push this 6
//push this 6
//add
//sub
//push temp 6
//add
