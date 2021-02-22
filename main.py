import sys

conta = sys.argv[1]


def calculadora(s):
    #inverter a string
    s = list(s[::-1])

    #verificar se um operador não está no final da string
    if s[0] == "-" or s[0] == "+":
        erro = "Formato errado"
        return erro

    def valor():
        valor = 0
        #enquanto o caracter for um digito ele e não um operador ele fica no loop
        while s and s[-1].isdigit():
            #multiplica por 10 para pegar números compostos
            valor *= 10
            #adiciona o que esta saiu no pop ao valor
            valor += int(s.pop())
        return valor

    def termo():
        t = valor()
        #retorna o valor
        return t

    result = termo()
    while s:
        op, t = s.pop(), termo()
        if op == "+":
            result += t
        else:
            result -= t
    return result


resultado = calculadora(conta)
print(resultado)