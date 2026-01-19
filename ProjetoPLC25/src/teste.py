from analex import lexer
import sys
class Cores:
    VERDE = '\033[92m'
    AZUL = '\033[94m'
    AMARELO = '\033[93m'
    VERMELHO = '\033[91m'
    RESET = '\033[0m'
    NEGRITO = '\033[1m'

# Para ler de um ficheiro específico:
with open('pascal/teste3.pp', 'r', encoding='utf-8') as f:
    conteudo = f.read()

lexer.input(conteudo)

try:
    for tok in lexer:
        print(tok)
except Exception as e:
    print(f'{Cores.VERMELHO}{e}{Cores.RESET}')
    exit()


print(f'{Cores.VERDE}TOKENS APANHADOS COM {Cores.NEGRITO}SUCESSO{Cores.RESET}')