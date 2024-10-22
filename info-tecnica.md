# Fab-Blocks-Server: Instalación y ejecución

## 1. Clonar el repositorio
```bash
git clone https://github.com/codigospace/Fab-Blocks-Server.git
cd Fab-Blocks-Server
```

## 2. Crear un entorno virtual
```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

## 4. Ejecutar el proyecto Django
```bash
python manage.py migrate
python manage.py runserver
```

Ahora puedes acceder a la aplicación en http://127.0.0.1:8000/

## Notas adicionales:
- Recuerda activar el entorno virtual cada vez que trabajes con el proyecto usando:
```bash
source venv/bin/activate
```
- Puedes detener el servidor Django presionando Ctrl+C.
- La aplicación utiliza una base de datos SQLite por defecto, que se configura en el archivo `settings.py`.

## Estructura del Proyecto
- **`fabwebdjango/`**: Contiene la configuración del proyecto y el archivo de configuración principal `settings.py`.
- **`fabblocks/`**: La aplicación Django principal del proyecto.
- **`accounts/`**: La aplicación que administra las cuentas de usuarios.
- **`inohub/`**: La aplicación encargada de compilar, procesar y enviar los archivos necesarios para la programación en Arduino, tanto local como externa.
- **`media/`**: La aplicación que maneja los ejemplos, proyectos, imagenes y contenido multimedia a utilizar en la aplicación.
- **`projects/`**: Carpeta que sirve de almacenamiento para los proyectos realizados por usuarios.
- **`manage.py`**: Herramienta de administración para ejecutar comandos de Django.

## Configuración Adicional
1. **Base de Datos**: La configuración predeterminada usa SQLite. Para cambiar a otra base de datos, edita `settings.py` y ajusta la configuración de `DATABASES`.
2. **Archivos Estáticos y Plantillas**: Asegúrate de colocar archivos estáticos y plantillas en las carpetas adecuadas bajo el directorio de la aplicación.