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
////////// START VM FILE: Sys.vm
// function Sys.init 0
(Sys.init)
// push constant 4000
@4000
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop pointer 0
@0
D=A
@3
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
// push constant 5000
@5000
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop pointer 1
@1
D=A
@3
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
// call Sys.main 0
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
@0
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
// call: goto f
@Sys.main
0;JMP
// call: (return-address)
(Sys.vm.1)
// pop temp 1
@1
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
// label LOOP
(LOOP)
// goto LOOP
@LOOP
0;JMP
// function Sys.main 5
(Sys.main)
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
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 4001
@4001
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop pointer 0
@0
D=A
@3
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
// push constant 5001
@5001
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop pointer 1
@1
D=A
@3
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
// push constant 200
@200
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop local 1
@1
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
// push constant 40
@40
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop local 2
@2
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
// push constant 6
@6
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop local 3
@3
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
// push constant 123
@123
D=A
@SP
A=M
M=D
@SP
M=M+1
// call Sys.add12 1
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
@1
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
// call: goto f
@Sys.add12
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
// push local 2
@2
D=A
@LCL
A=D+M
D=M
@SP
A=M
M=D
@SP
M=M+1
// push local 3
@3
D=A
@LCL
A=D+M
D=M
@SP
A=M
M=D
@SP
M=M+1
// push local 4
@4
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
// function Sys.add12 0
(Sys.add12)
// push constant 4002
@4002
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop pointer 0
@0
D=A
@3
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
// push constant 5002
@5002
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop pointer 1
@1
D=A
@3
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
// push constant 12
@12
D=A
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