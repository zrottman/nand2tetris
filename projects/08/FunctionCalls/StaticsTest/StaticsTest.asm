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
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
// call: push ARG
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
// call: push THIS
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
// call: push THAT
@THAT
D=M
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
////////// START VM FILE: Class1.vm
// function Class1.set 0
(Class1.set)
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
// pop static 0
@Class1.vm.0
D=A
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
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
// pop static 1
@Class1.vm.1
D=A
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
// push constant 0
@0
D=A
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
// function Class1.get 0
(Class1.get)
// push static 0
@Class1.vm.0
D=M
@SP
A=M
M=D
@SP
M=M+1
// push static 1
@Class1.vm.1
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
////////// START VM FILE: Sys.vm
// function Sys.init 0
(Sys.init)
// push constant 6
@6
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 8
@8
D=A
@SP
A=M
M=D
@SP
M=M+1
// call Class1.set 2
// call: push return-address
@Sys.vm.1
D=A
@SP
A=M
M=D
@SP
M=M+1
// call: push LCL
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
// call: push ARG
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
// call: push THIS
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
// call: push THAT
@THAT
D=M
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
@2
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
// call: goto f
@Class1.set
0;JMP
// call: (return-address)
(Sys.vm.1)
// pop temp 0
@0
D=A
@5
D=D+A
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
// push constant 23
@23
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 15
@15
D=A
@SP
A=M
M=D
@SP
M=M+1
// call Class2.set 2
// call: push return-address
@Sys.vm.2
D=A
@SP
A=M
M=D
@SP
M=M+1
// call: push LCL
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
// call: push ARG
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
// call: push THIS
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
// call: push THAT
@THAT
D=M
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
@2
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
// call: goto f
@Class2.set
0;JMP
// call: (return-address)
(Sys.vm.2)
// pop temp 0
@0
D=A
@5
D=D+A
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
// call Class1.get 0
// call: push return-address
@Sys.vm.3
D=A
@SP
A=M
M=D
@SP
M=M+1
// call: push LCL
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
// call: push ARG
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
// call: push THIS
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
// call: push THAT
@THAT
D=M
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
@Class1.get
0;JMP
// call: (return-address)
(Sys.vm.3)
// call Class2.get 0
// call: push return-address
@Sys.vm.4
D=A
@SP
A=M
M=D
@SP
M=M+1
// call: push LCL
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
// call: push ARG
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
// call: push THIS
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
// call: push THAT
@THAT
D=M
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
@Class2.get
0;JMP
// call: (return-address)
(Sys.vm.4)
// label WHILE
(WHILE)
// goto WHILE
@WHILE
0;JMP
////////// START VM FILE: Class2.vm
// function Class2.set 0
(Class2.set)
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
// pop static 0
@Class2.vm.0
D=A
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
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
// pop static 1
@Class2.vm.1
D=A
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
// push constant 0
@0
D=A
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
// function Class2.get 0
(Class2.get)
// push static 0
@Class2.vm.0
D=M
@SP
A=M
M=D
@SP
M=M+1
// push static 1
@Class2.vm.1
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
