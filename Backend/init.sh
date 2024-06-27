init.sh back
#!/bin/bash

# Actualizar el índice de paquetes e instalar Python 3.10 si es necesario
# Detectar la versión de Python 3 instalada
PYTHON_VERSION=$(python3 --version | awk '{print $2}')
PYTHON_MAJOR_MINOR=$(echo $PYTHON_VERSION | cut -d. -f1,2)

# Instalar Python 3 y los paquetes necesarios
sudo apt install -y python${PYTHON_MAJOR_MINOR} python${PYTHON_MAJOR_MINOR}-venv python${PYTHON_MAJOR_MINOR}-dev

# Instalar Flask y las demás dependencias
pipenv install flask
pipenv install SQLAlchemy Flask-SQLAlchemy mysql-connector-python PyJWT Flask-JWT-Extended

# Ejecutar la aplicación dentro del entorno virtual
pipenv run python app.py

