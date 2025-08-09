import json
import os

# Lista com os nomes dos seus arquivos JSON
arquivos = [
    "api-response (1).json",
    "api-response (2).json",
    "api-response (3).json",
    "api-response (4).json"
]

todas_questoes = []

for arquivo in arquivos:
    with open(arquivo, "r", encoding="utf-8") as f:
        dados = json.load(f)
        todas_questoes.extend(dados.get("questions", []))

# Criar JSON final
resultado = {
    "metadata": {
        "total": len(todas_questoes)
    },
    "questions": todas_questoes
}

# Salvar em um novo arquivo
with open("enem_completo.json", "w", encoding="utf-8") as f:
    json.dump(resultado, f, ensure_ascii=False, indent=4)



print("✅ Arquivo final salvo como 'enem_completo.json'")
