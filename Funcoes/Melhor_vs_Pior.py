import os
import json
import matplotlib.pyplot as plt

# Diretórios dos arquivos JSON
dir_huggingface = "/home/gabriel/TCC_GabrielVncs/Comentarios_Originais_Twitter/Resultados_HuggingFace"
dir_roberta = "/home/gabriel/TCC_GabrielVncs/Comentarios_Originais_Twitter/Resultados_Roberta"

def extrair_dados(diretorio):
    """Extrai a média de probabilidade de IA de cada tema nos arquivos JSON do diretório."""
    dados = {}
    for arquivo in os.listdir(diretorio):
        if arquivo.endswith(".json"):
            caminho = os.path.join(diretorio, arquivo)
            with open(caminho, "r", encoding="utf-8") as f:
                conteudo = json.load(f)
                probabilidades = [item["prob_IA"] for item in conteudo]
                media = sum(probabilidades) / len(probabilidades) if probabilidades else 0
                tema = arquivo.replace("resultados_", "").replace(".json", "")
                dados[tema] = media * 100  # Converter para porcentagem
    return dados

# Extrair os dados dos dois detectores
medias_por_detector = {
    "HuggingFace": extrair_dados(dir_huggingface),
    "Roberta": extrair_dados(dir_roberta)
}

# Criar gráfico de barras comparativo
def plot_bar_chart(medias_por_detector):
    temas = list(medias_por_detector["HuggingFace"].keys())
    valores_huggingface = list(medias_por_detector["HuggingFace"].values())
    valores_roberta = list(medias_por_detector["Roberta"].values())

    x = range(len(temas))  # Posições no eixo X

    plt.figure(figsize=(12, 6))
    plt.bar(x, valores_huggingface, width=0.4, label="HuggingFace", color="blue", alpha=0.7)
    plt.bar([p + 0.4 for p in x], valores_roberta, width=0.4, label="Roberta", color="red", alpha=0.7)

    plt.xlabel("Temas")
    plt.ylabel("Média prob_IA (%)")
    plt.title("Comparação da probabilidade de IA por tema")
    plt.xticks([p + 0.2 for p in x], temas, rotation=45)
    plt.legend()
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    plt.tight_layout()
    plt.show()

# Gerar o gráfico de barras
plot_bar_chart(medias_por_detector)
