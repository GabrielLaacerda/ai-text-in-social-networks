import os
import json
import matplotlib.pyplot as plt

# Diretórios dos arquivos JSON
dir_huggingface = "/home/gabriel/TCC_GabrielVncs/Comentarios_Originais_Twitter/Resultados_HuggingFace"
dir_roberta = "/home/gabriel/TCC_GabrielVncs/Comentarios_Originais_Twitter/Resultados_Roberta"

def extrair_dados(diretorio, detector):
    dados = {}
    for arquivo in os.listdir(diretorio):
        if arquivo.endswith(".json"):
            caminho = os.path.join(diretorio, arquivo)
            with open(caminho, "r", encoding="utf-8") as f:
                conteudo = json.load(f)
                total_itens = len(conteudo)
                print(f"\n[{detector}] Arquivo: {arquivo} - Total de comentários: {total_itens}")

                acertos = 0
                for item in conteudo:
                    comentario = item.get("comentario", "Comentário não encontrado")
                    prob_ia = item.get("prob_IA", 0.0)
                    print(f"  - [{detector}] {comentario} (Probabilidade: {prob_ia:.2f}%)")

                    if prob_ia >= 50.0:
                        acertos += 1

                tema = arquivo.replace("resultados_", "").replace(".json", "")
                porcentagem_acertos = (acertos / total_itens) * 100 if total_itens > 0 else 0
                dados[tema] = {"acertos": acertos, "porcentagem": porcentagem_acertos, "total": total_itens}
    return dados

# Extrair dados
acertos_por_detector = {
    "HuggingFace": extrair_dados(dir_huggingface, "HuggingFace"),
    "Roberta": extrair_dados(dir_roberta, "Roberta")
}

# Função para gerar o gráfico
def plot_bar_chart(acertos_por_detector):
    temas = list(acertos_por_detector["HuggingFace"].keys())
    valores_huggingface_acertos = [acertos_por_detector["HuggingFace"][tema]["acertos"] for tema in temas]
    valores_roberta_acertos = [acertos_por_detector["Roberta"][tema]["acertos"] for tema in temas]
    valores_huggingface_porcentagem = [acertos_por_detector["HuggingFace"][tema]["porcentagem"] for tema in temas]
    valores_roberta_porcentagem = [acertos_por_detector["Roberta"][tema]["porcentagem"] for tema in temas]
    valores_total_comentarios = [acertos_por_detector["HuggingFace"][tema]["total"] for tema in temas]

    x = range(len(temas))

    # Calcular valor máximo para definir limite superior do Y
    max_valor = max(valores_huggingface_acertos + valores_roberta_acertos)
    ylim_top = max_valor * 1.4  # 40% de margem acima da maior barra

    plt.figure(figsize=(12, 8))
    plt.bar(x, valores_huggingface_acertos, width=0.4, label="HuggingFace", color="blue", alpha=0.7)
    plt.bar([p + 0.4 for p in x], valores_roberta_acertos, width=0.4, label="RoBERTa", color="green", alpha=0.7)

    # Textos acima das barras com menor distância
    for i, v in enumerate(valores_huggingface_acertos):
        total = valores_total_comentarios[i]
        texto = f"{v} ({valores_huggingface_porcentagem[i]:.1f}%)\nTotal: {total}"
        plt.text(i, v + max_valor * 0.03, texto,
                 ha='center', va='bottom', fontsize=10, fontweight='bold', color="blue")
    for i, v in enumerate(valores_roberta_acertos):
        total = valores_total_comentarios[i]
        texto = f"{v} ({valores_roberta_porcentagem[i]:.1f}%)\nTotal: {total}"
        plt.text(i + 0.4, v + max_valor * 0.03, texto,
                 ha='center', va='bottom', fontsize=10, fontweight='bold', color="green")

    # Eixos e título em negrito
    plt.xlabel("Temas", fontsize=14, fontweight='bold')
    plt.ylabel("Número de Detecções como IA", fontsize=14, fontweight='bold')
    plt.title("Comentários Detectados como IA por Tema", fontsize=16, fontweight='bold')
    plt.xticks([p + 0.2 for p in x], temas, rotation=45, fontsize=12, fontweight='bold')
    plt.yticks(fontsize=12, fontweight='bold')

    plt.ylim(0, ylim_top)  # Limite do eixo Y com folga
    plt.legend(fontsize=12)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.show()

# Gerar o gráfico
plot_bar_chart(acertos_por_detector)
