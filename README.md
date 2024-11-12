
# Snake AI con Reinforcement Learning

Este proyecto implementa un juego de Snake que utiliza aprendizaje por refuerzo (Reinforcement Learning) para entrenar una IA que juegue de forma autónoma.

## Requisitos Previos

### 1. Instalar Miniconda

Miniconda es una versión ligera de Anaconda que incluye solo conda y sus dependencias.

1. Descarga Miniconda para tu sistema operativo desde [aquí](https://docs.conda.io/en/latest/miniconda.html)

2. Instala Miniconda:
   - **Windows**: Ejecuta el instalador descargado
   - **Linux/Mac**: Abre una terminal y ejecuta:
     ```bash
     bash Miniconda3-latest-Linux-x86_64.sh
     ```
     (Reemplaza el nombre del archivo según tu descarga)

3. Verifica la instalación:
   ```bash
   conda --version
   ```

### 2. Crear y Activar el Entorno Virtual

1. Clona este repositorio:
   ```bash
   git clone [URL-del-repositorio]
   cd [nombre-del-repositorio]
   ```

2. Crea un nuevo entorno virtual:
   ```bash
   conda create --name snake-ai python=3.8
   ```

3. Activa el entorno:
   - **Windows**:
     ```bash
     conda activate snake-ai
     ```
   - **Linux/Mac**:
     ```bash
     source activate snake-ai
     ```

### 3. Instalar Dependencias

Con el entorno activado, instala las dependencias necesarias:

