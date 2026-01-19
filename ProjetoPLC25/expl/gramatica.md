# Gramática Pascal Standard (ISO 7185)

## Estrutura Geral

# O ponto de entrada da gramática. Um programa tem cabeçalho, declarações e o bloco da main.

programa : PROGRAM VARNAME ";" bloco_declaracoes bloco_main

# Bloco que agrupa todas as declarações possíveis antes da main (Labels, Constantes, Tipos, Variáveis, Rotinas).

bloco_declaracoes : bloco_declaracoes decl_labels
| bloco_declaracoes decl_consts
| bloco_declaracoes decl_types
| bloco_declaracoes decl_vars
| bloco_declaracoes decl_rotinas
| empty

---

## Declaração de Labels (Rótulos para GOTO)

# Secção iniciada por LABEL, seguida de uma lista de identificadores.

decl_labels : LABEL lista_labels ";"
| empty

lista_labels : lista_labels "," INTVALUE
| INTVALUE

---

## Declaração de Constantes

# Secção iniciada por CONST, onde se definem valores fixos.

decl_consts : CONST lista_consts
| empty

lista_consts : lista_consts def_const
| def_const

def_const : VARNAME "=" valor_literal ";"

---

## Declaração de Tipos

# Secção TYPE para criar novos tipos de dados (arrays, records, alias).

decl_types : TYPE lista_types
| empty

lista_types : lista_types def_type
| def_type

def_type : VARNAME "=" definicao_tipo ";"

---

## Declaração de Variáveis

# Secção VAR para declarar variáveis globais.

decl_vars : VAR lista_decl_vars
| empty

lista_decl_vars : lista_decl_vars declaracao_var
| declaracao_var

# Ex: x, y, z : integer;

declaracao_var : lista_identificadores ":" definicao_tipo ";"

lista_identificadores : lista_identificadores "," VARNAME
| VARNAME

---

## Declaração de Rotinas (Funções e Procedimentos)

# Funções e Procedimentos podem ser declarados recursivamente.

decl_rotinas : lista_rotinas
| empty

# Definição de Funções e Procedimentos.

# Nota: Funções retornam valor (": tipo"), Procedimentos não.

lista_rotinas : lista_rotinas FUNCTION VARNAME "(" lista_params ")" ":" definicao_tipo ";" bloco_declaracoes bloco_main ";"
| lista_rotinas PROCEDURE VARNAME "(" lista_params ")" ";" bloco_declaracoes bloco_main ";"
| FUNCTION VARNAME "(" lista_params ")" ":" definicao_tipo ";" bloco_declaracoes bloco_main ";"
| PROCEDURE VARNAME "(" lista_params ")" ";" bloco_declaracoes bloco_main ";"

# Lista de parâmetros formais (argumentos da função).

lista_params : lista_params ";" param_group
| param_group
| empty

# Grupo de parâmetros do mesmo tipo (ex: x, y : integer).

# TODO: Adicionar suporte a VAR (passagem por referência).

param_group : lista_identificadores ":" definicao_tipo

---

## Bloco Principal e Instruções

# O corpo principal do programa ou de uma rotina.

# Nota: Programas acabam em ".", Rotinas acabam em ";" (tratado na regra acima).

bloco_main : BEGIN lista_instrucoes ENDPROGRAM
| BEGIN lista_instrucoes END

# Lista de instruções separadas por ponto e vírgula.

lista_instrucoes : lista_instrucoes ";" instrucao
| instrucao
| empty

# Instrução genérica (pode ser completa ou incompleta por causa do IF).

instrucao : instrucao_composta
| instrucao_incompleta

# Instruções que têm um fim bem definido (fechadas).

instrucao_composta : atribuicao
| chamada_rotina
| bloco_codigo
| IF condicao THEN instrucao_composta ELSE instrucao_composta
| comando_case
| ciclo_while
| ciclo_repeat
| ciclo_for
| comando_goto
| empty

# Instruções "abertas" (IF sem ELSE ou com ELSE aninhado aberto).

instrucao_incompleta : IF condicao THEN instrucao
| IF condicao THEN instrucao_composta ELSE instrucao_incompleta

---

## Tipos de Instruções

### Atribuição

# Atribuir o resultado de uma expressão a uma variável.

atribuicao : l_value ATR expressao

l_value : VARNAME
| VARNAME "[" indice "]"
| VARNAME "." VARNAME

### Chamada de Rotinas e IO

# Chamadas de funções ou procedimentos, incluindo read/write.

chamada_rotina : VARNAME
| VARNAME "(" lista_argumentos ")"
| READ "(" lista_leitura ")"
| READL "(" lista_leitura ")"
| WRITE "(" lista_escrita ")"
| WRITEL "(" lista_escrita ")"

### Bloco Composto

# Um bloco begin..end dentro do código (para agrupar instruções).

bloco_codigo : BEGIN lista_instrucoes END

### Switch Case

# Estrutura de seleção múltipla.

comando_case : CASE expressao OF lista_cases END

lista_cases : lista_cases ";" elemento_case
| elemento_case

elemento_case : lista_labels_case ":" instrucao
| empty

lista_labels_case : lista_labels_case "," label_case
| label_case

label_case : valor_literal

### Ciclos

# Ciclo While (Enquanto).

ciclo_while : WHILE condicao DO instrucao

# Ciclo Repeat (Repetir até).

ciclo_repeat : REPEAT lista_instrucoes UNTIL condicao

# Ciclo For (Para).

ciclo_for : FOR VARNAME ATR expressao passo expressao DO instrucao

passo : TO | DOWNTO

### Goto

# Salto incondicional para uma label.

comando_goto : GOTO VARNAME
| GOTO INTVALUE

---

## Auxiliares das Instruções

# Lista de argumentos passados numa chamada (R-Values).

lista_argumentos : lista_argumentos "," expressao
| expressao

# Lista de variáveis para leitura.

lista_leitura : lista_leitura "," l_value
| l_value

# Lista de expressões para escrita (pode ter formatação).

lista_escrita : lista_escrita "," item_escrita
| item_escrita

item_escrita : expressao
| expressao ":" INTVALUE
| expressao ":" INTVALUE ":" INTVALUE

---

## Expressões e Condições

# Condição Booleana (Comparação).

condicao : expressao rel_op expressao
| expressao

rel_op : ">" | "<" | GE | LE | NE | "=" | IN

# Expressão (Soma, Subtração, OR).

expressao : expressao "+" termo
| expressao "-" termo
| expressao OR termo
| termo

# Termo (Multiplicação, Divisão, AND).

termo : termo "/" fator
| termo "\*" fator
| termo DIV fator
| termo MOD fator
| termo AND fator
| fator

# Fator (Prioridade máxima, Negação, Parênteses).

fator : NOT fator
| "+" fator
| "-" fator
| "(" condicao ")"
| chamada_rotina
| valor_literal
| l_value

---

## Definição de Tipos

# Tipos que podem ser usados na declaração de variáveis.

definicao_tipo : subrange
| enum
| array
| record
| tipo_basico
| VARNAME # para um tipo já definido

# Intervalos (ex: 1..10).

subrange : valor_constante DOTDOT valor_constante

# Enumerados (ex: (azul, verde)).

enum : "(" lista_enums ")"

lista_enums : lista_enums "," item_enum
| item_enum

item_enum : VARNAME

# Arrays (ex: array[1..10] of integer).

array : PACKED ARRAY "[" lista_indices "]" OF definicao_tipo
| ARRAY "[" lista_indices "]" OF definicao_tipo

lista_indices : lista_indices "," indice
| indice

indice : INTEGER
| CHAR
| BOOL
| VARNAME
| subrange
| enum

# Records (Estruturas).

record : RECORD lista_campos END

lista_campos : lista_campos ";" campo
| campo

campo : lista_identificadores ":" definicao_tipo

# Tipos Primitivos.

tipo_basico : INTEGER
| REAL
| BOOL
| CHAR

# Valores Literais (Números, Strings, etc).

valor_literal : INTVALUE
| REALVALUE
| CHARVALUE
| STRINGVALUE
| BOOLVALUE

# Valores constantes para definições (sem variáveis).

valor_constante : INTVALUE
| CHARVALUE
| BOOLVALUE
| VARNAME # Se for uma const definida
| "+" INTVALUE
| "-" INTVALUE

empty :
