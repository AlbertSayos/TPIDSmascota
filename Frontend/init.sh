#!/bin/bash

# Actualizar el índice de paquetes e instalar las herramientas necesarias para Python
sudo apt update

# Detectar la versión de Python 3 instalada
PYTHON_VERSION=$(python3 --version | awk '{print $2}')
PYTHON_MAJOR_MINOR=$(echo $PYTHON_VERSION | cut -d. -f1,2)

# Instalar Python 3 y los paquetes necesarios
sudo apt install -y python${PYTHON_MAJOR_MINOR} python${PYTHON_MAJOR_MINOR}-venv python${PYTHON_MAJOR_MINOR}-dev
# Crear y activar el entorno virtual con pipenv usando la versión detectada de Python
pipenv --python $(which python3)

# Instalar Flask y las demás dependencias
pipenv install flask requests python-dotenv

# Ejecutar la aplicación dentro del entorno virtual
pipenv run python app.py
