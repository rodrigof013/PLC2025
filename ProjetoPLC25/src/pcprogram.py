from anasin import parser, lexer, ErroSintaxe
from anasem import AnalisadorSemantico
from geraCod import GeraCod
import argparse
import sys
import os
import webbrowser
import pyperclip

def ler_stdin():
    linhas = []
    try:
        while True:
            linha = input(">>> ")
            linhas.append(linha)
    except EOFError:
        pass
    return "\n".join(linhas)

def compilar(codigo, verbose=False):
    try:
        ast = parser.parse(codigo, lexer=lexer)
        if verbose:
            print("Parsing OK")
    except ErroSintaxe:
        return None

    analisador = AnalisadorSemantico()
    tabela = analisador.realizar_analise(ast)
    if analisador.erros:
        return None
    if verbose:
        print("Análise semântica OK")

    gerador = GeraCod(ast, tabela)
    codigo_vm = gerador.gera_codigo()
    if verbose:
        print("Geração de código OK")
    
    return codigo_vm

def main():
    arg_parser = argparse.ArgumentParser(description="Compilador Pascal Standard")
    arg_parser.add_argument('input', nargs='?', help='ficheiro de entrada (.pp)')
    arg_parser.add_argument('-o', '--output', help='ficheiro de saída (.vm)')
    arg_parser.add_argument('-v', '--verbose', action='store_true', help='modo verbose')
    arg_parser.add_argument('-c', '--clipboard', action='store_true', help='copia para clipboard e abre a VM')
    arg_parser.add_argument('-q', '--quick', action='store_true', help='como -c mas também guarda ficheiro .vm <--- RECOMENDO')
    args = arg_parser.parse_args()

    if args.input:
        if not os.path.exists(args.input):
            print(f"Erro: O ficheiro '{args.input}' não existe.", file=sys.stderr)
            sys.exit(1)
        with open(args.input, 'r', encoding='utf-8') as f:
            codigo = f.read()
    else:
        codigo = ler_stdin()
        if not codigo.strip():
            sys.exit(0)

    resultado = compilar(codigo, args.verbose)
    
    if resultado is None:
        sys.exit(1)

    if args.quick or args.clipboard:
        pyperclip.copy(resultado)
        webbrowser.open('https://ewvm.epl.di.uminho.pt')
        if args.verbose:
            print("Código copiado e VM aberta")

    if args.quick and args.input:
        nome_base = os.path.splitext(os.path.basename(args.input))[0]
        with open(f"{nome_base}.vm", 'w', encoding='utf-8') as f:
            f.write(resultado)
        if args.verbose:
            print(f"Código gerado em: {nome_base}.vm")
    elif args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(resultado)
        if args.verbose:
            print(f"Código gerado em: {args.output}")
    elif not args.quick and not args.clipboard:
        print(resultado)

if __name__ == "__main__":
    main()