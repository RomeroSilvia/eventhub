# Imagen base: Python 3.12 en su versión "slim"
FROM python:3.12-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia el archivo requirements.txt
COPY requirements.txt .

#Instala las dependencias listadas en requirements.txt evitando guardar caché 
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el contenido del proyecto
COPY . .

# Expone el puerto 8000
EXPOSE 8000

# Comandos que se ejecutan cuando se inicia el contenedor:
# migraciones, carga datos e inicia el servidor
CMD ["sh", "-c", "python manage.py migrate && python manage.py migrate cities_light && python manage.py loaddata fixtures/*.json && python manage.py runserver 0.0.0.0:8000"]
