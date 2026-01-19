from analex import lexer
from anasin import parser
import sys
class Cores:
    VERDE = '\033[92m'
    AZUL = '\033[94m'
    AMARELO = '\033[93m'
    VERMELHO = '\033[91m'
    RESET = '\033[0m'
    NEGRITO = '\033[1m'

# Para ler de um ficheiro específico:
with open('pascal/teste4.pp', 'r', encoding='utf-8') as f:
    conteudo = f.read()

try:
    import logging

    # Configurar um logger que escreve para um ficheiro
    logging.basicConfig(
        level = logging.DEBUG,
        filename = "parselog.txt",   # Nome do ficheiro onde vai ficar o log
        filemode = "w",              # "w" para limpar o ficheiro cada vez que corres
        format = "%(message)s"
    )

    logger = logging.getLogger()

    # ... o teu código de leitura do ficheiro ...

    # No parse, passa o logger que acabaste de criar
    parser.parse(conteudo, debug=logger)
except Exception as e:
    print(f'{Cores.VERMELHO}{e}{Cores.RESET}')
    exit()