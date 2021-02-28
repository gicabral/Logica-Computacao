import sys

conta = sys.argv[1]


def calculadora(s):
    #inverter a string
    s = list(s[::-1])

    #verificar se um operador não está no final ou no começo da string
    if s[0] == "-" or s[0] == "+" or s[-1] == "-" or s[-1] == "+":
        raise ValueError
    #verifica se não foi colocado nenhum operador
    if "+" not in s and "-" not in s:
        raise ValueError

    def valor():
        valor = 0
        cont = 0
        #enquanto o caracter for um digito ele e não um operador ele fica no loop
        while s and s[-1].isdigit():
            #multiplica por 10 para pegar números compostos
            valor *= 10
            #adiciona o que saiu no pop ao valor
            valor += int(s.pop())
        #para nao permitir casos como "1++1"
        for i in s:
            if i == "+" or i == "-":
                cont += 1
            if i.isdigit():
                cont = 0
            #verifica se tem dois operadores seguidos
            if cont == 2:
                raise ValueError
        return valor

    def termo():
        t = valor()
        #retorna o valor
        return t

    result = termo()
    while s:
        op, t = s.pop(), termo()
        #se o operador for +, realiza a soma
        if op == "+":
            result += t
        #senão, realiza a subtração
        else:
            result -= t
    return result


resultado = calculadora(conta)
print(resultado)