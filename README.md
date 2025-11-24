# 🎵 MP3 Tagger Microservice

Este es un microservicio ligero escrito en **Python (FastAPI)** diseñado para funcionar como un "sidecar" o servicio auxiliar para **n8n**.

Su única función es recibir un archivo MP3 y metadatos, incrustar las etiquetas ID3 (incluyendo la carátula) y devolver el archivo procesado sin necesidad de guardar nada en disco.

## 🚀 Características

* **In-Memory Processing:** No guarda archivos temporales, todo ocurre en la memoria RAM.
* **Soporte de Carátulas:** Incrusta imágenes (JPG/PNG) como portada del álbum.
* **Ligero:** Basado en `python:3.9-slim` y `mutagen`.
* **Docker Ready:** Listo para desplegar en Easypanel, Portainer o Docker Compose.

## 🛠️ Instalación / Despliegue

### En Easypanel (Recomendado)

1.  Crea un servicio de tipo **App**.
2.  Conecta este repositorio.
3.  Configura el puerto interno en `8000`.
4.  Nombre del servicio (Service Name): `mp3tagger` (Importante para la conexión interna con n8n).

### En Local (Docker)

```bash
# Construir la imagen
docker build -t mp3tagger .

# Correr el contenedor
docker run -p 8000:8000 mp3tagger
