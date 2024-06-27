#!/bin/bash

# Abre una nueva terminal para ejecutar docker-compose
gnome-terminal -- bash -c "cd ./Backend/database && sudo docker-compose up -d --build; exec bash"

# Abre una nueva terminal para ejecutar backend/init.sh
gnome-terminal -- bash -c "cd ./Backend && bash init.sh; exec bash"

# Abre una nueva terminal para ejecutar frontend/init.sh
gnome-terminal -- bash -c "cd ./Frontend && bash init.sh; exec bash"