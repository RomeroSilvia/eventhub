# Imagen base: Python 3.12 en su versión "slim"
FROM python:3.12-slim

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Establece el directorio de trabajo
WORKDIR /app

# Copia el archivo requirements.txt
COPY requirements.txt .

#Instala las dependencias listadas en requirements.txt evitando guardar caché 
RUN pip install --no-cache-dir -r requirements.txt

# Copia entrypoint y le da permisos
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Copia todo el contenido del proyecto
COPY . .

# Expone el puerto 8000
EXPOSE 8000

# Punto de entrada para el contenedor
ENTRYPOINT ["/entrypoint.sh"]

# Comando que se ejecutan cuando se inicia el contenedor: 
CMD ["gunicorn", "--bind", ":8000", "--workers", "2", "eventhub.wsgi:application"]
