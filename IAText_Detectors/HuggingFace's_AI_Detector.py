import os
import requests
import time

# Substitua pela sua chave de API
token = os.getenv('HUGGING_FACE_API_KEY')

model_name = "PirateXX/AI-Content-Detector"

# Texto a ser analisado
text = "Este é um exemplo de texto gerado por IA."

# URL da API
api_url = f"https://api-inference.huggingface.co/models/{model_name}"

# Cabeçalhos da requisição, incluindo a autenticação
headers = {
    "Authorization": f"Bearer {token}"
}

# Dados para a requisição
data = {
    "inputs": text
}

# Tentar novamente até o modelo estar disponível
while True:
    response = requests.post(api_url, headers=headers, json=data)

    if response.status_code == 503:
        print("Modelo ainda está carregando... tentando novamente em 20 segundos.")
        time.sleep(20)  # Espera o tempo estimado antes de tentar novamente
        continue
    elif response.status_code == 200:
        result = response.json()
        if isinstance(result, list) and len(result) > 0:
            scores = {item["label"]: item["score"] for item in result[0]}
            prob_ia = scores.get("LABEL_1", 0) * 100  # Convertendo para porcentagem
            prob_human = scores.get("LABEL_0", 0) * 100  # Convertendo para porcentagem

            print(f"Texto analisado: {text}")
            print(f"Porcentagem de ser IA: {prob_ia:.2f}%")
            print(f"Porcentagem de ser humano: {prob_human:.2f}%")

            if prob_ia > prob_human:
                print("Conclusão: O texto é provavelmente gerado por IA.")
            else:
                print("Conclusão: O texto é provavelmente humano.")
        else:
            print(f"Erro no formato do resultado: {result}")
        break
    else:
        print("Erro:", response.status_code, response.text)
        break
