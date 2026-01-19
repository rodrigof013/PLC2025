from Cores import Cores

class Erros:
    FLAG_WARNINGS = True 

    MENSAGENS = {
        'VAR_EXISTE': "A variável '{nome}' já foi declarada neste escopo.",
        'VAR_N_EXISTE': "A variável '{nome}' não foi declarada.",
        'CONST_EXISTE': "A constante '{nome}' já foi definida.",
        'TIPO_INCOMPATIVEL': "Tipo incompatível: esperava '{esperado}', recebeu '{recebido}'.",
        'FUNCAO_NAO_DECLARADA': "A função '{nome}' não foi declarada.",
        'NUM_ARGS': "Número de argumentos inválido para '{nome}': esperava {esperado}, recebeu {recebido}.",
        'ARG_TIPO': "Argumento '{param}' com tipo inválido: esperava '{esperado}', recebeu '{recebido}'.",
        # Erros de geração de código
        'CAMPO_N_EXISTE': "O campo '{nome}' não existe no record.",
        'TIPO_N_IMPLEMENTADO': "O tipo '{nome}' não está implementado na geração de código.",
        # Erros sintáticos
        'TOKEN_INESPERADO': "Token inesperado '{token}' (tipo: {tipo_token}).",
        'TOKEN_INESPERADO_CONTEXTO': "Token inesperado '{token}' (tipo: {tipo_token}). {contexto}",
        'EOF_INESPERADO': "Fim de ficheiro inesperado.",
        'EOF_INESPERADO_CONTEXTO': "Fim de ficheiro inesperado. {contexto}",
        'FALTA_PONTO_VIRGULA': "Esperava ';' após {elemento}.",
        'FALTA_END': "Esperava 'END' para fechar o bloco.",
        'FALTA_BEGIN': "Esperava 'BEGIN' para iniciar o bloco de código.",
        'FALTA_THEN': "Esperava 'THEN' após a condição do IF.",
        'FALTA_DO': "Esperava 'DO' após a condição do {ciclo}.",
        'EXPR_INVALIDA': "Expressão inválida.",
        'TIPO_INVALIDO': "Definição de tipo inválida.",
    }

    TIPOS = {
        'lex': 'Erro Léxico',
        'sin': 'Erro Sintático',
        'sem': 'Erro Semântico',
        'ger': 'Erro de Geração',
        'w'  : 'Aviso'
    }

    @staticmethod
    def get(tipo, linha, chave, **kwargs):
        """
        Retorna a mensagem formatada.
        Uso: Erros.get('sem', 10, 'VAR_EXISTE', nome='x')
        """
        if tipo == 'w' and not Erros.MOSTRAR_AVISOS:
            return None

        prefixo_texto = Erros.TIPOS.get(tipo, "Erro")
        cor = Cores.AMARELO if tipo == 'w' else Cores.VERMELHO
        
        template = Erros.MENSAGENS.get(chave, "Erro desconhecido.")
        
        if linha is None:
            linha = 'Indefinida'
    
        try:
            mensagem_formatada = template.format(**kwargs)
        except KeyError as e:
            mensagem_formatada = f"{template} [Falta argumento: {e}]"

        resultado = f"{cor}{prefixo_texto}: {mensagem_formatada} {Cores.NEGRITO}(Linha {linha}){Cores.RESET}"
        
        return resultado