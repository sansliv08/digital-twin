FROM python:3.12-slim

WORKDIR /app

# Instala dependências básicas do sistema para compilar pacotes Python se necessário
RUN apt-get update && apt-get install -y --no-install-recommends gcc && rm -rf /var/lib/apt/lists/*

# Instala as dependências do projeto
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código do backend (server.py, context.py, resources.py, pasta data/, etc.)
COPY . .

# Cria a pasta de memória dentro do contentor e define as variáveis padrão
RUN mkdir -p /app/memory
ENV PORT=80
ENV MEMORY_DIR="/app/memory"
ENV USE_S3="false"

# Expõe a porta 80 exigida pelo Coolify
EXPOSE 80

# Arranca o servidor FastAPI na porta 80
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "80"]