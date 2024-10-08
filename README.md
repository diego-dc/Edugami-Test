# Edugami-Test App

Esta aplicación apunta a cumplir con los requisitos de una prueba de reclutamiento realizada para Edugami. Una aplicación basada en Django para gestionar los puntajes de estudiantes en pruebas, permitiendo a los estudiantes enviar sus respuestas y calcular sus puntajes, junto con estadísticas sobre respuestas correctas, incorrectas y omitidas.

## Características

- **Creación de Alumnos**: Facilita la creación de registros de estudiantes en el sistema. Esto se hizo como extra para la interfaz.
- **Subida de Pruebas**: Permite crear nuevas pruebas que pueden ser asignadas a los estudiantes.
- **Envío de Respuestas de Pruebas**: Se simula como Los estudiantes podrían enviar sus respuestas para una prueba específica.
- **Asignación de Pruebas a Alumnos**: Permite asignar pruebas específicas a los estudiantes seleccionados.
- **Mandar o Revisar Respuestas de una Prueba**: se pueden enviar o revisar resultados para una prueba.
  > Nota: Se crean además dos GET más para ver de forma interactiva una lista de los estudiantes creados y las pruebas creadas. Esperando que esto facilite un poco la visualización de las pruebas desde la interfaz.

## Tecnologías Utilizadas

- **Django**: Framework backend utilizado para gestionar solicitudes, modelos, vistas y la administración de bases de datos.

- **HTML, Bootstrap y JavaScript**: Utilizados para crear las plantillas front-end y crear una interfaz de usuario simple para facilitar una funcionalidad interactiva.

## Requisitos previos

- Python 3.12
- Django 5.1

## Estructura del Proyecto

Edugami_test/

├── edugami_test/ # Directorio core del proyecto Django (Acá van los settings y urls generales, pero al estar en local no hay mucho que recalcar acá.)

│

├── edugami_app/ # Directorio de la app Django creada.

│

├── edugami_app/models.py # Acá se define el modelo de datos utilizado para esta prueba.

│

├── edugami_app/views.py # Acá se encuentran las vistas y la lógica para el envío y procesamiento de las requests HTTPS.

│

├── edugami_app/urls.py # Define las rutas URL para la aplicación, se utilizan las mismas mencionadas en el test.

│

└── edugami_app/templates/ # Plantillas HTML para renderizar la interfaz de usuario de la aplicación.

│

├── edugami_app/static/ # Acá se encuentran los archivos estáticos (CSS, JS). El archivo index.js contiene toda la lógica para manejar las solicitudes HTTP y actualizar la interfaz de usuario con los datos obtenidos de la API. En el CSS se utilizaron algunas clases para mejorar la visual de la interfaz, lo demás se complementó con Bootstrap.

|

├── manage.py # Script de gestión de Django

└── README.md # Archivo README del proyecto (este archivo)

## Endpoints de la API

- **Agregar Estudiantes**: `/add_students/`

  - Método: `POST`
  - Descripción: Permite agregar nuevos estudiantes a la base de datos.

- **Obtener Lista de Estudiantes**: `/get_students/`

  - Método: `GET`
  - Descripción: Recupera la lista de todos los estudiantes almacenados en la base de datos.

- **Obtener Lista de Tests**: `/get_tests/`

  - Método: `GET`
  - Descripción: Recupera la lista de todas las pruebas disponibles en la base de datos.

- **Crear una Prueba**: `/test/`

  - Método: `POST`
  - Descripción: Permite crear una nueva prueba en la base de datos.

- **Asignar Prueba a Estudiante**: `/test/<int:test_id>/assign/`

  - Método: `POST`
  - Descripción: Asigna una prueba específica a los estudiantes especificados.

- **Enviar o Solicitar Respuestas**: `/test/<int:test_id>/answers/`

  - Método: `POST` (para enviar respuestas) / `GET` (para obtener respuestas)
  - Descripción: Permite a los estudiantes enviar sus respuestas para una prueba específica o recuperar las respuestas enviadas por un(unos) estudiante(s) para dicha prueba.

## Modelo de Datos

El modelo de datos está compuesto por las siguientes entidades:

- **TagEnum**: Enumeración que define los tipos de etiquetas para las preguntas.

- **Alternative**: Representa las alternativas de respuesta para cada pregunta.

- **Question**: Representa una pregunta en el test.

- **Test**: Representa un test que contiene varias preguntas.

- **Student**: Representa a un estudiante que puede realizar múltiples tests.

- **StudentTestScore**: Representa la relación entre estudiantes y pruebas, esto permite que un estudiante tenga multiples pruebas y además que se pueda registrar el puntaje obtenido por un estudiante en un test específico y las estadisticas de este en dicha prueba.
  > **Nota**: Se garantiza que un estudiante solo tenga un puntaje por test.

## Cómo Ejecutar el Proyecto

1.  **Clonar el repositorio**:

```bash
git clone https://github.com/diego-dc/Edugami-Test.git
```

2. Instalar las dependencias:

```bash
pip install -r requirements.txt
```

3. Ejecutar las migraciones de la base de datos:
4.

```
python manage.py makemigrations

python manage.py migrate
```

4. Ejecutar el servidor de desarrollo:

```bash
python manage.py runserver
```

Acceder a la aplicación en http://localhost:8000/.

## Ejemplo de Uso

Aquí hay un ejemplo de cómo enviar respuestas de pruebas:

1. Poblar datos iniciales en la DB.
   - Es posible simplemente utilizar la interfaz de usuario con el JSON de los estudiantes que se quieren crear o bien utilizar el comando para cargar una lista de estudiantes desde un archivo que se dispuso para este fin:
     `python manage.py loaddata edugami_app/fixtures/initial_data_students.json`
2. Asegurarse que existan estudiantes y pruebas creadas. (Ver las tablas.)
3. Asignar una prueba a un estudiante.
4. Enviar las respuestas de la prueba a través del formulario.
5. Ver el resultado obtenido de las solicitudes HTTPS en la sección de resultado, o bien las alertas por si hubo algún error.
   > Nota: Con la interfaz de usuario se espera facilitar las pruebas, pero cualquier otro medio que colabore el trabajo realizado es válido.

## Notas del proyecto a considerar:

- **Modelo de Datos**: Se utilizó el modelo planteado en el test, y se utilizaron como modelos extras: Question, Alternatives y StudentTestScore, para simplificar la implementación y aprovechar los models de Django. StudentTestScore se utilizó como una tabla intermediara de la relación entre estudiantes y pruebas, este modelo podría permitir futuras acciones especificas para una prueba de un estudiantes, entre ellas feedback por ejemplo.

- **Interfaz de Usuario**: No estoy seguro si se esperaba que la aplicación sólo pudiera procesar las solicitudes, pero ante la duda se creó una interfaz simple para facilitar las pruebas. No es necesario utilizar este medio, pero quedó como una gran forma de visualizar más rápidamente lo que ocurre en la app.

- **URLS**: Se utilizaron las mismas rutas utilizadas en el test.

- **Manejo de errores y consideraciones tomadas**: Se tomaron las restricciones más lógicas y las mencionadas, como que un test tenga máx. 5 preguntas. En los ejemplos de las pruebas se usaron "tags" y "score", y en otro no, por lo que se designaron valores defaults en caso de que no vengan. También se asumió que siempre vendrá una alternativa correcta en las creación de pruebas/preguntas. En el código quedan comentados los errores y casos que se podrían considerar como restricciones. Se asumió que los JSON llegarán como se mencionaba en los ejemplos. Para errores se dejó los mensajes por default, y se crearon algunos para casos específicos, como que no venga un dato, o cosas por el estilo. Si es un error del procesamiento, se entregó como indicaban los ejemplos.

## Obtener Recomendaciones - Pregunta Propuesta.

Para un sistema de recomendaciones, creo que igual tendría que ser un poco mas robusto el sistema. Para esto creo sería importante que las recomendaciones vayan vinculadas a las preguntas especificas que los estudiantes fallan o se saltan. En mi versión al tener una relación entre estudiante y test en una tabla intermediara, se permite que un estudiante tenga multiples tests, y además se podría crear una especie de feedback con facilidad, pero esto solo sería posible para los resultados de la prueba en su totalidad, es decir, según sus estadísticas finales se podrían agregar un campo extra, para entregar comentarios a ese alumno sobre el resultado final de su prueba.

Ahora, para que tuviera mayor valor, y fuera especifico a cada pregunta, se tendría que registrar las respuestas de los estudiantes y vincularlas a estos, o al menos las que fallan o se saltan. (En esta versión solo se guarda lo que vendría siendo el score final y las estadísticas, que no tienen mucho valor formativo por decirlo de alguna manera.).

Al tener estos datos, se podría desplegar para cada estudiante en especifico las preguntas que fallaron, y una recomendación al respecto que los ayude a entender o mejorar en ese tipo de preguntas. Junto con esto, se podría analizar si el estudiante va mejorando, mantiene o empeora su rendimiento, para los diferentes tipos de preguntas.
