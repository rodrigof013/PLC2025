import sys
import json
import alex_tp5 as analex
import datetime
# abrir e carregar o ficheiro json
ficheiro = "stock.json"

with open(ficheiro, "r", encoding="utf-8") as f:
    stock = json.load(f)

def calcular_troco(valor):
    moedas = [2, 1, 0.5, 0.2, 0.1, 0.05, 0.02, 0.01]
    troco = {}
    for m in moedas:
        while valor >= m - 0.001:  # tolerância por arredondamentos
            troco[m] = troco.get(m, 0) + 1
            valor = round(valor - m, 2)
    return troco

def formatar_troco(troco):
    return ", ".join([f"{v}x {int(m*100)}c" if m < 1 else f"{v}x {int(m)}e" for m,v in troco.items()])

saldo = 0

print(f"maq: {datetime.datetime.now()}, Stock carregado, Estado atualizado.")
print(f"maq: Bom dia. Estou disponível para atender o seu pedido.")

while True:
    comando = input(">> ").strip()
    analex.lexer.input(comando)
    tokens = [tok for tok in analex.lexer]

    if not tokens:
        continue

    tok0 = tokens[0]
    if tok0.type == "LISTAR":
        print("maq:")
        print("cod  |   nome            | quantidade    | preço")
        print("--------------------------------------------")
        for produto in stock:
            print(f"{produto['cod']:<6} {produto['nome']:<15} {produto['quant']:<6} {produto['preco']:.2f}")        
    elif tok0.type == "MOEDA":
        valor_total = 0
        for t in tokens[1:]:
            if t.type == "EURO":
                valor_total += t.value
            elif t.type == "CENTIMO":
                valor_total += t.value / 100
        saldo += valor_total
        euros = int(saldo)
        centimos = int(round((saldo -euros) * 100))
        print(f"maq: Saldo = {euros}e{centimos}c")
    elif tok0.type == "SELECIONAR":
        codigo = tokens[1].value
        produto = next((produto for produto in stock if produto["cod"] == codigo), None)

        if not produto:
            print("maq: Produto inexistente.")
            continue
        if produto["quant"] <= 0:
            print("maq: Produto esgotado.")
            continue
        if saldo < produto["preco"]:
            print("maq: Saldo insuficiente para satisfazer o seu pedido")
            print(f"maq: Saldo = {saldo:.2f}€; Pedido = {produto['preco']:.2f}€")
            continue

        produto["quant"] -= 1
        saldo = round(saldo - produto["preco"], 2)
        print(f'maq: Pode retirar o produto dispensado "{produto["nome"]}"')
        euros = int(saldo)
        cents = int(round((saldo - euros) * 100))
        print(f"maq: Saldo = {euros}e{cents:02d}c")

    elif tok0.type == "SAIR":
        troco = calcular_troco(saldo)
        if troco:
            print(f"maq: Pode retirar o troco: {formatar_troco(troco)}.")
        print("maq: Até à próxima.")

        with open("stock.json", "w", encoding="utf-8") as f:
            json.dump(stock, f, indent=4, ensure_ascii=False)







