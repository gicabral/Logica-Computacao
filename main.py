import sys

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
        else:
            raise ValueError("Simbolo desconhecido")


class Parser:
    @staticmethod
    def parseExpression():
        if Parser.tokens.actual.type == "int":
            res = Parser.tokens.actual.value
            Parser.tokens.selectNext()
            while Parser.tokens.actual.type == "plus" or Parser.tokens.actual.type == "minus":
                if Parser.tokens.actual.type == "plus":
                    Parser.tokens.selectNext()
                    if Parser.tokens.actual.type == "int":
                        res += Parser.tokens.actual.value
                    else:
                        raise ValueError("Não é um  inteiro")
                elif Parser.tokens.actual.type == "minus":
                    Parser.tokens.selectNext()
                    if Parser.tokens.actual.type == "int":
                        res -= Parser.tokens.actual.value
                    else:
                        raise ValueError("Não é um int")
                else:
                    raise ValueError("Não é plus ou minus")
                Parser.tokens.selectNext()
            if Parser.tokens.actual.type != "eof":
                raise ValueError("Não chegou no final da string")
            return res
        else:
            raise ValueError("Não é um inteiro")

    @staticmethod
    def run(origin):
        Parser.tokens = Tokenizer(origin, None)
        Parser.tokens.selectNext()
        res = Parser.parseExpression()
        print(res)
        return res


def main():
    Parser.run(conta)


if __name__ == '__main__': main()
