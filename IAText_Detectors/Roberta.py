import warnings
from transformers import AutoModelForSequenceClassification, AutoTokenizer, logging
import torch.nn.functional as F

warnings.filterwarnings("ignore")

# Desabilitar logs do transformers (Hugging Face)
logging.set_verbosity_error()

# Define o repositório do modelo
model_name = "roberta-large-openai-detector"

# Baixa o modelo e o tokenizer
model = AutoModelForSequenceClassification.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)


text = "este texto foi escrito por IA"
inputs = tokenizer(text, return_tensors="pt")
outputs = model(**inputs)

logits = outputs.logits

# Aplica softmax para obter as probabilidades
probabilities = F.softmax(logits, dim=-1)

# Obtém a probabilidade de ser IA e de ser humano
prob_ia = probabilities[0][1].item()  # Probabilidade de ser IA
prob_human = probabilities[0][0].item()  # Probabilidade de ser humano

# Exibe as probabilidades
print(f"Probabilidade de ser IA: {prob_ia:.4f}\n")
print(f"Probabilidade de ser humano: {prob_human:.4f}")

# Exibe a classificação
prediction = logits.argmax(-1).item()  # Obtém a classe com maior pontuação
if prediction == 1:
    print("Texto gerado por IA")
else:
    print("Texto humano")
