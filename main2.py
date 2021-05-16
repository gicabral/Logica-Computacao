import re
import sys

arquivo = sys.argv[1]

reserved = ["println", "readln", "while", "if", "else"]
PRINTLN, READLN, WHILE, IF, ELSE  = reserved

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
                self.origin)) and (self.origin[self.position] == " " or self.origin[self.position] == "\n"):
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

        
class SymbolTable():
    def __init__(self):
        self.table = {}

    def getter(self, key):
        if key in self.table.keys():
            res = self.table.get(key)    
            return res
        else:
            raise ValueError("key não está na SymbolTable") 

    def setter(self, key, value):  
        self.table.update({key: value})         

class Node():
    def __init__(self, valor, filho):
        self.valor = valor
        self.filho = filho

    def evaluate(self, ST):
        pass

class BinOp(Node):
    def __init__(self, valor, filho):
        super().__init__(valor, filho)

    def evaluate(self, ST):    
        if self.valor == "+":
            return self.filho[0].evaluate(ST) + self.filho[1].evaluate(ST)
        elif self.valor == "-":
            return self.filho[0].evaluate(ST) - self.filho[1].evaluate(ST)
        elif self.valor == "*":
            return self.filho[0].evaluate(ST) * self.filho[1].evaluate(ST)
        elif self.valor == "/":
            return self.filho[0].evaluate(ST) // self.filho[1].evaluate(ST) 
        elif self.valor == ">":
            return self.filho[0].evaluate(ST) > self.filho[1].evaluate(ST)
        elif self.valor == "<":
            return self.filho[0].evaluate(ST) < self.filho[1].evaluate(ST)
        elif self.valor == "==":
            return self.filho[0].evaluate(ST) == self.filho[1].evaluate(ST)
        elif self.valor == "&&":
            return self.filho[0].evaluate(ST) and self.filho[1].evaluate(ST)
        elif self.valor == "||":
            return self.filho[0].evaluate(ST) or self.filho[1].evaluate(ST)                          

class UnOp(Node):
    def __init__(self, valor, filho):
        super().__init__(valor, filho)  

    def evaluate(self, ST):
        if self.valor == "-":
            res = self.filho[0].evaluate(ST)
            return -res
        if self.valor == "+":
            res = self.filho[0].evaluate(ST)
            return res
        else:
            return not self.filho[0].evaluate(ST)     

class IntVal(Node):
    def __init__(self, valor, filho):
        super().__init__(valor, filho)  

    def evaluate(self, ST):
        return self.valor

class NoOp(Node):
    def __init__(self):
        pass  

    def evaluate(self, ST):
        pass                                    

class Identifier(Node):
    def __init__(self, valor, filho):
        super().__init__(valor, filho)  

    def evaluate(self, ST):
        st = ST.getter(self.valor)
        return st

class Assignment(Node):
    def __init__(self, valor, filho):
        super().__init__(valor, filho)  

    def evaluate(self, ST):
        ST.setter(self.filho[0].valor, self.filho[1].evaluate(ST))   

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
        print(self.filho[0].evaluate(ST)) 

class Readln(Node):
    def __init__(self, valor, filho):
        super().__init__(valor, filho)  

    def evaluate(self, ST):
        entrada = input()
        return int(entrada)

class While(Node):
    def __init__(self, valor, filho):
        super().__init__(valor, filho)  

    def evaluate(self, ST):
        while self.filho[0].evaluate(ST) == True: 
            self.filho[1].evaluate(ST) 

class If(Node):
    def __init__(self, valor, filho):
        super().__init__(valor, filho)  

    def evaluate(self, ST):
        if self.filho[0].evaluate(ST) == True:
            return self.filho[1].evaluate(ST)
        elif len(self.filho) == 3:
            return self.filho[2].evaluate(ST)              


def main():
    with open(f"{arquivo}", "r") as file:
        conta = file.read()    
    codigo = PrePro.filter(conta)
    Parser.run(codigo)
    

if  __name__ =='__main__':main()