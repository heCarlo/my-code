# Usando a imagem base Python slim
FROM python:3.10-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos de dependências
COPY requirements.txt .

# Instala dependências do sistema e do projeto
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copia o código da aplicação para o container
COPY . .

# Define o comando padrão
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
