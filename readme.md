# Asistente virtual que actúa como un profesor de inglés nativo

## Introducción:
Se pretende diseñar y desarrollar un Chatbot u asistente virtual que se comporte como un profesor nativo Inglés el cual sirva para estudiar y practicar el idioma con un nivel A1. Que permita entre otras cosas mantener conversaciones manteniendo un nivel de conversación adecuado al nivel, poder consultar dudas sobre gramática o  que genere textos redactados en inglés, entre otras opciones. En todo momento podrá corregir malos hábitos y recomendar buenas formas  en la escritura.

Eres libre de usar este script para tu uso y para el fin que quieras.

El objetivo de este proyecto es solo un prototipo para evaluar el nuevo modelo de **Anthropic,  Claude 3.5 Sonnet.**

## Requisitos:

 - Desarrollado en Python
 - La conversación se guarda en una base de datos sqllite. 
 - En cualquier momento podemos resetear la sesión y por ende borrar la base de datos, pero guardando una copia en PDF del contexto, así como un MP3 de la conversación mantenida, para poder escuchar posteriormente y las veces que queramos la pronunciación.
 - Usamos el modelo *Claude 3.5 Sonnet* usando su Api.

## Librerías usadas:

 - **gTTS** (Google Text-to-Speech) https://pypi.org/project/gTTS/ Librería que va a permitir generar el MP3 del  contexto y con el que se puede elegir el acento del tono, en nuestro caso: *inglés británico*.
 - **Anthropic Python API library** https://pypi.org/project/anthropic/ Librería para el acceso al API REST de Anthropic.
 - **PyFPDF** https://pypi.org/project/fpdf/ Librería para generar de forma sencilla PDFs.
 - **python-dotenv** https://pypi.org/project/python-dotenv/ Librería para lectura de ficheros .ENV

## Instalación y uso:

 - Clona el repositorio en local en la ubicación que desees.
 - Crea y edita el fichero **.env** y añade tu api key de Anthropic, la puedes generar en https://console.anthropic.com/  
*`ANTHROPIC_API_KEY="tu clave api key"`*.
**Nota:** supone un coste, pero es bastante asequible. A día de hoy (Julio 2024) si añades tu teléfono en tu registro, te regalan 5$ para evaluar, más que suficiente para probar este script.
 - Crea un entorno virtual, por ejemplo: *`python3 -m venv venv`*.
 - Instala todas las dependencias: *`pip install -r  requirements.txt`*
 - Ejecuta el script: *`python3 main.py`*
 - Puedes teclear ***exit***, para salir del Agente manteniendo la conversación y contexto en la base de datos para la siguiente ejecución o teclear ***clear*** el cual limpia la base de datos y guarda la conversacion y contexto en un PDF con el timestamp en la carpeta HISTORIC de la ubicación del proyecto, ademas de un MP3 con la transcripción en audio del contexto salvado en PDF en tono "inglés británico".

## Mejoras:

Posibles mejoras y/o modificaciones:

 - Puedes cambiar el prompt del Asistente como desees.
 - Aunque el asistente  se le ha indicado que la conversación ha de ser manteniendo un nivel A1, puedes jugar con otros niveles (A2, B1, B2, C1 o C2). Incluso lo podrías hacer configurable.
 - Puedes añadir un GUI o entorno gráfico, dispones de varias librerías:  Streamlit o Google Mesop entre otras.
 - Puedes adaptar el script a un API, realizada con FastAPI, Flask etc y monetizarlo, ideal para academias de idiomas o para uso en centros de estudio como Colegios u Universidades.
 - Se podría añadir la opción de añadir audios con nuestra pronunciación y el asistente corregir los errores gramaticales o fonéticos, proponiendo mejoras.
 - Se podría crear una App  RAG, adaptando este script en el cual se añada el temario de la *Escuela Oficial de Idiomas*, asi como "exámenes tipo" y de esa forma el Asistente podría incluso generar tests u exámenes. Se podría hacer uso de los frameworks, **LangChain** o **LlamaIndex** para su implementación. 
 - Escalabilidad: Considera usar un sistema de colas para manejar muchas solicitudes simultáneas. Por ejemplo **Celery**
- gTTS, no tiene muchas opciones de cambiar la voz, por ejemplo a la de un hombre. Si, la tonalidad basada en la localización, por ejemplo puedes cambiar un tono de un inglés de Estados unidos o de Australia. Si necesitas algo más profesional y con otro tipo de tonos y voces (incluso podrias clonar tu propia voz), puedes usar el servicio de https://elevenlabs.io/
## Versiones:

 - Version 0.9 : Julio 2024. Commit inicial.

Si necesitas ideas, noticias o código para tus proyectos SaaS o para tu próxima startup únete a mi comunidad en Telegram: https://t.me/izarlabs


