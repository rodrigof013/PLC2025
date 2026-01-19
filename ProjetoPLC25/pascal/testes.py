import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.analex import lexer

# Caminho para a pasta com os exemplos pascal
PASTA_TESTES = './pascal'
PASTA_RESULTADOS = os.path.join(PASTA_TESTES, 'resultadosLEX')

def testar_lexer():
    print(f"--- A iniciar testes na pasta '{PASTA_TESTES}' ---")
    
    # Verifica se a pasta de testes existe
    if not os.path.exists(PASTA_TESTES):
        print(f"Erro: A pasta {PASTA_TESTES} não existe.")
        return

    # Cria a pasta de resultados se não existir
    if not os.path.exists(PASTA_RESULTADOS):
        os.makedirs(PASTA_RESULTADOS)
        print(f"Pasta '{PASTA_RESULTADOS}' criada.")

    # Lista todos os ficheiros .pas ou .pp
    ficheiros = [f for f in os.listdir(PASTA_TESTES) if f.endswith(('.pas', '.pp'))]
    
    sucessos = 0
    erros = 0

    for ficheiro in ficheiros:
        caminho_entrada = os.path.join(PASTA_TESTES, ficheiro)
        
        # Define o nome do ficheiro de saída (ex: teste1.pas -> teste1.txt)
        nome_saida = os.path.splitext(ficheiro)[0] + ".txt"
        caminho_saida = os.path.join(PASTA_RESULTADOS, nome_saida)
        
        try:
            # Ler o ficheiro de entrada
            with open(caminho_entrada, 'r', encoding='utf-8') as f_in:
                conteudo = f_in.read()
            
            # Reinicia o lexer
            lexer.lineno = 1
            lexer.begin('INITIAL')
            lexer.input(conteudo)
            print(f"Processando {ficheiro}...", end=" ")
            
            # Abrir ficheiro de saída para escrever os tokens
            with open(caminho_saida, 'w', encoding='utf-8') as f_out:
                f_out.write(f"--- Tokens gerados para: {ficheiro} ---\n")
                
                for tok in lexer:
                    # Escreve o token no ficheiro
                    f_out.write(str(tok) + '\n')
            
            print(f"✅ Gerado: {nome_saida}")
            sucessos += 1
            
        except Exception as e:
            print(f"❌ ERRO: {e}")
            # Em caso de erro, escreve o erro no ficheiro de saída também
            with open(caminho_saida, 'w', encoding='utf-8') as f_out:
                f_out.write(f"ERRO FATAL: {str(e)}\n")
            erros += 1

    print("-" * 30)
    print(f"Resumo: {sucessos} processados com sucesso, {erros} falharam.")
    print(f"Resultados guardados em: {PASTA_RESULTADOS}")

if __name__ == "__main__":
    testar_lexer()