# Usa una imagen base ligera con Python
FROM python:3.12-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos del proyecto al contenedor
COPY . /app

# Install system dependencies
RUN apt-get update && apt-get install -y libpq-dev gcc \
    && apt-get clean && rm -rf /var/lib/apt/lists/*



# Instala Poetry y las dependencias del proyecto
RUN pip install poetry && poetry config virtualenvs.create false && poetry install --only main --no-interaction --no-ansi

# Expone el puerto en el que corre la aplicación
EXPOSE 8080

# Comando para correr la aplicación

CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]

