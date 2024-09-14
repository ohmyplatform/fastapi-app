# Aplicación de Ejemplo: FastAPI con MariaDB en Kubernetes

Esta es una aplicación de ejemplo desarrollada en Python utilizando FastAPI, diseñada para propósitos de pruebas y demostraciones. La aplicación expone una API REST que permite listar, obtener y crear cursos, conectándose a una base de datos MariaDB. Está preparada para ser desplegada en Kubernetes y utiliza GitHub Actions para construir y publicar la imagen Docker en GitHub Container Registry (GHCR).

## Tabla de Contenidos

- [Descripción](#descripción)
- [Características](#características)
- [Requisitos](#requisitos)
- [Configuración](#configuración)
- [Construcción y Publicación de la Imagen Docker](#construcción-y-publicación-de-la-imagen-docker)
- [Uso de la API](#uso-de-la-api)
- [Notas](#notas)
- [Licencia](#licencia)

## Descripción

La aplicación es un servicio sencillo que gestiona información sobre cursos. Proporciona endpoints para:

- Listar todos los cursos.
- Obtener un curso específico por ID.
- Crear un nuevo curso.

La aplicación está pensada para fines educativos y de prueba, demostrando cómo construir y desplegar una aplicación basada en FastAPI y MariaDB en un entorno de Kubernetes, utilizando GitHub Actions y GHCR para la integración continua y el despliegue continuo (CI/CD).

## Características

- **API RESTful** desarrollada con **FastAPI**.
- Conexión a **MariaDB** para almacenamiento de datos.
- **Dockerización** de la aplicación para facilitar su despliegue.
- Uso de **GitHub Actions** para automatizar la construcción y publicación de la imagen Docker.
- Despliegue en **Kubernetes** utilizando manifiestos YAML para los recursos necesarios.
- Lectura de la configuración a través de **variables de entorno**.

## Requisitos

- **Git** para clonar el repositorio.
- **Docker** para construir y ejecutar la imagen localmente.
- **Kubernetes** para el despliegue en cluster.
- **kubectl** configurado para interactuar con el cluster de Kubernetes.
- **Cuenta de GitHub** para acceder al código y configurar GitHub Actions.
- **GitHub Container Registry** (GHCR) para alojar la imagen Docker.

## Configuración

La aplicación requiere una variable de entorno para la conexión a la base de datos:

- `DATABASE_URL`: La cadena de conexión a la base de datos MariaDB en el formato `mysql+pymysql://usuario:contraseña@host:puerto/nombre_base_datos`.

Ejemplo:

```
DATABASE_URL=mysql+pymysql://dbuser:dbpassword@mariadb:3306/courses_db
```

## Construcción y Publicación de la Imagen Docker

### Construir la Imagen Localmente

Para construir la imagen Docker de la aplicación localmente, ejecute:

```bash
docker build -t fastapi-mariadb-test .
```

### Ejecutar la Imagen Localmente

Para ejecutar la imagen Docker localmente:

```bash
docker run -d -p 80:80 -e DATABASE_URL='mysql+pymysql://dbuser:dbpassword@localhost:3306/courses_db' fastapi-mariadb-test
```

### Publicación en GitHub Container Registry

La imagen Docker se construye y publica automáticamente en GHCR mediante GitHub Actions al hacer push a la rama `main`.

## Uso de la API

La API expone los siguientes endpoints:

- `GET /courses`: Lista todos los cursos.
- `GET /courses/{course_id}`: Obtiene un curso por su ID.
- `POST /courses`: Crea un nuevo curso.

### Ejemplo de Petición `POST /courses`

```bash
curl -X POST "http://localhost/courses" -H "Content-Type: application/json" -d '{
  "name": "Curso de Prueba",
  "description": "Este es un curso de prueba"
}'
```

### Documentación Interactiva
Puede acceder a la documentación interactiva de la API generada automáticamente por Swagger UI en `http://localhost/docs`.

## Notas
- **Propósito de Prueba**: Esta aplicación es para fines de prueba y no está destinada para entornos de producción.
- **Configuración de Variables de Entorno**: Asegúrese de configurar correctamente las variables de entorno necesarias, especialmente al desplegar en Kubernetes.
- **Base de Datos**: La aplicación creará automáticamente la base de datos y la tabla courses si no existen.
- **Seguridad**: Las credenciales y datos sensibles se manejan a través de Secrets en Kubernetes y variables de entorno en Docker.
