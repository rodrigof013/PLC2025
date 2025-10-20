import ply.lex as lex

states = (
    ('moedas', 'exclusive') ,
    ('selecionar', 'exclusive')
)

tokens = (
    'LISTAR',
    'MOEDA',
    'MOEDA_FIM',
    'EURO',
    'CENTIMO',
    'SELECIONAR',
    'CODIGO',
    'SAIR'
)

t_ANY_ignore = ' \t\n'

def t_LISTAR(t):
    r'LISTAR'
    return t

def t_MOEDA(t):
    r'MOEDA'
    t.lexer.begin('moedas')
    return t

def t_moedas_EURO(t):
    r'\d+e'
    t.value = int(t.value[:-1])
    return t

def t_moedas_CENTIMO(t):
    r'\d+c'
    t.value = int(t.value[:-1])
    return t

def t_moedas_MOEDA_FIM(t):
    r'\.'
    t.lexer.begin('INITIAL')
    return t

t_moedas_ignore = ' \t\n,'

def t_SELECIONAR(t):
    r'SELECIONAR'
    t.lexer.begin('selecionar')
    return t

def t_selecionar_CODIGO(t):
    r'[A-Z]\d+'
    t.lexer.begin('INITIAL')
    return t

t_selecionar_ignore = ' \t\n'

def t_SAIR(t):
    r'SAIR'
    return t

def t_ANY_error(t):
    print(f"Caracter ilegal: {t.value[0]}")
    t.lexer.skip(1)

lexer = lex.lex()
