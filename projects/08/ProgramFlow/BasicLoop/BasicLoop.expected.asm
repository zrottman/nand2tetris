//push constant 0    
    @0
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1
//pop local 0         // initializes sum = 0
    @0
    D=A
    @LCL
    D=D+M
    @R13
    M=D
    @SP
    M=M-1
    A=M
    D=M
    @R13
    A=M
    M=D
//label LOOP_START
    (LOOP_START)
//push argument 0    
//push local 0
//add
//pop local 0	        // sum = sum + counter
//push argument 0
//push constant 1
//sub
//pop argument 0      // counter--
//push argument 0
//if-goto LOOP_START  // If counter != 0, goto LOOP_START
    
//push local 0

