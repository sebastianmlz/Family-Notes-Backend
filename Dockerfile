# 1. Imagen base: Usamos una versión "slim" de Python para ahorrar RAM y espacio
FROM python:3.12-slim

# 2. Variables de entorno: Evitan que Python genere archivos .pyc y aseguran logs en tiempo real
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Directorio de trabajo: Donde vivirá el código dentro del contenedor
WORKDIR /app

# 4. Dependencias del sistema: Necesarias para que psycopg2 se comunique con NeonDB
RUN adduser --disabled-password --gecos "" appuser

# 5. Instalación de librerías de Python: Copiamos solo el requirements primero para usar el caché de Docker
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copiar el código: Ahora sí, pasamos todo tu proyecto al contenedor
COPY --chown=appuser:appuser . /app/

# 7. Puerto: Avisamos que Django escuchará en el 8000
USER appuser
EXPOSE 8000

# 8. Comando de inicio: Lo que arranca el servidor
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]