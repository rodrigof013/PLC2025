# Trabalho Prático 3

## Resumo
O objetivo deste trabalho prático foi construir um analisador léxico para uma linguagem de query com a qual se podem escrever frases do género:

" # DBPedia: obras de Chuck Berry
        select ?nome ?desc where {
        ?s a dbo:MusicalArtist.
        ?s foaf:name "Chuck Berry"@en .
        ?w dbo:artist ?s.
        ?w foaf:name ?nome.
        ?w dbo:abstract ?desc
    } LIMIT 1000 "


O meu raciocínio passou por olhar para a frase e identificar os tokens presentes nela. Depois de colocar cada token associado à expressão regular que o representa, o objetivo foi percorrer a frase e ir acrescentando o token encontrado, o seu valor (string), a linha onde está e o span, a uma lista reconhecidos.

## Lista de Resultados
- [Notebook com a solução do TP3](tp3.ipynb)
