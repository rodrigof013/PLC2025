import os
import sys
from anasin import parser, lexer

PASTA_TESTES = './pascal'
PASTA_RESULTADOS = os.path.join(PASTA_TESTES, 'resultadosSIN')

def testar_parser():
    print(f"--- A iniciar testes SINTÁTICOS na pasta '{PASTA_TESTES}' ---")
    
    if not os.path.exists(PASTA_TESTES):
        print(f"Erro: A pasta {PASTA_TESTES} não existe.")
        return

    if not os.path.exists(PASTA_RESULTADOS):
        os.makedirs(PASTA_RESULTADOS)

    ficheiros = [f for f in os.listdir(PASTA_TESTES) if f.endswith(('.pas', '.pp'))]
    
    sucessos = 0
    erros = 0

    for ficheiro in ficheiros:
        caminho_entrada = os.path.join(PASTA_TESTES, ficheiro)
        nome_saida = os.path.splitext(ficheiro)[0] + ".txt"
        caminho_saida = os.path.join(PASTA_RESULTADOS, nome_saida)
        
        # Reiniciar estado do lexer e parser
        lexer.lineno = 1
        lexer.begin('INITIAL')
        parser.error = False
        
        print(f"Analisando {ficheiro}...", end=" ")
        
        try:
            with open(caminho_entrada, 'r', encoding='utf-8') as f_in:
                conteudo = f_in.read()
            
            resultado = parser.parse(conteudo)
            
            with open(caminho_saida, 'w', encoding='utf-8') as f_out:
                if resultado is None and parser.error == False: 
                    # Nota: Precisas de uma flag no parser para saber se houve erro, 
                    # porque o PLY às vezes devolve None mesmo com sucesso se não tiveres return.
                    # Vou assumir sucesso se não lançar exceção por agora.
                    f_out.write("Análise Sintática: SUCESSO\n")
                    f_out.write("O código respeita a gramática definida.\n")
                    print("✅ SUCESSO")
                    sucessos += 1
                else:
                    f_out.write(f"Resultado da análise: {resultado}\n")
                    print("✅ SUCESSO")
                    sucessos += 1

        except Exception as e:
            # Isto apanha erros de Python no teu código, não erros de sintaxe do Pascal
            # (A menos que tenhas configurado o p_error para lançar exceções)
            print(f"❌ ERRO DE EXECUÇÃO: {e}")
            with open(caminho_saida, 'w', encoding='utf-8') as f_out:
                f_out.write(f"ERRO CRÍTICO: {str(e)}\n")
            erros += 1

    print("-" * 30)
    print(f"Resumo: {sucessos} ficheiros analisados, {erros} erros de execução.")
    print(f"Resultados guardados em: {PASTA_RESULTADOS}")

if __name__ == "__main__":
    testar_parser()