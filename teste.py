import pandas as pd
import numpy as np
import re
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
import torch
from transformers import BertTokenizer, BertForSequenceClassification, AdamW
from torch.utils.data import DataLoader, TensorDataset
import nltk
nltk.download('stopwords')

# Carregar o dataset de treinamento
train_essays = pd.read_csv("llm-detect-ai-generated-text/train_essays.csv")

# Pré-processamento do texto
stop_words = set(stopwords.words('english'))

def clean_text(text):
    text = re.sub(r'[^\w\s]', '', text)  # Remove pontuações
    words = text.split()  # Tokenização
    words = [word.lower() for word in words if word.isalpha()]  # Minúsculas e remover palavras não alfabéticas
    words = [word for word in words if word not in stop_words]  # Remover palavras de parada
    return ' '.join(words)

train_essays['clean_text'] = train_essays['text'].apply(clean_text)

# Dividir os dados em treinamento e validação
X_train, X_val, y_train, y_val = train_test_split(train_essays['clean_text'], train_essays['generated'], test_size=0.2, random_state=42)

# Tokenização e codificação para BERT
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', do_lower_case=True, padding=True, truncation=True, max_length=64, cache_dir='./bert_cache')

encoded_train = tokenizer(X_train.tolist(), padding=True, truncation=True, return_tensors='pt', max_length=64)
encoded_val = tokenizer(X_val.tolist(), padding=True, truncation=True, return_tensors='pt', max_length=64)

# Converter os rótulos para tensores
train_labels = torch.tensor(y_train.values)
val_labels = torch.tensor(y_val.values)

# Criar TensorDatasets
train_dataset = TensorDataset(encoded_train['input_ids'], encoded_train['attention_mask'], train_labels)
val_dataset = TensorDataset(encoded_val['input_ids'], encoded_val['attention_mask'], val_labels)

# DataLoader para processamento eficiente
train_loader = DataLoader(train_dataset, batch_size=8, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=8, shuffle=False)

# Definir o modelo BERT para classificação de sequência
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=2)
model.to(device)

# Definir otimizador e taxa de aprendizado
optimizer = AdamW(model.parameters(), lr=2e-5, correct_bias=False)
epochs = 10

# Loop de treinamento
for epoch in range(epochs):
    model.train()
    total_loss = 0

    for batch in train_loader:
        input_ids, attention_mask, labels = batch
        input_ids, attention_mask, labels = input_ids.to(device), attention_mask.to(device), labels.to(device)

        optimizer.zero_grad()

        outputs = model(input_ids, attention_mask=attention_mask, labels=labels)
        loss = outputs.loss
        total_loss += loss.item()

        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)  # Clipping de gradientes
        optimizer.step()

    avg_train_loss = total_loss / len(train_loader)
    print(f"Epoch {epoch + 1}/{epochs}, Average Training Loss: {avg_train_loss:.2f}")

# Salvar o modelo treinado e o tokenizador
model.save_pretrained('./trained_model')
tokenizer.save_pretrained('./trained_model')
