////////// START BOOTSTRAP
@256
D=A
@SP
M=D
// call Sys.init 0
@Bootstrap.0
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
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
@Sys.init
0;JMP
(Bootstrap.0)
////////// START VM FILE: Main.vm
// function Main.fibonacci 0
(Main.fibonacci)
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
// push constant 2
@2
D=A
@SP
A=M
M=D
@SP
M=M+1
// lt
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=D-M
@TRUE.Main.vm$1
D;JGT
D=0
@ENDIF.Main.vm$1
0;JMP
(TRUE.Main.vm$1)
D=-1
(ENDIF.Main.vm$1)
@SP
A=M
M=D
@SP
M=M+1
// if-goto IF_TRUE
@SP
M=M-1
A=M
D=M
@IF_TRUE
D;JNE
// goto IF_FALSE
@IF_FALSE
0;JMP
// label IF_TRUE
(IF_TRUE)
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
// label IF_FALSE
(IF_FALSE)
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
// push constant 2
@2
D=A
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
// call Main.fibonacci 1
@Main.vm.2
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@5
D=D-A
@1
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
(Main.vm.2)
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
// push constant 1
@1
D=A
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
// call Main.fibonacci 1
@Main.vm.3
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@5
D=D-A
@1
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
(Main.vm.3)
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
////////// START VM FILE: Sys.vm
// function Sys.init 0
(Sys.init)
// push constant 4
@4
D=A
@SP
A=M
M=D
@SP
M=M+1
// call Main.fibonacci 1
@Sys.vm.4
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@5
D=D-A
@1
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
(Sys.vm.4)
// label WHILE
(WHILE)
// goto WHILE
@WHILE
0;JMP
// END WRITE
