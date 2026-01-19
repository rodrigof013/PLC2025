from Cores import Cores
from rich import print

d={
    'Length': {
        'categoria': 'func',
        'args': [{'nome': 's', 'tipo': {'tipo': 'array', 'dimensoes': [{'tipo': 'subrange', 'min': 1, 'max': 50, 'datatype': 'integer', 'size': 1}], 'of': {'tipo': 'atomico', 'nome': 'char', 'size': 1}, 'size': 50, 'packed': True, 'categoria': 'type'}, 'categoria': 'param', 'sp': -50}, {'nome': 'j', 'tipo': {'tipo': 'atomico', 'nome': 'integer', 'size': 1}, 'categoria': 'param', 'sp': -51}],
        'vars': {
            's': {'nome': 's', 'tipo': {'tipo': 'array', 'dimensoes': [{'tipo': 'subrange', 'min': 1, 'max': 50, 'datatype': 'integer', 'size': 1}], 'of': {'tipo': 'atomico', 'nome': 'char', 'size': 1}, 'size': 50, 'packed': True, 'categoria': 'type'}, 'categoria': 'param', 'sp': -50},
            'j': {'nome': 'j', 'tipo': {'tipo': 'atomico', 'nome': 'integer', 'size': 1}, 'categoria': 'param', 'sp': -51},
            'i': {'categoria': 'var_local', 'tipo': {'tipo': 'atomico', 'nome': 'integer', 'size': 1}, 'sp': 0}
        },
        'return': {'tipo': 'atomico', 'nome': 'integer', 'size': 1}
    }
}

cor = Cores.AMARELO if 1+1==2 else Cores.AZUL


h={k: v for k, v in d['Length']['vars'].items() if v['categoria'] == 'param'}
print(h)