import sys
import re

conta = sys.argv[1]


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

        else:
            raise ValueError("Simbolo desconhecido")


class PrePro():
    @staticmethod
    def filter(entrada):
        filtro = re.sub("", "", entrada)  #apenas para o meu terminal
        return filtro


class Parser:
    @staticmethod
    def parseTerm():
        res = Parser.tokens.actual.value
        Parser.tokens.selectNext()
        while Parser.tokens.actual.type == "mult" or Parser.tokens.actual.type == "div":
            if Parser.tokens.actual.type == "mult":
                Parser.tokens.selectNext()
                if Parser.tokens.actual.type == "int":
                    res = res * Parser.tokens.actual.value
                else:
                    raise ValueError(
                        "Dois operadores seguidos ou operador isolado")
            elif Parser.tokens.actual.type == "div":
                Parser.tokens.selectNext()
                if Parser.tokens.actual.type == "int":
                    res = res // Parser.tokens.actual.value
                else:
                    raise ValueError(
                        "Dois operadores seguidos ou operador isolado")
            else:
                raise ValueError("Simbolo invalido")
            Parser.tokens.selectNext()  #4/2/2
        return res

    @staticmethod
    def parseExpression():
        res = Parser.parseTerm()
        while Parser.tokens.actual.type == "plus" or Parser.tokens.actual.type == "minus":
            if Parser.tokens.actual.type == "plus":
                Parser.tokens.selectNext()
                if Parser.tokens.actual.type == "int":
                    res = res + Parser.parseTerm()
                else:
                    raise ValueError(
                        "Dois operadores seguidos ou operador isolado")
            elif Parser.tokens.actual.type == "minus":
                Parser.tokens.selectNext()
                if Parser.tokens.actual.type == "int":
                    res = res - Parser.parseTerm()
                else:
                    raise ValueError(
                        "Dois operadores seguidos ou operador isolado")
            else:
                raise ValueError("Simbolo invalido")
        return res

    @staticmethod
    def run(origin):
        Parser.tokens = Tokenizer(origin, None)
        Parser.tokens.selectNext()
        res = Parser.parseExpression()
        if Parser.tokens.actual.type != "eof":
            raise ValueError("Não chegou no final da string")
        print(res)
        return res


def main():
    codigo = PrePro.filter(conta)
    Parser.run(codigo)


if __name__ == '__main__': main()
