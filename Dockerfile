FROM python:3.11-slim

# Variables de entorno para pip (se incrementa el timeout)
ENV PIP_DEFAULT_TIMEOUT=1000 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 

# Instalar solo las dependencias necesarias
RUN apt-get update && apt-get install -y \
    # Dependencias para WeasyPrint
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libcairo2 \
    # Dependencias para wkhtmltopdf
    wkhtmltopdf \
    xvfb \
    # Dependencias básicas necesarias
    libxml2 \
    libxslt1.1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Establecer directorio de trabajo
WORKDIR /app

# Copiar requirements e instalar dependencias
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --default-timeout=1000 -r requirements.txt

# Crear directorio de salida con permisos
RUN mkdir -p /app/output && chmod 777 /app/output

# Comando por defecto
CMD ["xvfb-run", "python", "src/test_generator.py"]