import ply.yacc as yacc
from analex import tokens,literals,lexer
from Erros import Erros
import sys

# Excepção personalizada para erros sintáticos (evita traceback feio)
class ErroSintaxe(Exception):
    pass

# --- Estrutura Geral ---

def p_programa(p):
    'programa : PROGRAM VARNAME ";" bloco_declaracoes bloco_main'
    p[0] = {'nome':p[2], 'decl':p[4], 'main':p[5]}

# Error production para programa sem ;
def p_programa_error_no_semicolon(p):
    'programa : PROGRAM VARNAME error'
    raise Exception(Erros.get('sin', p.lineno(2), 'FALTA_PONTO_VIRGULA', elemento='nome do programa'))

def p_bloco_declaracoes_labels(p):
    'bloco_declaracoes : bloco_declaracoes decl_labels'
    p[0] = p[1] + [p[2]]

def p_bloco_declaracoes_consts(p):
    'bloco_declaracoes : bloco_declaracoes decl_consts'
    p[0] = p[1] + [p[2]]

def p_bloco_declaracoes_types(p):
    'bloco_declaracoes : bloco_declaracoes decl_types'
    p[0] = p[1] + [p[2]]

def p_bloco_declaracoes_vars(p):
    'bloco_declaracoes : bloco_declaracoes decl_vars'
    p[0] = p[1] + [p[2]]

def p_bloco_declaracoes_rotinas(p):
    'bloco_declaracoes : bloco_declaracoes decl_rotinas'
    p[0] = p[1] + [p[2]]
    
def p_bloco_declaracoes_empty(p):
    'bloco_declaracoes : empty'
    p[0] = []

# --- Declaração de Labels ---

def p_decl_labels(p):
    'decl_labels : LABEL lista_labels ";"'
    p[0] = {'tipo': 'DECL_LABELS', 'vals': p[2]}

def p_decl_labels_empty(p):
    'decl_labels : empty'
    p[0] = []

def p_lista_labels(p):
    'lista_labels : lista_labels "," INTVALUE'
    p[0] = p[1] + [str(p[3])]

def p_lista_labels_single(p):
    'lista_labels : INTVALUE'
    p[0] = [str(p[1])]

# --- Declaração de Constantes ---

def p_decl_consts(p):
    'decl_consts : CONST lista_consts'
    p[0] = {'tipo':'DECL_CONSTS', 'vals':p[2]}

def p_decl_consts_empty(p):
    'decl_consts : empty'
    p[0] = []

def p_lista_consts(p):
    'lista_consts : lista_consts def_const'
    p[0] = p[1] + [p[2]]

def p_lista_consts_single(p):
    'lista_consts : def_const'
    p[0] = [p[1]]

def p_def_const(p):
    'def_const : VARNAME "=" valor_literal ";"'
    p[0] = {'tipo': 'DEF_CONST', 'nome': p[1], 'val': p[3], 'linha':p.lineno(1)}

# --- Declaração de Tipos ---

def p_decl_types(p):
    'decl_types : TYPE lista_types'
    p[0] = {'tipo':'DECL_TYPES', 'vals':p[2]}

def p_decl_types_empty(p):
    'decl_types : empty'
    p[0] = []

def p_lista_types(p):
    'lista_types : lista_types def_type'
    p[0] = p[1] + [p[2]]

def p_lista_types_single(p):
    'lista_types : def_type'
    p[0] = [p[1]]

def p_def_type(p):
    'def_type : VARNAME "=" definicao_tipo ";"'
    p[0] = {'tipo': 'DEF_TYPE', 'nome':p[1], 'val': p[3], 'linha':p.lineno(1)}

# --- Declaração de Variáveis ---

def p_decl_vars(p):
    'decl_vars : VAR lista_decl_vars'
    p[0] = {'tipo': 'DECL_VARS', 'vals': p[2]}

def p_decl_vars_empty(p):
    'decl_vars : empty'
    p[0] = []

def p_lista_decl_vars(p):
    'lista_decl_vars : lista_decl_vars declaracao_var'
    p[0] = p[1] + [p[2]]

def p_lista_decl_vars_single(p):
    'lista_decl_vars : declaracao_var'
    p[0] = [p[1]]

def p_declaracao_var(p):
    'declaracao_var : lista_identificadores ":" definicao_tipo ";"'
    p[0] = {'tipo': 'DECL_VAR', 'nomes': p[1], 'datatype': p[3], 'linha':p.lineno(1)}

def p_lista_identificadores(p):
    'lista_identificadores : lista_identificadores "," VARNAME'
    p[0] = p[1] + [p[3]]

def p_lista_identificadores_single(p):
    'lista_identificadores : VARNAME'
    p[0] = [p[1]]

# --- Declaração de Rotinas ---

def p_decl_rotinas(p):
    'decl_rotinas : lista_rotinas'
    p[0] = {'tipo':'DECL_ROTINAS', 'vals': p[1]}

def p_decl_rotinas_empty(p):
    'decl_rotinas : empty'
    p[0] = []

def p_lista_rotinas_func(p):
    'lista_rotinas : lista_rotinas FUNCTION VARNAME "(" lista_params ")" ":" definicao_tipo ";" bloco_declaracoes bloco_main ";"'
    p[0] = p[1] + [{'tipo': 'FUNCTION', 'nome': p[3], 'params': p[5], 'return': p[8], 'decl': p[10], 'corpo': p[11],'linha':p.lineno(2)}]

def p_lista_rotinas_proc(p):
    'lista_rotinas : lista_rotinas PROCEDURE VARNAME "(" lista_params ")" ";" bloco_declaracoes bloco_main ";"'
    p[0] = p[1] + [{'tipo': 'PROCEDURE', 'nome': p[3], 'params': p[5], 'decl': p[8], 'corpo': p[9],'linha':p.lineno(2)}]

def p_lista_rotinas_func_single(p):
    'lista_rotinas : FUNCTION VARNAME "(" lista_params ")" ":" definicao_tipo ";" bloco_declaracoes bloco_main ";"'
    p[0] = [{'tipo': 'FUNCTION', 'nome': p[2], 'params': p[4], 'retrn': p[7], 'decl': p[9], 'corpo': p[10],'linha':p.lineno(1)}]

def p_lista_rotinas_proc_single(p):
    'lista_rotinas : PROCEDURE VARNAME "(" lista_params ")" ";" bloco_declaracoes bloco_main ";"'
    p[0] = [{'tipo': 'PROCEDURE', 'nome': p[2], 'params': p[4], 'decl': p[7], 'corpo': p[8],'linha':p.lineno(1)}]

def p_lista_params(p):
    'lista_params : lista_params ";" param_group'
    p[0] = p[1] + [p[3]]

def p_lista_params_single(p):
    'lista_params : param_group'
    p[0] = [p[1]]

def p_lista_params_empty(p):
    'lista_params : empty'
    p[0] = []

def p_param_group(p):
    'param_group : lista_identificadores ":" definicao_tipo'
    p[0] = {'vars': p[1], 'tipo': p[3]}

# --- Bloco Principal e Instruções ---

def p_bloco_main_prog(p):
    'bloco_main : BEGIN lista_instrucoes ENDPROGRAM'
    p[0] = p[2]

def p_bloco_main_rout(p):
    'bloco_main : BEGIN lista_instrucoes END'
    p[0] = p[2]

# Error productions para blocos
def p_bloco_main_error_no_end(p):
    'bloco_main : BEGIN lista_instrucoes error'
    raise Exception(Erros.get('sin', p.lineno(3), 'FALTA_END'))

def p_lista_instrucoes(p):
    'lista_instrucoes : lista_instrucoes ";" instrucao'
    if p[3] is not None:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = p[1]

def p_lista_instrucoes_single(p):
    'lista_instrucoes : instrucao'
    if p[1] is not None:
        p[0] = [p[1]]
    else:
        p[0] = []

def p_lista_instrucoes_empty(p):
    'lista_instrucoes : empty'
    p[0] = []

def p_instrucao(p):
    '''instrucao : instrucao_composta
                 | instrucao_incompleta
                 | empty'''
    p[0] = p[1]

def p_instrucao_composta(p):
    '''instrucao_composta : atribuicao
                          | chamada_rotina
                          | bloco_codigo
                          | comando_case
                          | ciclo_while
                          | ciclo_repeat
                          | ciclo_for
                          | comando_goto
                          | bloco_label'''
    p[0] = p[1]

def p_instrucao_composta_if(p):
    'instrucao_composta : IF condicao THEN instrucao_composta ELSE instrucao_composta'
    p[0] = {'tipo': 'IF', 'cond': p[2], 'then': p[4], 'else': p[6], 'linha': p.lineno(1)}

# Error productions para IF
def p_instrucao_if_error_no_then(p):
    'instrucao_composta : IF condicao error'
    raise Exception(Erros.get('sin', p.lineno(1), 'FALTA_THEN'))

def p_instrucao_incompleta(p):
    '''instrucao_incompleta : IF condicao THEN instrucao
                            | IF condicao THEN instrucao_composta ELSE instrucao_incompleta'''
    if len(p) == 5:
        p[0] = {'tipo': 'IF', 'cond': p[2], 'then': p[4], 'else': None, 'linha': p.lineno(1)}
    else:
        p[0] = {'tipo': 'IF', 'cond': p[2], 'then': p[4], 'else': p[6], 'linha': p.lineno(1)}

# --- Tipos de Instruções ---

def p_bloco_label(p):
    'bloco_label : INTVALUE ":" instrucao'
    p[0] = {'tipo': 'LABEL', 'label': str(p[1]), 'instrucao': p[3]}

def p_atribuicao(p):
    'atribuicao : l_value ATR expressao'
    p[0] = {'tipo': 'ATRIBUICAO', 'var': p[1], 'val': p[3], 'linha': p.lineno(2)}

def p_l_value(p):
    '''l_value : VARNAME
               | l_value "[" lista_indices_expressao "]"
               | l_value "." VARNAME'''
    if len(p) == 2:
        p[0] = {'tipo': 'VAR', 'nome': p[1], 'linha': p.lineno(1)}
    elif p[2] == '[':
        p[0] = {'tipo': 'ARRAY_ACCESS', 'target': p[1], 'indices': p[3], 'linha': p.lineno(2)}
    else:
        p[0] = {'tipo': 'FIELD_ACCESS', 'target': p[1], 'field': p[3], 'linha': p.lineno(2)}

def p_lista_indices_expressao(p):
    '''lista_indices_expressao : lista_indices_expressao "," expressao
                               | expressao'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]

def p_chamada_rotina(p):
    '''chamada_rotina : VARNAME
                      | VARNAME "(" lista_argumentos ")"
                      | READ "(" lista_leitura ")"
                      | READL "(" lista_leitura ")"
                      | WRITE "(" lista_escrita ")"
                      | WRITEL "(" lista_escrita ")"'''
    if p[1].upper() in ['READ', 'READLN', 'READL']:
        p[0] = {'tipo': 'READ', 'args': p[3], 'newline': 'L' in p[1].upper(), 'linha': p.lineno(1)}
    elif p[1].upper() in ['WRITE', 'WRITELN', 'WRITEL']:
        p[0] = {'tipo': 'WRITE', 'args': p[3], 'newline': 'L' in p[1].upper(), 'linha': p.lineno(1)}
    elif len(p) == 2:
        p[0] = {'tipo': 'CALL', 'nome': p[1], 'args': [], 'linha': p.lineno(1)}
    else:
        p[0] = {'tipo': 'CALL', 'nome': p[1], 'args': p[3], 'linha': p.lineno(1)}

def p_bloco_codigo(p):
    'bloco_codigo : BEGIN lista_instrucoes END'
    p[0] = {'tipo': 'BLOCO', 'instrucoes': p[2]}

def p_comando_case(p):
    'comando_case : CASE expressao OF lista_cases END'
    p[0] = {'tipo': 'CASE', 'exp': p[2], 'cases': p[4], 'linha': p.lineno(1)}

def p_lista_cases(p):
    'lista_cases : lista_cases ";" elemento_case'
    if p[3] is not None:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = p[1]

def p_lista_cases_single(p):
    'lista_cases : elemento_case'
    if p[1] is not None:
        p[0] = [p[1]]
    else:
        p[0] = []

def p_elemento_case(p):
    'elemento_case : lista_labels_case ":" instrucao'
    p[0] = {'labels': p[1], 'instrucao': p[3]}

def p_elemento_case_empty(p):
    'elemento_case : empty'
    p[0] = None

def p_lista_labels_case(p):
    'lista_labels_case : lista_labels_case "," label_case'
    p[0] = p[1] + [p[3]]

def p_lista_labels_case_single(p):
    'lista_labels_case : label_case'
    p[0] = [p[1]]

def p_label_case(p):
    'label_case : valor_literal'
    p[0] = p[1]

def p_ciclo_while(p):
    'ciclo_while : WHILE condicao DO instrucao'
    p[0] = {'tipo': 'WHILE', 'cond': p[2], 'do': p[4], 'linha': p.lineno(1)}

# Error production para WHILE
def p_ciclo_while_error_no_do(p):
    'ciclo_while : WHILE condicao error'
    raise Exception(Erros.get('sin', p.lineno(1), 'FALTA_DO', ciclo='WHILE'))

def p_ciclo_repeat(p):
    'ciclo_repeat : REPEAT lista_instrucoes UNTIL condicao'
    p[0] = {'tipo': 'REPEAT', 'instrucoes': p[2], 'until': p[4], 'linha': p.lineno(1)}

def p_ciclo_for(p):
    'ciclo_for : FOR VARNAME ATR expressao passo expressao DO instrucao'
    p[0] = {'tipo': 'FOR', 'var': p[2], 'inicio': p[4], 'passo': p[5], 'fim': p[6], 'do': p[8], 'linha': p.lineno(1)}

# Error production para FOR
def p_ciclo_for_error_no_do(p):
    'ciclo_for : FOR VARNAME ATR expressao passo expressao error'
    raise Exception(Erros.get('sin', p.lineno(1), 'FALTA_DO', ciclo='FOR'))

def p_passo(p):
    '''passo : TO
             | DOWNTO'''
    p[0] = p[1]

def p_comando_goto(p):
    '''comando_goto : GOTO INTVALUE'''
    p[0] = {'tipo': 'GOTO', 'label': p[2], 'linha': p.lineno(1)}

# --- Auxiliares das Instruções ---

def p_lista_argumentos(p):
    'lista_argumentos : lista_argumentos "," expressao'
    p[0] = p[1] + [p[3]]

def p_lista_argumentos_single(p):
    'lista_argumentos : expressao'
    p[0] = [p[1]]

def p_lista_leitura(p):
    'lista_leitura : lista_leitura "," l_value'
    p[0] = p[1] + [p[3]]

def p_lista_leitura_single(p):
    'lista_leitura : l_value'
    p[0] = [p[1]]

def p_lista_escrita(p):
    'lista_escrita : lista_escrita "," item_escrita'
    p[0] = p[1] + [p[3]]

def p_lista_escrita_single(p):
    'lista_escrita : item_escrita'
    p[0] = [p[1]]

def p_item_escrita(p):
    '''item_escrita : expressao
                    | expressao ":" INTVALUE
                    | expressao ":" INTVALUE ":" INTVALUE'''
    if len(p) == 2:
        p[0] = {'exp': p[1]}
    elif len(p) == 4:
        p[0] = {'exp': p[1], 'width': p[3]}
    else:
        p[0] = {'exp': p[1], 'width': p[3], 'prec': p[5]}

# --- Expressões e Condições ---

def p_condicao(p):
    '''condicao : expressao rel_op expressao
                | expressao'''
    if len(p) == 4:
        p[0] = {'op': p[2], 'left': p[1], 'right': p[3],'tipo':parser.cond[p[2]]}
    else:
        p[0] = p[1]

def p_rel_op(p):
    '''rel_op : ">"
              | "<"
              | GE
              | LE
              | NE
              | "="
              | IN'''
    p[0] = p[1]

def p_expressao(p):
    '''expressao : expressao "+" termo
                 | expressao "-" termo
                 | expressao OR termo
                 | termo'''
    if len(p) == 4:
        p[0] = {'op':p[2],'left':p[1],'right':p[3],'tipo':parser.oper[p[2]]}
    else:
        p[0] = p[1]

def p_termo(p):
    '''termo : termo "/" fator
             | termo "*" fator
             | termo DIV fator
             | termo MOD fator
             | termo AND fator
             | fator'''
    if len(p) == 4:
        p[0] = {'op':p[2],'left':p[1],'right':p[3],'tipo':parser.oper[p[2]]}
    else:
        p[0] = p[1]

def p_fator(p):
    '''fator : NOT fator
             | "+" fator
             | "-" fator
             | "(" condicao ")"
             | chamada_rotina
             | valor_literal
             | l_value'''
    if len(p) == 3:
        p[0] = {'op': p[1], 'right': p[2],'tipo':parser.sinal[p[1]]} # Unary operators
    elif p[1] == '(':
        p[0] = p[2]
    else:
        p[0] = p[1]
    
# --- Definição de Tipos ---

def p_definicao_tipo(p):
    '''definicao_tipo : subrange
                      | enum
                      | array
                      | record
                      | tipo_basico
                      | VARNAME'''
    p[0] = p[1]

def p_subrange(p):
    'subrange : valor_constante DOTDOT valor_constante'
    p[0] = {'tipo': 'SUBRANGE', 'min': p[1], 'max': p[3]}

def p_enum(p):
    'enum : "(" lista_enums ")"'
    p[0] = {'tipo': 'ENUM', 'vals': p[2]}

def p_lista_enums(p):
    'lista_enums : lista_enums "," item_enum'
    p[0] = p[1] + [p[3]]

def p_lista_enums_single(p):
    'lista_enums : item_enum'
    p[0] = [p[1]]

def p_item_enum(p):
    'item_enum : VARNAME'
    p[0] = p[1]

def p_array(p):
    '''array : PACKED ARRAY "[" lista_indices "]" OF definicao_tipo
             | ARRAY "[" lista_indices "]" OF definicao_tipo'''
    if p[1].lower() == 'packed':
        p[0] = {'tipo': 'ARRAY', 'packed': True, 'indices': p[4], 'of': p[7]}
    else:
        p[0] = {'tipo': 'ARRAY', 'packed': False, 'indices': p[3], 'of': p[6]}

def p_lista_indices(p):
    'lista_indices : lista_indices "," indice'
    p[0] = p[1] + [p[3]]

def p_lista_indices_single(p):
    'lista_indices : indice'
    p[0] = [p[1]]

def p_indice(p):
    '''indice : INTEGER
              | CHAR
              | BOOL
              | VARNAME
              | subrange
              | enum'''
    p[0] = p[1]

def p_record(p):
    'record : RECORD lista_campos END'
    p[0] = {'tipo': 'RECORD', 'campos': p[2]}

def p_lista_campos(p):
    'lista_campos : lista_campos ";" campo'
    if p[3] is not None:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = p[1]

def p_lista_campos_single(p):
    'lista_campos : campo'
    if p[1] is not None:
        p[0] = [p[1]]
    else:
        p[0] = []

def p_campo(p):
    'campo : lista_identificadores ":" definicao_tipo'
    p[0] = {'vars': p[1], 'tipo': p[3]}

def p_campov(p):
    'campo : empty'
    p[0] = None

def p_tipo_basico(p):
    '''tipo_basico : INTEGER
                   | REAL
                   | BOOL
                   | CHAR'''
    p[0] = p[1].lower()

#acho que aqui temos de separar
def p_valor_literal(p):
    '''valor_literal : INTVALUE
                     | REALVALUE
                     | CHARVALUE
                     | STRINGVALUE
                     | BOOLVALUE'''
    tipo = 'UNKNOWN'
    if p.slice[1].type == 'INTVALUE': tipo = 'integer'
    elif p.slice[1].type == 'REALVALUE': tipo = 'real'
    elif p.slice[1].type == 'CHARVALUE': tipo = 'char'
    elif p.slice[1].type == 'STRINGVALUE': tipo = 'string'
    elif p.slice[1].type == 'BOOLVALUE': tipo = 'boolean'
    
    p[0] = {'tipo': 'LITERAL', 'valor': p[1], 'datatype': tipo}
    
def p_valor_constante(p):
    '''valor_constante : INTVALUE
                       | CHARVALUE
                       | BOOLVALUE
                       | VARNAME
                       | "+" INTVALUE
                       | "-" INTVALUE'''
    if len(p) == 2:
        tipo = 'UNKNOWN'
        if p.slice[1].type == 'INTVALUE': tipo = 'integer'
        elif p.slice[1].type == 'CHARVALUE': tipo = 'char'
        elif p.slice[1].type == 'BOOLVALUE': tipo = 'boolean'
        elif p.slice[1].type == 'VARNAME': tipo = 'id'
        
        p[0] = {'tipo': 'LITERAL', 'valor': p[1], 'datatype': tipo}
    else:
        # Handle unary + or - for constants
        val = p[2]
        if p[1] == '-':
            val = -val
        p[0] = {'tipo': 'LITERAL', 'valor': val, 'datatype': 'integer'}

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    if p:
        # Tentar inferir um contexto mais útil baseado no token e estado
        contexto = getattr(parser, 'contexto', None)
        
        # Heurísticas para mensagens mais úteis
        sugestao = None
        if p.type == 'VARNAME':
            # Um identificador onde não era esperado pode indicar falta de keyword
            sugestao = "Verifique se falta uma palavra-chave como 'THEN', 'DO', 'BEGIN', ou ';'."
        elif p.type == 'BEGIN':
            sugestao = "Verifique se falta ';' antes do 'BEGIN'."
        elif p.type == 'END':
            sugestao = "Verifique se falta ';' entre instruções."
        elif p.type == 'ATR':
            sugestao = "Verifique a expressão antes do ':='."
        
        if contexto and sugestao:
            msg = Erros.get('sin', p.lineno, 'TOKEN_INESPERADO_CONTEXTO', 
                           token=p.value, tipo_token=p.type, contexto=f"{contexto} {sugestao}")
        elif sugestao:
            msg = Erros.get('sin', p.lineno, 'TOKEN_INESPERADO_CONTEXTO', 
                           token=p.value, tipo_token=p.type, contexto=sugestao)
        elif contexto:
            msg = Erros.get('sin', p.lineno, 'TOKEN_INESPERADO_CONTEXTO', 
                           token=p.value, tipo_token=p.type, contexto=contexto)
        else:
            msg = Erros.get('sin', p.lineno, 'TOKEN_INESPERADO', 
                           token=p.value, tipo_token=p.type)
    else:
        contexto = getattr(parser, 'contexto', None)
        if contexto:
            msg = Erros.get('sin', None, 'EOF_INESPERADO_CONTEXTO', contexto=contexto)
        else:
            msg = Erros.get('sin', None, 'EOF_INESPERADO_CONTEXTO', 
                           contexto="Verifique se falta 'END.' no final do programa.")
    
    # Limpar o contexto após usar
    parser.contexto = None
    
    # Imprimir a mensagem de erro formatada
    print(msg, file=sys.stderr)
    
    # Lançar excepção para parar o parsing (mas sem traceback feio)
    raise ErroSintaxe(msg)

parser = yacc.yacc(debug=True)

# Inicialização das variáveis de contexto para erros
parser.contexto = None

def set_contexto(msg):
    """Define o contexto atual para mensagens de erro mais informativas."""
    parser.contexto = msg

def clear_contexto():
    """Limpa o contexto após sucesso."""
    parser.contexto = None

def parse_with_context(code, context_msg=None):
    """
    Faz parse do código com um contexto opcional para mensagens de erro.
    Uso: parse_with_context(code, "A processar o ficheiro exemplo.pp")
    """
    if context_msg:
        parser.contexto = context_msg
    try:
        result = parser.parse(code, lexer=lexer)
        parser.contexto = None
        return result
    except Exception as e:
        parser.contexto = None
        raise e

parser.cond={
    '<': 'LESS',
    '>': 'GREAT',
    '<=': 'LEQ',
    '>=': 'GEQ',
    '=': 'EQUAL',
    '<>': 'NEQ',
    'in': 'IN'
}
parser.oper={
    '+': 'SOMA',
    '-': 'SUB',
    '*': 'MUL',
    '/': 'DIVR',
    'div': 'DIV',
    'mod': 'MOD',
    'and': 'AND',
    'or': 'OR'
}
parser.sinal ={
    '+': 'POS',
    '-': 'NEG',
    'not': 'NOT'
}