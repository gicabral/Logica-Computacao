; constantes
SYS_EXIT equ 1
SYS_READ equ 3
SYS_WRITE equ 4
STDIN equ 0
STDOUT equ 1
True equ 1
False equ 0
segment . data
segment . bss ; v a r i a v e i s
r e s RESB 1
s e c t i o n . text
g l o b a l _start
print : ; subrotina print
PUSH EBP ; guarda o base pointer
MOV EBP, ESP ; e s t a b e l e c e um novo base pointer
1
MOV EAX, [EBP+8] ; 1 argumento antes do RET e EBP
XOR ESI , ESI
print_dec : ; empilha todos os d i g i t o s
MOV EDX, 0
MOV EBX, 0x000A
DIV EBX
ADD EDX, '0 '
PUSH EDX
INC ESI ; contador de d i g i t o s
CMP EAX, 0
JZ print_next ; quando acabar pula
JMP print_dec
print_next :
CMP ESI , 0
JZ print_exit ; quando acabar de imprimir
DEC ESI
MOV EAX, SYS_WRITE
MOV EBX, STDOUT
POP ECX
MOV [ r e s ] , ECX
MOV ECX, r e s
MOV EDX, 1
INT 0x80
JMP print_next
print_exit :
POP EBP
RET
; subrotinas i f / while
binop_je :
JE binop_true
JMP binop_false
binop_jg :
JG binop_true
JMP binop_false
binop_jl :
JL binop_true
JMP binop_false
binop_false :
MOV EBX, False
JMP binop_exit
binop_true :
MOV EBX, True
binop_exit :
RET
_start :
PUSH EBP ; guarda o base pointer
MOV EBP, ESP ; e s t a b e l e c e um novo base pointer
2
; codigo gerado pelo compilador
PUSH DWORD 0 ; Dim i as I nteg er [EBP−4]
PUSH DWORD 0 ; Dim n as I nteg er [EBP−8]
PUSH DWORD 0 ; Dim f as I nteg er [EBP−12]
MOV EBX, 5
MOV [EBP−8] , EBX ; n = 5
MOV EBX, 2
MOV [EBP−4] , EBX ; i = 2
MOV EBX, 1
MOV [EBP−12] , EBX ; f = 1
LOOP_34:
MOV EBX, [EBP−4]
PUSH EBX ; empilha i
MOV EBX, [EBP−8]
PUSH EBX ; empilha n
MOV EBX, 1
POP EAX
ADD EAX, EBX ; n + 1
MOV EBX, EAX
POP EAX
CMP EAX, EBX
CALL binop_jl ; i < n + 1
CMP EBX, False
JE EXIT_34
MOV EBX, [EBP−12]
PUSH EBX ; empilha f
MOV EBX, [EBP−4]
POP EAX ; empilha i
IMUL EBX ; i ∗ f
MOV EBX, EAX
MOV [EBP−12] , EBX ; f = f ∗ i
MOV EBX, [EBP−4]
PUSH EBX ; empilha i
MOV EBX, 1
POP EAX
ADD EAX, EBX ; i + 1
MOV EBX, EAX
MOV [EBP−4] , EBX ; i = i + 1
JMP LOOP_34
EXIT_34 :
MOV EBX, [EBP−12]
PUSH EBX ; empilha f
CALL print ; Print f
POP EBX ; limpa args
; interrupcao de saida
POP EBP
MOV EAX, 1
INT 0x80
