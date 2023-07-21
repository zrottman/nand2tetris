////////// START BOOTSTRAP
@256
D=A
@SP
M=D
// call Sys.init 0
// call: push return-address
@Bootstrap.0
D=A
@SP
A=M
M=D
@SP
M=M+1
// call: push LCL
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
// call: push ARG
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
// call: push THIS
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
// call: push THAT
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
// call: ARG = SP-n-5; LCL = SP
@SP
D=M
@5
D=D-A
@0
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
// call: goto f
@Sys.init
0;JMP
// call: (return-address)
(Bootstrap.0)
////////// START VM FILE: SimpleFunction.vm
// function SimpleFunction.test 2
(SimpleFunction.test)
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
// push local 0
@0
D=A
@LCL
A=D+M
D=M
@SP
A=M
M=D
@SP
M=M+1
// push local 1
@1
D=A
@LCL
A=D+M
D=M
@SP
A=M
M=D
@SP
M=M+1
// add
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
M=D+M
@SP
M=M+1
// not
@SP
M=M-1
A=M
M=!M
@SP
M=M+1
// push argument 0
@0
D=A
@ARG
A=D+M
D=M
@SP
A=M
M=D
@SP
M=M+1
// add
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
M=D+M
@SP
M=M+1
// push argument 1
@1
D=A
@ARG
A=D+M
D=M
@SP
A=M
M=D
@SP
M=M+1
// sub
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
M=M-D
@SP
M=M+1
// return
// return: FRAME = LCL
@LCL
D=M
@FRAME
M=D
// return: RET = *(FRAME-5)
@5
A=D-A
D=M
@RET
M=D
// return: *ARG = pop()
@SP
M=M-1
A=M
D=M
@ARG
A=M
M=D
@ARG
D=M
// return: SP = ARG+1
@SP
M=D+1
// return: THAT = *(FRAME-1)
@FRAME
D=M
@1
A=D-A
D=M
@THAT
M=D
// return: THIS = *(FRAME-2)
@FRAME
D=M
@2
A=D-A
D=M
@THIS
M=D
// return: ARG = *(FRAME-3)
@FRAME
D=M
@3
A=D-A
D=M
@ARG
M=D
// return: LCL = *(FRAME-4)
@FRAME
D=M
@4
A=D-A
D=M
@LCL
M=D
// return: goto RET
@RET
A=M
0;JMP
// END WRITE
