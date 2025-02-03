import os
import torch
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
from datasets import Dataset
import pandas as pd
from sklearn.model_selection import train_test_split

# Caminho para os diretórios dos datasets
datasets_paths = [
    "TuringBench/TuringBench/TT_gpt1",
    "TuringBench/TuringBench/TT_gpt2_large",
    "TuringBench/TuringBench/TT_gpt2_medium",
    "TuringBench/TuringBench/TT_gpt3",
    "TuringBench/TuringBench/TT_grover_mega",
    "TuringBench/TuringBench/TT_pplm_gpt2"
]

# Carregar dados
def load_text_data(dataset_paths):
    texts = []
    labels = []
    label_map = {
        "TT_gpt1": 0,
        "TT_gpt2_large": 1,
        "TT_gpt2_medium": 2,
        "TT_gpt3": 3,
        "TT_grover_mega": 4,
        "TT_pplm_gpt2": 5
    }

    # Itera sobre os diretórios de datasets
    for dataset_path in dataset_paths:
        if not os.path.exists(dataset_path):
            print(f"Diretório {dataset_path} não encontrado!")
            continue

        dataset_name = os.path.basename(dataset_path)
        print(f"Carregando dados de: {dataset_name}")

        # Verifica os arquivos CSV presentes: train.csv, test.csv, valid.csv
        for filename in ['train.csv', 'test.csv', 'valid.csv']:
            file_path = os.path.join(dataset_path, filename)

            if os.path.exists(file_path):
                print(f"Carregando o arquivo: {filename}")
                df = pd.read_csv(file_path)

                # Verifique se as colunas 'Generation' e 'label' estão presentes
                if 'Generation' in df.columns and 'label' in df.columns:
                    texts.extend(df['Generation'].dropna().tolist())  # Adiciona os textos
                    labels.extend(df['label'].dropna().tolist())  # Adiciona os rótulos
                else:
                    print(f"Colunas esperadas 'Generation' e 'label' não encontradas no arquivo {filename}")
            else:
                print(f"Arquivo {filename} não encontrado em {dataset_path}")

    if not texts:
        print("Nenhum dado de texto encontrado nos diretórios!")

    return texts, labels



# Carregar dados
texts, labels = load_text_data(datasets_paths)

# Dividir os dados em treino e teste
train_texts, test_texts, train_labels, test_labels = train_test_split(texts, labels, test_size=0.2)

# Carregar o tokenizer BERT
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')


# Função para tokenizar os dados
def tokenize_function(texts):
    return tokenizer(texts, padding=True, truncation=True, max_length=512)


# Tokenizar os dados
train_encodings = tokenize_function(train_texts)
test_encodings = tokenize_function(test_texts)

# Criar os datasets
train_dataset = Dataset.from_dict(
    {'input_ids': train_encodings['input_ids'], 'attention_mask': train_encodings['attention_mask'],
     'labels': train_labels})
test_dataset = Dataset.from_dict(
    {'input_ids': test_encodings['input_ids'], 'attention_mask': test_encodings['attention_mask'],
     'labels': test_labels})

# Carregar o modelo BERT para classificação
model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=6)

# Definir argumentos de treinamento
training_args = TrainingArguments(
    output_dir='./results',  # Diretório para salvar os resultados
    num_train_epochs=3,  # Número de épocas
    per_device_train_batch_size=8,  # Tamanho do batch para treino
    per_device_eval_batch_size=16,  # Tamanho do batch para avaliação
    warmup_steps=500,  # Número de steps de aquecimento
    weight_decay=0.01,  # Taxa de decaimento
    logging_dir='./logs',  # Diretório de logs
    logging_steps=10,
)

# Inicializar o Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=test_dataset
)

# Treinar o modelo
trainer.train()

# Avaliar o modelo
results = trainer.evaluate()
print(results)
