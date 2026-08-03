# Imagen base optimizada de Python
FROM python:3.12-slim

# Evitar escritura de bytecode y habilitar buffer de salida
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8080

WORKDIR /app

# Instalar uv para gestión ultrarrápida de dependencias
RUN pip install --no-cache-dir uv

# Copiar archivos de configuración de dependencias
COPY backend/pyproject.toml backend/uv.lock ./backend/

# Instalar dependencias en el entorno del sistema dentro del contenedor
WORKDIR /app/backend
RUN uv pip install --system .

# Copiar el código del proyecto backend
COPY backend/ /app/backend/

# Exponer puerto para Cloud Run
EXPOSE 8080

# Comando de inicio del bot
CMD ["python", "main.py"]
