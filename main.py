import sys
import re

arquivo = sys.argv[1]

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
                self.origin)) and (self.origin[self.position] == " "):
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

        else:
            raise ValueError("Simbolo desconhecido")


class PrePro():
    @staticmethod
    def filter(entrada):
        filtro = re.sub(r"/\*(.|\n)*?\*/", "", entrada)
        return filtro     

class Parser:
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
    def parseFactor():
        if Parser.tokens.actual.type == "int":
            node = Parser.tokens.actual.value
            node = IntVal(node, [])
            Parser.tokens.selectNext()
            return node
        elif Parser.tokens.actual.type == "plus" or Parser.tokens.actual.type == "minus":
            if Parser.tokens.actual.type == "plus":
                Parser.tokens.selectNext()
                node = Parser.parseFactor()
                node = UnOp("+", [node])
                return node
            else:
                Parser.tokens.selectNext()
                node = Parser.parseFactor()
                node = UnOp("-", [node])
                return node

        elif Parser.tokens.actual.type == "lpar":
            Parser.tokens.selectNext()
            res = Parser.parseExpression()
            if Parser.tokens.actual.type == "rpar":
                Parser.tokens.selectNext()
                return res
            else:
                raise ValueError("Não fechou o parentesis")

        else:
            raise ValueError("Operadoração inválida")

    @staticmethod
    def run(origin):
        Parser.tokens = Tokenizer(origin, None)
        Parser.tokens.selectNext()
        node = Parser.parseExpression()
        if Parser.tokens.actual.type != "eof":
            raise ValueError("Não chegou no final da string")
        print(node.evaluate())
        return node

class Node():
    def __init__(self, valor, filho):
        self.valor = valor
        self.filho = filho

    def evaluate(self):
        pass

class BinOp(Node):
    def __init__(self, valor, filho):
        super().__init__(valor, filho)

    def evaluate(self):    
        if self.valor == "+":
            return self.filho[0].evaluate() + self.filho[1].evaluate()
        elif self.valor == "-":
            return self.filho[0].evaluate() - self.filho[1].evaluate()
        elif self.valor == "*":
            return self.filho[0].evaluate() * self.filho[1].evaluate()
        elif self.valor == "/":
            return self.filho[0].evaluate() // self.filho[1].evaluate()           

class UnOp(Node):
    def __init__(self, valor, filho):
        super().__init__(valor, filho)  

    def evaluate(self):
        if self.valor == "-":
            res = self.filho[0].evaluate()
            return -res
        else:
            res = self.filho[0].evaluate()
            return res

class IntVal(Node):
    def __init__(self, valor, filho):
        super().__init__(valor, filho)  

    def evaluate(self):
        return self.valor

class NoOp(Node):
    def __init__(self, valor, filho):
        super().__init__(valor, filho)  

    def evaluate(self):
        pass                                    


     

def main():
    with open(f"{arquivo}", "r+") as file:
        conta = file.read()
    codigo = PrePro.filter(conta)
    Parser.run(codigo)
    

if __name__ == '__main__': main()
