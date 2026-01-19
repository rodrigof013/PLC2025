from analex import lexer
from anasin import parser
from rich import print
from anasem import AnalisadorSemantico
from geraCod import GeraCod
import sys
import pyperclip

class Cores:
    VERDE = '\033[92m'
    AZUL = '\033[94m'
    AMARELO = '\033[93m'
    VERMELHO = '\033[91m'
    RESET = '\033[0m'
    NEGRITO = '\033[1m'

# Para ler de um ficheiro específico:
with open('pascal/teste2.pp', 'r', encoding='utf-8') as f:
    conteudo = f.read()

    ast = parser.parse(conteudo)

    anasem = AnalisadorSemantico()
    print(ast)
    print('A começar análise semântica...')
    anasem.realizar_analise(ast)
    # print('\n',"TABELA DE SIMBOLOS",'\n')
    print(anasem.tabela_simbolos)
    geraC=GeraCod(ast,anasem.tabela_simbolos)
    geraC.gera_codigo()
    codigo_gerado = '\n'.join(geraC.lCod)
    print(codigo_gerado)
    pyperclip.copy(codigo_gerado)
    print('Código copiado para a área de transferência!')
    print('Se não mostrou erros então tá tudo mano!')
