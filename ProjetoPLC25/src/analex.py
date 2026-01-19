import ply.lex as lex
import re

literals = ['=','(',')',',',':','+','-','*','/','<','>','[',']', '{', '}','.',';']
tokens = (
    'COMNT', 'COMNTSTD','COMTSTDS','PROGRAM', 'BEGIN', 'FUNCTION', 'END', 'ENDPROGRAM',
    'VAR', 'AND', 'ARRAY', 'DOTDOT', 'CASE', 'CONST', 'DIV', 'ELSE',
    'GE', 'LE', 'NE', 'ATR', 'DO', 'DOWNTO', 'FILE', 'FOR',
    'GOTO', 'IF', 'IN', 'LABEL', 'MOD', 'NIL', 'NOT', 'OF',
    'OR', 'PACKED', 'PROCEDURE', 'RECORD', 'REPEAT', 'SET',
    'THEN', 'TO', 'TYPE', 'UNTIL', 'WHILE', 'WITH',
    'ABS', 'SQR', 'SQRT', 'ROUND', 'ODD', 'INTEGER', 'SMALLINT',
    'LONGINT', 'REAL', 'BOOL', 'CHAR', 'BYTE',
    'READ', 'READL', 'WRITE', 'WRITEL', 'VARNAME',
    'INTVALUE', 'REALVALUE', 'BOOLVALUE', 'STRINGVALUE', 'CHARVALUE'
)

states = [
    ('ended','inclusive')
]

t_ignore = '\t '

##------Depois de acabar o programa

def t_ended_ANY(t):
    r'[^ \t\n]+'
    print(f"AVISO: Conteúdo ignorado após 'end.': {t.value}")
    pass

t_ended_ignore = ' \t\n'

##-----KEY WORDS

def t_COMNTSTD(t):
    r'\{[^}]*\}'
    pass

def t_COMTSTDS(t):
    r'\(\*[^\(\*\)]*\*\)'
    pass

def t_COMNT(t):
    r'//[^\n]*'
    pass

def t_PROGRAM(t):
    r'\bprogram\b'
    return t

def t_ENDPROGRAM(t):
    r'\bend\b[ \t\n]*\.'
    t.lexer.begin('ended')
    return t

def t_INTEGER(t):
    r'\b(?:integer|smallint|longint|int64|byte)\b'
    return t

def t_DOTDOT(t):
    r'\.\.'
    return t

def t_GE(t):
    r'>='
    return t

def t_LE(t):
    r'<='
    return t

def t_NE(t):
    r'<>'
    return t

def t_END(t):
    r'\bend\b'
    return t

def t_ATR(t):
    r':='
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


#-----VALORES---------

def t_CHARVALUE(t):
    r"'[^']'"
    t.value = t.value[1:-1]
    return t

def t_STRINGVALUE(t):
    r"'[^']*'"
    t.value = t.value[1:-1]  # Remove as aspas simples
    return t

def t_REALVALUE(t):
    r'\d+\.\d{1,}'
    t.value = float(t.value)
    return t

def t_INTVALUE(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_BOOLVALUE(t):
    r'\b(?:true|false)\b'
    if t.value.lower() == 'true':
        t.value = True
    else:
        t.value = False
    return t

#-----------------------
def t_KEYWORDS(t):
    r'[A-Za-z_][A-Za-z0-9_]*'
    val = t.value.lower()
    reserved = {
        'begin': 'BEGIN', 'function': 'FUNCTION', 'do' : 'DO', 'const' : 'CONST',
        'end': 'END', 'var': 'VAR', 'if': 'IF', 'then': 'THEN', 'else': 'ELSE',
        'for': 'FOR', 'while': 'WHILE', 'repeat': 'REPEAT', 'until': 'UNTIL',
        'read': 'READ', 'write': 'WRITE', 'div' : 'DIV', 'downto' : 'DOWNTO',
        'and' : 'AND', 'case' : 'CASE', 'file':'FILE', 'in' : 'IN', 'goto':'GOTO',
        'mod' : 'MOD', 'nil':'NIL', 'not' : 'NOT', 'of' : 'OF', 'or' : 'OR',
        'packed' : 'PACKED', 'procedure' : 'PROCEDURE', 'record' : 'RECORD', 'array':'ARRAY',
        'set' : 'SET', 'to' : 'TO', 'type' : 'TYPE', 'with':'WITH', 'abs' : 'ABS',
        'sqr' : 'SQR', 'sqrt' : 'SQRT', 'round':'ROUND','odd':'ODD', 'round' : 'ROUND',
        'odd' : 'ODD', 'real': 'REAL', 'boolean' : 'BOOL','char':'CHAR',
        'read':'READ', 'readln':'READL', 'write':'WRITE', 'writeln':'WRITEL', 'label' : 'LABEL'
    }
    if val in reserved:
        t.type = reserved[val]
    else:
        t.type = 'VARNAME'
    return t

def t_error(t):
    caracter = t.value[0]
    
    justificacao = f"Carácter ilegal '{caracter}' não reconhecido."
    
    inicio_linha = t.lexer.lexdata.rfind('\n', 0, t.lexpos) + 1
    coluna = (t.lexpos - inicio_linha) + 1
    
    raise Exception(f"ERRO LÉXICO: {justificacao} [Linha {t.lexer.lineno}, Coluna {coluna}]")

lexer = lex.lex(reflags=re.IGNORECASE)