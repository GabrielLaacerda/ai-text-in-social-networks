from transformers import AutoModel

# Carregar o modelo com seus pesos
model = AutoModel.from_pretrained('/home/gabriel/Músicas/')

# Mostrar a arquitetura do modelo
print(model)
