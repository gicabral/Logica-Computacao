import re
import sys

arquivo = sys.argv[1]

reserved = ["println", "readln", "while", "if", "else", "int", "bool", "true", "false", "string"]
PRINTLN, READLN, WHILE, IF, ELSE, INT, BOOL, TRUE, FALSE, STRING  = reserved

class Token:
    def __init__(self, tipo, valor):
        self.type = tipo
        self.value = valor


class Tokenizer:
    def __init__(self, origin, actual):
        self.origin = origin
        self.position = 0
        if actual == None:
            self.actual = Token("int", 0)
        else:
            self.actual = Token(actual.type, actual.value)

    def selectNext(self):
        while (self.position < len(
                self.origin)) and (self.origin[self.position] == " " or self.origin[self.position] == "\n" or self.origin[self.position] == "\t"):
            self.position = self.position + 1
        if self.position == len(self.origin):
            self.actual = Token("eof", "eof")

        elif self.origin[self.position].isdigit():
            numero = ""
            while (self.position < len(
                    self.origin)) and (self.origin[self.position].isdigit()):
                numero = numero + self.origin[self.position]
                self.position = self.position + 1
            self.actual = Token("int", int(numero))

        elif self.origin[self.position] == '+':
            self.actual = Token("plus", "+")
            self.position = self.position + 1

        elif self.origin[self.position] == '-':
            self.actual = Token("minus", "-")
            self.position = self.position + 1

        elif self.origin[self.position] == '*':
            self.actual = Token("mult", "*")
            self.position = self.position + 1

        elif self.origin[self.position] == '/':
            self.actual = Token("div", "/")
            self.position = self.position + 1

        elif self.origin[self.position] == '(':
            self.actual = Token("lpar", "(")
            self.position = self.position + 1

        elif self.origin[self.position] == ')':
            self.actual = Token("rpar", ")")
            self.position = self.position + 1

        elif self.origin[self.position] == '=':
            self.position = self.position + 1 
            if self.origin[self.position] == '=':
                self.actual = Token("equal", "==")
                self.position = self.position + 1
            else:     
                self.actual = Token("assignment", "=")

        elif self.origin[self.position] == ';':
            self.actual = Token("semicolon", ";")
            self.position = self.position + 1   

        elif self.origin[self.position] == '{':
            self.actual = Token("lchaves", "{")
            self.position = self.position + 1    

        elif self.origin[self.position] == '}':
            self.actual = Token("rchaves", "{")
            self.position = self.position + 1

        elif self.origin[self.position] == '!':
            self.actual = Token("not", "!")
            self.position = self.position + 1 

        elif self.origin[self.position] == '==':
            self.actual = Token("equal", "==")
            self.position = self.position + 1 

        elif self.origin[self.position] == '&':
            self.position = self.position + 1 
            if self.origin[self.position] == '&':
                self.actual = Token("and", "&&")
                self.position = self.position + 1  

        elif self.origin[self.position] == '|':
            self.position = self.position + 1 
            if self.origin[self.position] == '|':
                self.actual = Token("or", "||")
                self.position = self.position + 1 

        elif self.origin[self.position] == '>':
            self.actual = Token("maior", ">")
            self.position = self.position + 1 

        elif self.origin[self.position] == '<':
            self.actual = Token("menor", "<")
            self.position = self.position + 1  

        elif self.origin[self.position] == '"':
            palavra = ""
            self.position += 1
            while (self.position < (len(self.origin))) and \
                self.origin[self.position] != '"':
                palavra += self.origin[self.position]
                self.position += 1

            self.position += 1
            self.actual = Token(STRING, palavra)                                        

        elif self.origin[self.position].isalpha():
            palavra = ""
            while (self.position < len(
                    self.origin)) and (self.origin[self.position].isalpha() or self.origin[self.position].isdigit() or self.origin[self.position] == "_"):
                palavra = palavra + self.origin[self.position]
                self.position = self.position + 1       
   
            if palavra in reserved:
                self.actual = Token(palavra, palavra)
            else:    
                self.actual = Token("identifier", palavra)      

        else:
            raise ValueError("Simbolo desconhecido", self.origin[self.position])

class Parser:
    @staticmethod
    def block():
        nodes = []
        if Parser.tokens.actual.type == "lchaves":
            Parser.tokens.selectNext()
            while Parser.tokens.actual.type != "rchaves":
                nodes.append(Parser.command())

            if Parser.tokens.actual.type == "rchaves":
                Parser.tokens.selectNext()
                node = Block(" ", nodes)
                return node
            else:
                raise ValueError("Token '}' não encontrado", Parser.tokens.actual.type)    

        else:
            raise ValueError("Token '{' não encontrado", Parser.tokens.actual.type)

    @staticmethod
    def command():
        node = NoOp()
        if Parser.tokens.actual.type == "identifier":
            identifier = Identifier(Parser.tokens.actual.value, [])
            Parser.tokens.selectNext()
            if Parser.tokens.actual.type == "assignment":
                Parser.tokens.selectNext()
                node_l = Parser.parseOrExpression()
                node = Assignment("=", [identifier, node_l])
            else:
                raise ValueError("Atribuição com '=' não encontrada")     

        elif Parser.tokens.actual.type == PRINTLN:
            Parser.tokens.selectNext()
            if Parser.tokens.actual.type == "lpar" :
                Parser.tokens.selectNext()
                node_l = Parser.parseOrExpression()
                node = Println(PRINTLN, [node_l])
                if Parser.tokens.actual.type == "rpar":
                    Parser.tokens.selectNext()
                else:
                    raise ValueError("Não fechou parentesis")    
            else:
                raise ValueError("Não abriu parentesis do println")  

        elif Parser.tokens.actual.type == "lchaves":
            node = Parser.block()
            return node

        elif Parser.tokens.actual.type == WHILE:
            Parser.tokens.selectNext()
            if Parser.tokens.actual.type == "lpar":
                Parser.tokens.selectNext()
                node_l = Parser.parseOrExpression()
                if Parser.tokens.actual.type == "rpar":
                    Parser.tokens.selectNext()
                    node_r = Parser.command()
                    return While("while", [node_l, node_r])
                else:
                    raise ValueError("Não fechou parentesis do while", Parser.tokens.actual.value)    
            else:
                raise ValueError("Não abriu parentesis no while")

        elif Parser.tokens.actual.type == IF:
            Parser.tokens.selectNext()
            node_l = None
            node_r = None
            if Parser.tokens.actual.type == "lpar":
                Parser.tokens.selectNext()
                node = Parser.parseOrExpression()
                if Parser.tokens.actual.type == "rpar":
                    Parser.tokens.selectNext()
                    node_l = Parser.command()

                    if Parser.tokens.actual.type == ELSE:
                        Parser.tokens.selectNext()
                        node_r = Parser.command()
                        return If("if", [node, node_l, node_r]) 

                    return If("if", [node, node_l])  

                else:
                    raise ValueError("Não fechou parentesis do if", Parser.tokens.actual.value)
            else:
                raise ValueError("Não abriu parentesis do if")

        elif Parser.tokens.actual.type == BOOL or Parser.tokens.actual.type == INT or Parser.tokens.actual.type == STRING:
            tipo = Parser.tokens.actual.type
            Parser.tokens.selectNext()
            if Parser.tokens.actual.type == "identifier":
                identifier = Identifier(Parser.tokens.actual.value, [])
                Parser.tokens.selectNext()
                node = VarDec("variável", [identifier, tipo])

        # else:   
        #     return NoOp()        

        if Parser.tokens.actual.type == "semicolon":
            Parser.tokens.selectNext()
            return node 

        else:
            raise ValueError("Erro", Parser.tokens.actual.value)       

         

    @staticmethod
    def parseFactor():
        if Parser.tokens.actual.type == "int":
            node = Parser.tokens.actual.value
            node = IntVal(node, [])
            Parser.tokens.selectNext()
            return node

        elif Parser.tokens.actual.type == "identifier":
            res = Parser.tokens.actual.value
            node = Identifier(res, [])
            Parser.tokens.selectNext()
            return node

        elif Parser.tokens.actual.type == "plus" or Parser.tokens.actual.type == "minus" or Parser.tokens.actual.type == "not":
            if Parser.tokens.actual.type == "plus":
                Parser.tokens.selectNext()
                node = Parser.parseFactor()
                node = UnOp("+", [node])
                return node
            if Parser.tokens.actual.type == "minus":
                Parser.tokens.selectNext()
                node = Parser.parseFactor()
                node = UnOp("-", [node])
                return node
            else:
                Parser.tokens.selectNext()
                node = Parser.parseFactor()
                node = UnOp("!", [node])
                return node   

        elif Parser.tokens.actual.type == "lpar":
            Parser.tokens.selectNext()
            res = Parser.parseOrExpression()
            if Parser.tokens.actual.type == "rpar":
                Parser.tokens.selectNext()
                return res
            else:
                raise ValueError("Não fechou o parentesis", Parser.tokens.actual.type)

        elif Parser.tokens.actual.type == READLN:
            Parser.tokens.selectNext()
            if Parser.tokens.actual.type == "lpar":
                Parser.tokens.selectNext()
                res = Readln('', [])
                if Parser.tokens.actual.type == "rpar":
                    Parser.tokens.selectNext()
                    return res
            else:
                raise ValueError("Não fechou o parentesis")
        
        elif Parser.tokens.actual.type == TRUE or Parser.tokens.actual.type == FALSE:
            node = BoolVal(Parser.tokens.actual.value, [])
            Parser.tokens.selectNext()
            return node

        elif Parser.tokens.actual.type == STRING:
            node = StringVal(Parser.tokens.actual.value, [])  
            Parser.tokens.selectNext() 
            return node
        else:
            raise ValueError("Operadoração inválida")        
            
    @staticmethod
    def parseTerm():
        node = Parser.parseFactor()
        while Parser.tokens.actual.type == "mult" or Parser.tokens.actual.type == "div":
            if Parser.tokens.actual.type == "mult":
                Parser.tokens.selectNext()
                node = BinOp("*", [node, Parser.parseFactor()])
            elif Parser.tokens.actual.type == "div":
                Parser.tokens.selectNext()
                node = BinOp("/", [node, Parser.parseFactor()])
            else:
                raise ValueError("Simbolo invalido")
        return node

    @staticmethod
    def parseExpression():
        node = Parser.parseTerm()
        while Parser.tokens.actual.type == "plus" or Parser.tokens.actual.type == "minus":
            if Parser.tokens.actual.type == "plus":
                Parser.tokens.selectNext()
                node = BinOp("+", [node, Parser.parseTerm()])

            elif Parser.tokens.actual.type == "minus":
                Parser.tokens.selectNext()
                node = BinOp("-", [node, Parser.parseTerm()])
            else:
                raise ValueError("Simbolo invalido")
        return node

    @staticmethod
    def parseRealExpression():
        node = Parser.parseExpression()
        while Parser.tokens.actual.type == "maior" or Parser.tokens.actual.type == "menor":
            if Parser.tokens.actual.type == "maior":
                Parser.tokens.selectNext()
                node = BinOp(">", [node, Parser.parseExpression()])
            elif Parser.tokens.actual.type == "menor":
                Parser.tokens.selectNext()
                node = BinOp("<", [node, Parser.parseExpression()])
        return node
        

    @staticmethod
    def parseEqualExpression():
        node = Parser.parseRealExpression()
        while Parser.tokens.actual.type == "equal":
            if Parser.tokens.actual.type == "equal":
                Parser.tokens.selectNext()
                node = BinOp("==", [node, Parser.parseRealExpression()])
        return node    

    @staticmethod
    def parseAndExpression():
        node = Parser.parseEqualExpression()
        while Parser.tokens.actual.type == "and":
            if Parser.tokens.actual.type == "and":
                Parser.tokens.selectNext()
                node = BinOp("&&", [node, Parser.parseEqualExpression()])
        return node

    @staticmethod
    def parseOrExpression():
        node = Parser.parseAndExpression()
        while Parser.tokens.actual.type == "or":
            if Parser.tokens.actual.type == "or":
                Parser.tokens.selectNext()
                node = BinOp("||", [node, Parser.parseAndExpression()])
        return node                 

    @staticmethod
    def run(origin):
        Parser.tokens = Tokenizer(origin, None)
        Parser.tokens.selectNext()
        res = Parser.block()
        if Parser.tokens.actual.type != 'eof':
            raise ValueError('Entrada inválida. Último token não é o EOF.')   
        ST = SymbolTable()
        res.evaluate(ST)
        return res

class PrePro():
    @staticmethod
    def filter(entrada):
        filtro = re.sub(r"/\*(.|\n)*?\*/", "", entrada)
        return filtro  

class Assembler:
    stringAsm = ""

    @staticmethod
    def AddString(string):
        Assembler.stringAsm += string + "\n"

    @staticmethod
    def Write():
        begin = """; constantes
SYS_EXIT equ 1
SYS_READ equ 3
SYS_WRITE equ 4
STDIN equ 0
STDOUT equ 1
True equ 1
False equ 0

segment .data

segment .bss  ; variaveis
  res RESB 1

section .text
  global _start

print:  ; subrotina print

  PUSH EBP ; guarda o base pointer
  MOV EBP, ESP ; estabelece um novo base pointer

  MOV EAX, [EBP+8] ; 1 argumento antes do RET e EBP
  XOR ESI, ESI

print_dec: ; empilha todos os digitos
  MOV EDX, 0
  MOV EBX, 0x000A
  DIV EBX
  ADD EDX, '0'
  PUSH EDX
  INC ESI ; contador de digitos
  CMP EAX, 0
  JZ print_next ; quando acabar pula
  JMP print_dec

print_next:
  CMP ESI, 0
  JZ print_exit ; quando acabar de imprimir
  DEC ESI

  MOV EAX, SYS_WRITE
  MOV EBX, STDOUT

  POP ECX
  MOV [res], ECX
  MOV ECX, res

  MOV EDX, 1
  INT 0x80
  JMP print_next

print_exit:
  POP EBP
  RET

; subrotinas if/while
binop_je:
  JE binop_true
  JMP binop_false

binop_jg:
  JG binop_true
  JMP binop_false

binop_jl:
  JL binop_true
  JMP binop_false

binop_false:
  MOV EBX, False
  JMP binop_exit
binop_true:
  MOV EBX, True
binop_exit:
  RET

_start:

  PUSH EBP ; guarda o base pointer
  MOV EBP, ESP ; estabelece um novo base pointer

  ; codigo gerado pelo compilador

"""
        end = """; interrupcao de saida
    POP EBP
    MOV EAX, 1
    INT 0x80
    """
        with open("program.asm", "w") as file:
            file.write(begin+Assembler.stringAsm+end)      
        
class SymbolTable():
    def __init__(self):
        self.table = {}
        self.shift = 0

    def getter(self, chave):
        if chave in self.table.keys():
            tupla = tuple(self.table.get(chave))
            return tupla

        else:
            raise ValueError("Chave {} não localizada na Tabela de Símbolos".format(chave))
    
    def setter(self, chave, valor): #((nome da variável, [tipo, "TYPE"]), value)
        if chave in self.table.keys():
            self.table[chave][0] = valor
        else:
            raise ValueError("Chave {} não existe na Tabela de Símbolos".format(chave))
        return

    def creator(self, chave, tipo):
        self.shift+=4
        if chave in self.table.keys():
            raise ValueError("Chave {} já existe na Tabela de Símbolos".format(chave))
        else:
            self.table[chave] = [None, tipo, self.shift]
            return   
            
class Node():
    i = 0
    def __init__(self, valor, filho):
        self.valor = valor
        self.filho = filho

    def evaluate(self, ST):
        pass

    def newId():
        Node.i +=1
        return Node.i

class BinOp(Node):
    def __init__(self, valor, filho):
        super().__init__(valor, filho)
        self.id = Node.newId()

    def evaluate(self, ST):   
        f0 = self.filho[0].evaluate(ST) 
        Assembler.AddString("PUSH EBX")
        f1 = self.filho[1].evaluate(ST) 
        Assembler.AddString("POP EAX")

        if self.valor == "+":
            if f0[1] != STRING or f1[1] != STRING:
                Assembler.AddString("ADD EAX, EBX")
                Assembler.AddString("MOV EBX, EAX")
                return (f0[0] + f1[0], INT)
            raise ValueError("Tipos incompatíveis")

        elif self.valor == "-":
            if f0[1] == STRING or f1[1] == STRING:
                raise ValueError("Tipos incompatíveis")
            Assembler.AddString("SUB EAX, EBX")
            Assembler.AddString("MOV EBX, EAX")    
            return (f0[0] - f1[0], INT)

        elif self.valor == "*":
            if f0[1] == STRING or f1[1] == STRING:
                raise ValueError("Tipos incompatíveis")
            Assembler.AddString("IMUL EBX")    
            Assembler.AddString("MOV EBX, EAX")
            return (f0[0] * f1[0], INT)

        elif self.valor == "/":
            if f0[1] == STRING or f1[1] == STRING:
                raise ValueError("Tipos incompatíveis")
            Assembler.AddString("IDIV EBX")
            Assembler.AddString("MOV EBX, EAX")    
            return (f0[0] // f1[0], INT)

        elif self.valor == ">":
            if f0[1] == STRING or f1[1] == STRING:
                raise ValueError("Tipos incompatíveis")
            Assembler.AddString("CMP EAX, EBX")
            Assembler.AddString("CALL binop_jg")    
            if f0[0] > f1[0]:
                return (1, BOOL)    
            else:
                return (0, BOOL)    

        elif self.valor == "<":
            if f0[1] == STRING or f1[1] == STRING:
                raise ValueError("Tipos incompatíveis")
            Assembler.AddString("CMP EAX, EBX")
            Assembler.AddString("CALL binop_jl")    
            if f0[0] < f1[0]:
                return (1, BOOL)    
            else:
                return (0, BOOL) 

        elif self.valor == "==":
            Assembler.AddString("CMP EAX, EBX")
            Assembler.AddString("CALL binop_je")
            if f0[0] == f1[0]:
                return (1, BOOL)
            else:
                return (0, BOOL)   

        elif self.valor == "&&":
            if f0[1] == STRING or f1[1] == STRING:
                raise ValueError("Tipos incompatíveis")
            Assembler.AddString("AND EBX, EAX")    
            if f0[0] and f1[0]:
                return (1, BOOL)    
            else:
                return (0, BOOL) 
   
        elif self.valor == "||":
            if f0[1] == STRING or f1[1] == STRING:
                raise ValueError("Tipos incompatíveis")
            Assembler.AddString("OR EBX, EAX")    
            if f0[0] or f1[0]:
                return (1, BOOL)    
            else:
                return (0, BOOL) 

class UnOp(Node):
    def __init__(self, valor, filho):
        super().__init__(valor, filho)  
        self.id = Node.newId()

    def evaluate(self, ST):
        filho = self.filho[0].evaluate(ST)

        if filho[1] == INT:
            if self.valor == "-":
                Assembler.AddString("MOV EAX, {}".format(filho[0]))
                Assembler.AddString("MOV EBX, -1")
                Assembler.AddString("IMUl EBX")
                Assembler.AddString("MOV EBX, EAX")
                return (-filho[0], INT)
            if self.valor == "+":
                Assembler.AddString("ADD EBX, 0")
                return (filho[0], INT)
        elif filho[1] == BOOL:        
            if self.valor == "!":
                Assembler.AddString("NEG EBX")
                return (not filho[0], BOOL)     
                

# class Type(Node):
#     def __init__(self, valor, filho):
#         super().__init__(valor, filho)  

#     def evaluate(self, ST):
#         return(self.valor)                   

class IntVal(Node):
    def __init__(self, valor, filho):
        super().__init__(valor, filho)  
        self.id = Node.newId()

    def evaluate(self, ST):
        Assembler.AddString("MOV EBX, {}".format(self.valor))
        return (self.valor, INT)

class StringVal(Node):
    def __init__(self, valor, filho):
        super().__init__(valor, filho)  

    def evaluate(self, ST):
        return (self.valor, STRING)        

class BoolVal(Node):
    def __init__(self, valor, filho):
        super().__init__(valor, filho)  

    def evaluate(self, ST):
        if self.valor == "false":
            Assembler.AddString("MOV EBX, {}".format(0))
            return (0, BOOL)
        elif self.valor == "true":
            Assembler.AddString("MOV EBX, {}".format(1))
            return (1, BOOL)

class NoOp(Node):
    def __init__(self):
        pass  

    def evaluate(self, ST):
        pass                                    

class Identifier(Node):
    def __init__(self, valor, filho):
        super().__init__(valor, filho)  

    def evaluate(self, ST):
        Assembler.AddString("MOV EBX, [EBP-{}]".format(ST.getter(self.valor)[2]))
        st = ST.getter(self.valor)
        return st

class Assignment(Node):
    def __init__(self, valor, filho):
        super().__init__(valor, filho)  

    def evaluate(self, ST):
        tipo = ST.getter(self.filho[0].valor)[1] #Declaração -> (nome da variável, [tipo, "TYPE"])
        tupla = self.filho[1].evaluate(ST) #variável (valor, tipo)
        if tipo == tupla[1]:
            Assembler.AddString("MOV [EBP-{}], EBX".format(ST.getter(self.filho[0].valor)[2]))
            ST.setter(self.filho[0].valor, tupla[0]) #(nome da variável, value)
        elif(tupla[1] == "int" and tipo == "bool"):
            Assembler.AddString("MOV [EBP-{}], EBX".format(ST.getter(self.filho[0].valor)[2]))
            if tupla[0] == 0:
                ST.setter(self.filho[0].valor, 0)
            else: 
                ST.setter(self.filho[0].valor, 1)    
            pass
        elif(tupla[1] == "bool" and tipo == "int"):
            Assembler.AddString("MOV [EBP-{}], EBX".format(ST.getter(self.filho[0].valor)[2]))
            ST.setter(self.filho[0].valor, tupla[0])
            pass
        else:
            raise ValueError ("Variável não compatível com o tipo declarado.") 

class VarDec(Node):
    def __init__(self, valor, filho):
        super().__init__(valor, filho)  

    def evaluate(self, ST):
        ST.creator(self.filho[0].valor, self.filho[1])  
        Assembler.AddString("PUSH DWORD 0")                  

class Block(Node):
    def __init__(self, valor, filho):
        super().__init__(valor, filho)  

    def evaluate(self, ST):
        for node in self.filho:
            node.evaluate(ST)   

class Println(Node):
    def __init__(self, valor, filho):
        super().__init__(valor, filho)  

    def evaluate(self, ST):
        res = self.filho[0].evaluate(ST)
        if res[1] == BOOL:
            if res[0] == 0:
                print("false")
            else:
                print("true")    
        else:
            print(res[0])  
        Assembler.AddString("PUSH EBX")
        Assembler.AddString("CALL print")
        Assembler.AddString("POP EBX")          

class Readln(Node):
    def __init__(self, valor, filho):
        super().__init__(valor, filho)

    def evaluate(self, ST):
        entrada = input()
        return (int(entrada), INT)

class While(Node):
    def __init__(self, valor, filho):
        super().__init__(valor, filho)  
        self.id = Node.newId()

    def evaluate(self, ST):
        Assembler.AddString("LOOP_34:")
        self.filho[0].evaluate(ST)
        Assembler.AddString("CMP EBX, False")
        Assembler.AddString("JE EXIT_34") 
        self.filho[1].evaluate(ST) 
        Assembler.AddString("JMP LOOP_34")
        Assembler.AddString("EXIT_34:")

class If(Node):
    def __init__(self, valor, filho):
        super().__init__(valor, filho) 
        self.id = Node.newId() 

    def evaluate(self, ST):
        Assembler.AddString("if_{}:".format(self.id))
        filho = self.filho[0].evaluate(ST)
        Assembler.AddString("CMP EBX, False")
        if filho[1] == STRING:
            raise ValueError("Para essa operação string não é permitido")
        else:
            if len(self.filho) == 3:
                Assembler.AddString("JE Else_{}".format(self.id))
            else:
                Assembler.AddString("JE EndIf_{}".format(self.id))
                
            self.filho[1].evaluate(ST)
            Assembler.AddString("JMP EndIf_{}".format(self.id))
 
            if len(self.children) == 3:
                Assembler.AddString("Else_{}:".format(self.id))
                self.children[2].evaluate(ST)

            Assembler.AddString("EndIf_{}:".format(self.id))
            # if filho[0] == True or filho[0] > 0:
            #     return self.filho[1].evaluate(ST)
            # elif len(self.filho) == 3:
            #     Assembler.AddString("JE else_{}".format(self.id))
            #     return self.filho[2].evaluate(ST)              


def main():
    with open(f"{arquivo}", "r") as file:
        conta = file.read()    
    codigo = PrePro.filter(conta)
    Parser.run(codigo)
    Assembler.Write()
    

if  __name__ =='__main__':main()