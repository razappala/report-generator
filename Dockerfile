FROM python:3.11-slim

# Configurar variables de entorno para pip y XDG_RUNTIME_DIR
ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    XDG_RUNTIME_DIR=/tmp/runtime-root

# Instalar dependencias del sistema para WeasyPrint y wkhtmltopdf
RUN apt-get update && apt-get install -y \
    build-essential \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libcairo2 \
    libffi-dev \
    libssl-dev \
    libxml2 \
    libxslt1.1 \
    libjpeg-dev \
    zlib1g-dev \
    wget \
    xvfb \
    wkhtmltopdf \
    libxrender1 \
    libfontconfig1 \
    libfreetype6 \
    libjpeg62-turbo \
    libpng-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Establecer directorio de trabajo
WORKDIR /app

# Copiar el archivo requirements.txt
COPY requirements.txt /app/requirements.txt

# Instalar dependencias de Python
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Establecer permisos para la carpeta output
RUN mkdir -p /app/output && chmod -R 755 /app && chmod 777 /app/output\
# Comando por defecto
CMD ["xvfb-run", "python", "src/test_generator.py"]