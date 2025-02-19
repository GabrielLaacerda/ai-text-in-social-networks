import os
import json
import matplotlib.pyplot as plt

# Diretórios dos arquivos JSON
dir_huggingface = "/home/gabriel/TCC_GabrielVncs/Comentarios_Originais_Twitter/Resultados_HuggingFace"
dir_roberta = "/home/gabriel/TCC_GabrielVncs/Comentarios_Originais_Twitter/Resultados_Roberta"

def extrair_dados(diretorio):
    """Conta acertos binários (prob_IA >= 50) para cada tema nos arquivos JSON."""
    dados = {}
    for arquivo in os.listdir(diretorio):
        if arquivo.endswith(".json"):
            caminho = os.path.join(diretorio, arquivo)
            with open(caminho, "r", encoding="utf-8") as f:
                conteudo = json.load(f)
                acertos = sum(1 for item in conteudo if item["prob_IA"] >= 50.0)  # Conta acertos
                tema = arquivo.replace("resultados_", "").replace(".json", "")
                dados[tema] = acertos  # Salva acertos absolutos
    return dados

# Extrair os dados dos dois detectores
acertos_por_detector = {
    "HuggingFace": extrair_dados(dir_huggingface),
    "Roberta": extrair_dados(dir_roberta)
}

# Criar gráfico de barras comparativo
def plot_bar_chart(acertos_por_detector):
    temas = list(acertos_por_detector["HuggingFace"].keys())
    valores_huggingface = list(acertos_por_detector["HuggingFace"].values())
    valores_roberta = list(acertos_por_detector["Roberta"].values())

    x = range(len(temas))  # Posições no eixo X

    plt.figure(figsize=(12, 6))
    plt.bar(x, valores_huggingface, width=0.4, label="HuggingFace", color="blue", alpha=0.7)
    plt.bar([p + 0.4 for p in x], valores_roberta, width=0.4, label="Roberta", color="red", alpha=0.7)

    # Adiciona números exatos nos topos das barras
    for i, v in enumerate(valores_huggingface):
        plt.text(i, v + 0.2, str(v), ha='center', va='bottom', fontsize=10, color="blue")
    for i, v in enumerate(valores_roberta):
        plt.text(i + 0.4, v + 0.2, str(v), ha='center', va='bottom', fontsize=10, color="red")

    plt.xlabel("Temas")
    plt.ylabel("Número de Acertos")
    plt.title("Comparação de Acertos por Tema")
    plt.xticks([p + 0.2 for p in x], temas, rotation=45)
    plt.legend()
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    plt.tight_layout()
    plt.show()

# Gerar o gráfico de barras
plot_bar_chart(acertos_por_detector)
