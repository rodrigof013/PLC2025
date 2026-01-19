# TODO List - Compilador Pascal

## Já feito

- [x] **Testar:**

  - [x] Testar os tokens gerados pelo analex e analisar se gera o que deve gerar!(colocar testes ou criar um script de testes, na pasta [pascal](/pascal/))
    - [x] Teste 1
    - [x] Teste 2
    - [x] Teste 3
    - [x] Teste 4
    - [x] Teste 5
    - [x] Teste 6
    - [x] Teste 7
    - [x] Teste 8
    - [x] Teste 9
    - [x] Teste 10
    - [x] Teste 11
    - [x] Teste 12
  - [x] Implementar a gramática no anasin (Passar do texto para o código)
  - [x] Depois de implementar o anasin testar a gramática
    - [x] Teste 1
    - [x] Teste 2
    - [x] Teste 3
    - [x] Teste 4
    - [x] Teste 5
    - [x] Teste 6
    - [x] Teste 7
    - [x] Teste 8
    - [x] Teste 9
    - [x] Teste 10
    - [x] Teste 11
    - [x] Teste 12

- [x] **Pensar na AST** Reunir e ver melhor forma para representar a nossa árvore
- [x] **Implementar a AST** Colocar as funções da parte sintática a criar a árvore
- [x] **Pensar e implementar na tabela de símbolos** Pensar como iremos armazenar símbolos (nome,tipo,posição_na_VM)
- [x] **Análise Semântica** Pensar como iremos fazer a análise semântica (analisar a AST)
- [x] Testar a análise sintática, falta teste 9
- [x] Dividir testes em testes que é suposto dar, e testes que é suposto dar erro (mas erros inteligentes) (os testes 8, 11 e)

## Prioridade Alta (Anasem, Programa)

- [ ] **Fazer o programa** Lê a AST e gera o código para a VM
  - [ ] Corre para os programas do enunciado?
    - [x] 1
    - [x] 2
    - [x] 3
    - [ ] 4
    - [ ] 5

## Prioridade Baixa / Futuro (Funcionalidades)

- [ ] Ver o que se passa com os records ainda não processa bem
- [ ] **Erros Inteligentes** Pensar em como fazer gerar estes erros inteligentes
  - [ ] **Extras Interessantes**
    - [ ] **Abrir direto no site** Ao correr o código abrir logo o site com o código da VM pronto a colar
    - [ ] **Chamar o programa** Criar um executável, tentar fazer no terminal por exemplo: gcc ficheiro (possiveis flags)
