📜 Projeto de Geração e Detecção de Texto com LLMs

📌 Descrição

Este projeto utiliza Modelos de Linguagem (LLMs) para gerar comentários e detectores de IA para verificar a autenticidade do texto. O sistema processa entradas por meio de diversos scripts organizados em diretórios específicos.

📂 Estrutura do Projeto

📁 Projeto
│-- 📄 app.py                      # Arquivo principal
│-- 📁 LLMs                        # Scripts de geração de texto com LLMs
│-- 📁 IAText_Detectors            # Detectores de texto gerado por IA
│-- 📁 Comentarios_Gerados_PrimeiraEtapa  # Comentários gerados pelos LLMs
│-- 📄 requirements.txt             # Pacotes necessários

🚀 Como Executar

Clone o repositório:

git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio

Crie um ambiente virtual e ative-o:

python3 -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows

Instale as dependências:

pip install -r requirements.txt

Configure as variáveis de ambiente:

export COHERE_API_KEY="sua-chave-aqui"

Para definir permanentemente, adicione ao ~/.bashrc ou ~/.zshrc:

echo 'export COHERE_API_KEY="sua-chave-aqui"' >> ~/.bashrc
source ~/.bashrc

Execute o programa:

python app.py

🛠 Dependências Principais

As dependências do projeto estão listadas no arquivo requirements.txt. Alguns dos pacotes principais incluem:

transformers → Modelos de linguagem

torch → Framework para aprendizado profundo

cohere → API de geração de texto

numpy → Manipulação de arrays numéricos

Para instalar todas as dependências, execute:

pip install -r requirements.txt

📝 Notas

Certifique-se de que o CUDA está corretamente instalado se estiver utilizando modelos acelerados por GPU.

Os comentários gerados pelos modelos serão armazenados em Comentarios_Gerados_PrimeiraEtapa.

O diretório IAText_Detectors contém scripts para identificar textos gerados por IA.

📜 Licença

Este projeto está licenciado sob a MIT License.

Se precisar de mais detalhes ou suporte, fique à vontade para contribuir! 🚀


