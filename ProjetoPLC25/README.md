# Compilador de Pascal Standard (ISO 7185)

## **Apresentação**: https://www.canva.com/design/DAG-2o45VKU/uMsRJ8UnLK7A6zX6W3rKpQ/edit?utm_content=DAG-2o45VKU&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton

<p align="center">
  <img src="logotipoPCP.png" alt="Logo PCP" width="200"/>
</p>

Compilador para a linguagem **Pascal Standard** (ISO 7185), implementado em **Python** com **PLY** (Python Lex-Yacc). Gera código para a máquina virtual **EWVM**.

## Funcionalidades

- **Análise Léxica** - Reconhecimento de tokens, palavras reservadas, literais e comentários
- **Análise Sintática** - Parser completo com mensagens de erro contextuais
- **Análise Semântica** - Verificação de tipos, declarações e compatibilidade
- **Geração de Código** - Código para a VM EWVM (arrays, records, funções, etc.)

### Suporte a:

- Tipos: `integer`, `real`, `char`, `string`, `boolean`
- Estruturas: `array`, `record`, `subrange`, `enum`
- Controlo: `if-then-else`, `while`, `repeat-until`, `for`, `case`
- Subprogramas: `procedure` e `function` com parâmetros
- I/O: `read`, `readln`, `write`, `writeln`

## Utilização

```bash
cd src

# Compilar ficheiro e mostrar código gerado
python pcprogram.py programa.pp

# Compilar e guardar em ficheiro .vm
python pcprogram.py programa.pp -o programa.vm

# Quick mode: compila, copia para clipboard e abre a VM (recomendado)
python pcprogram.py programa.pp -q

# Modo interativo (escrever código diretamente, Ctrl+Z para terminar)
python pcprogram.py
```

### Opções

| Opção     | Descrição                                                  |
| --------- | ---------------------------------------------------------- |
| `-o FILE` | Guarda o código gerado no ficheiro especificado            |
| `-v`      | Modo verbose (mostra progresso da compilação)              |
| `-c`      | Copia código para clipboard e abre a VM no browser         |
| `-q`      | Como `-c` mas também guarda ficheiro `.vm` automaticamente |

## 📂 Estrutura do Projeto

```
ProjetoPLC25/
├── src/
│   ├── pcprogram.py    # Programa principal do compilador
│   ├── analex.py       # Analisador léxico
│   ├── anasin.py       # Analisador sintático (parser)
│   ├── anasem.py       # Analisador semântico
│   ├── geraCod.py      # Gerador de código EWVM
│   ├── Erros.py        # Sistema de mensagens de erro
│   └── Cores.py        # Cores para output no terminal
├── pascal/             # Programas de teste (.pp)
├── expl/               # Documentação da gramática
│   ├── gramatica.md
│   └── tokens.md
└── README.md
```

## Exemplo

```pascal
program Exemplo;
var
  n, fat: integer;
begin
  write('Numero: ');
  readln(n);
  fat := 1;
  while n > 1 do
  begin
    fat := fat * n;
    n := n - 1
  end;
  writeln('Fatorial: ', fat)
end.
```

```bash
python pcprogram.py exemplo.pp -q
```

## Dependências

```bash
pip install ply pyperclip
```

## 📚 Referências

- [Pascal Standard (ISO 7185)](https://wiki.freepascal.org/Standard_Pascal)
- [PLY Documentation](https://www.dabeaz.com/ply/)
- [EWVM - Máquina Virtual](https://ewvm.epl.di.uminho.pt)
