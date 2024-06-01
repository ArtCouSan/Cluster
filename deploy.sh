#!/bin/bash

# Atualizar o sistema e instalar pré-requisitos
echo "Atualizando o sistema e instalando pré-requisitos..."
sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common


# Instalação do Docker, se necessário
if ! command -v docker &> /dev/null; then
    echo "Docker não está instalado. Instalando Docker..."
    sudo apt-get update
    sudo apt-get install -y docker.io
    sudo systemctl start docker
    sudo systemctl enable docker
    echo "Docker instalado com sucesso."
fi

# Instalação do MicroK8s, se necessário
if ! command -v microk8s &> /dev/null; then
    echo "MicroK8s não está instalado. Instalando MicroK8s..."
    sudo snap install microk8s --classic
    sudo usermod -a -G microk8s $USER
    sudo chown -f -R $USER ~/.kube
    newgrp microk8s
    echo "MicroK8s instalado com sucesso."
fi

# Habilitar o Docker Registry do MicroK8s
echo "Habilitando o Docker Registry do MicroK8s..."
microk8s enable registry

# Esperar o MicroK8s estar pronto após habilitar o registry
microk8s status --wait-ready

# Definindo os caminhos para os arquivos YAML
NAMESPACE="infraestrutura/01-namespaces.yaml"
PV="infraestrutura/02-pv-volume.yaml"
PVC="infraestrutura/03-pvc-volume.yaml"
SECRET="infraestrutura/04-secrets.yaml"
MYSQL="infraestrutura/05-mysql-deployment.yaml"
FLASK="infraestrutura/06-flask-deployment.yaml"
SERVICES="infraestrutura/07-services.yaml"

# Construir e enviar a imagem do Flask para o Registry do MicroK8s
FLASK_IMAGE_NAME="localhost:5000/sensorapi:latest"
echo "Construindo a imagem Flask: $FLASK_IMAGE_NAME"
docker build -t $FLASK_IMAGE_NAME -f app/Dockerfile.flask .
echo "Enviando a imagem Flask para o Registry local..."
docker push $FLASK_IMAGE_NAME

# Construir e enviar a imagem MySQL para o Registry do MicroK8s
MYSQL_IMAGE_NAME="localhost:5000/mysqlcustom:latest"
echo "Construindo a imagem MySQL: $MYSQL_IMAGE_NAME"
docker build -t $MYSQL_IMAGE_NAME -f app/Dockerfile.mysql .
echo "Enviando a imagem MySQL para o Registry local..."
docker push $MYSQL_IMAGE_NAME

if [ $? -ne 0 ]; then
    echo "Erro ao enviar imagens para o Registry. Abortando."
    exit 1
fi

# Aplicando os arquivos YAML
echo "Aplicando configurações de Namespace..."
microk8s kubectl apply -f $NAMESPACE

echo "Aplicando configurações de Persistent Volume..."
microk8s kubectl apply -f $PV
microk8s kubectl apply -f $PVC

echo "Aplicando configurações de Secrets..."
microk8s kubectl apply -f $SECRET

echo "Aplicando configurações do Deployment do MySQL..."
microk8s kubectl apply -f $MYSQL

echo "Aplicando configurações do Deployment do Flask..."
microk8s kubectl apply -f $FLASK

echo "Aplicando configurações dos Services..."
microk8s kubectl apply -f $SERVICES

echo "Verificando status dos Deployments e Services..."
microk8s kubectl get deployments
microk8s kubectl get services

echo "Deploy concluído com sucesso."
