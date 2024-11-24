# Usar uma imagem base do Python
FROM python:3.10-slim

# Criar diretório de trabalho
WORKDIR /app

# Copiar os arquivos para o container
COPY . /app

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expor a porta do Flask
EXPOSE 5000

# Comando para rodar o aplicativo
CMD ["flask", "run", "--host=0.0.0.0"]
