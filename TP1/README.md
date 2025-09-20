# Trabalho Prático 1

## Autor
- **Nome:** Rodrigo Lavandeira Fernandes
- **ID:** A108401
- **Foto:** 
<img src="foto.jpeg" alt="Foto do autor" width="200">


## Resumo
- Neste trabalho prático, foi-nos proposto determinar uma expressão regular de strings binárias que não incluíssem a subsequência "011". 
- Para apoiar os resultados e validar a expressão regular, utilizei a aplicação regex101, bem como o desenho de um autómato que reconhece a expressão pretendida.
- Quanto ao raciocínio, a fim de conseguir incluir todas as palavras possíveis na expressão, começo por permitir que hajam palavras formadas por um número arbitrário de - 1's. De seguida, caso ocorra um 0 na expressão, depois disso apenas posso permitir que hajam ou mais 0's ou então a subsequência "10", o número de vezes que a 
- pretender. No fim da expressão, há ainda a opção de terminar com 1. Desta forma, o padrão "011" é evitado. 

## Lista de Resultados
- [Expressão regular proposta pelo trabalho prático](tpc1.txt)
- [Autómato que descreve a expressão regular](automato.jpeg)
- [Lista de testes efetuados no regex101](https://regex101.com/r/CwqLaB/1)