@256
D=A
@SP
M=D
@RET_ADD_CALL1
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
@0
D=A
@SP
D=M-D
@R15
M=D
@5
D=A
@R15
D=M-D
@ARG
M=D
@SP
D=M
@LCL
M=D
@Sys.init
0; JMP
(RET_ADD_CALL1)
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
@0
D=A
@LCL
D=D+M
@R13
M=D
@SP
A=M
D=M
@R13
A=M
M=D
(LOOP_START)
@0
D=A
@ARG
D=D+M
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1
@0
D=A
@LCL
D=D+M
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M+D
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
@0	
D=A
@LCL
D=D+M
@R13
M=D
@SP
A=M
D=M
@R13
A=M
M=D
@0
D=A
@ARG
D=D+M
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
@0
D=A
@ARG
D=D+M
@R13
M=D
@SP
A=M
D=M
@R13
A=M
M=D
@0
D=A
@ARG
D=D+M
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@LOOP_START
D;JNE
@0
D=A
@LCL
D=D+M
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1