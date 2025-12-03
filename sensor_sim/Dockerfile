FROM python:3.11-slim

WORKDIR /app

# Instala dependencias mínimas
RUN pip install --no-cache-dir requests

# Copia los scripts de simulación
COPY simple_data_forest.py obs_periodica.py ./

# Comando por defecto: lanzar el bucle de observaciones
CMD ["python", "obs_periodica.py"]
