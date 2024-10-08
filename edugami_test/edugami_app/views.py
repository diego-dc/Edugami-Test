from django.shortcuts import render
from django.http import JsonResponse
import json
from .models import *
from django.views.decorators.csrf import csrf_exempt

# vistas creadas para el test

def Index(request):
    """
    Descripción:
    Vista que renderiza la página de llegada.

    Parámetros:
    - request: El objeto HttpRequest enviado por el cliente.   

    Returns:
    El renderizado del template index.html

    Lógica:
    Renderiza la página.

    Errores:
    -----

    """
    return render(request, 'index.html')

@csrf_exempt
def GetStudents(request):
    """
    Descripción:
    Vista que obtiene todos los estudiantes.

    Parámetros:
    - request: El objeto HttpRequest enviado por el cliente.

    Returns:
    JsonResponse con la lista de estudiantes.

    Lógica:
    Obtiene todos los estudiantes y los convierte en un JSON.

    Errores:
    -----

    """
    if request.method == 'GET':
        try:
            # Obtenemos todos los estudiantes
            students = Student.objects.all()

            # Creamos una lista para almacenar los estudiantes
            students_list = []
            for student in students:
                students_list.append({
                    "id": student.id,
                    "rut": student.rut,
                    "name": student.name
                })

            # retornamos la lista de estudiantes como un JSON
            return JsonResponse({"students": students_list}, status=200)

        except Exception as e:
            return JsonResponse({"status": "Error", "message": f"[!] ERROR {str(e)}"}, status=400)
        
@csrf_exempt
def GetTests(request):
    """
    Descripción:
    Vista que obtiene todos los tests.

    Parámetros:
    - request: El objeto HttpRequest enviado por el cliente.

    Returns:
    JsonResponse con la lista de tests.

    Lógica:
    Obtiene todos los tests y los convierte en un JSON.

    Errores:
    -----
    """
    if request.method == 'GET':
        try:
            # Obtenemos todos los tests
            tests = Test.objects.all()

            # Creamos una lista para almacenar los tests
            tests_list = []
            for test in tests:
                tests_list.append({
                    "id": test.id,
                    "name": test.name
                })

            # retornamos la lista de tests como un JSON
            return JsonResponse({"tests": tests_list}, status=200)

        except Exception as e:
            return JsonResponse({"status": "Error", "message": f"[!] ERROR {str(e)}"}, status=400)

@csrf_exempt
def AddStudents(request):
    """
    Descripción:
    Vista que crea estudiantes.

    Parámetros:
    - request: El objeto HttpRequest enviado por el cliente.

    Returns:
    JsonResponse con los estudiantes creados.

    Lógica:
    Crea estudiantes a partir de un JSON.

    Errores:
    -----
    """
    if request.method == 'POST':
        try:
            # Parseamos el JSON recibido
            data = json.loads(request.body)

            # Verificamos los datos contengan la lista de estudiantes
            if data is None or "students" not in data:
                return JsonResponse({"message": "Formato incorrecto: faltan estudiantes par agregar"}, status=400)

            # Lista para almacenar los IDs de los estudiantes que se crearon correctamente
            success_ids = []
            error_ids = []

            for student_data in data:
                try:
                    # Creamos el estudiante
                    student = Student.objects.create(
                        id=student_data['id'],
                        rut=student_data['rut'],
                        name=student_data['name']
                    )
                    success_ids.append(student.id)  # Si es exitoso, lo añadimos a la lista de éxito

                except Exception as e:
                    error_ids.append(student_data['rut'])  # Si hay un error, lo añadimos a la lista de error
                    continue

            # Verificamos si todos los estudiantes fueron creados
            if len(success_ids) == len(data):
                return JsonResponse({
                    "status": "OK",
                    "success": success_ids,
                    "error": error_ids
                }, status=201)
            else:
                return JsonResponse({
                    "status": "Error",
                    "message": "[!] Algunos estudiantes no pudieron ser creados.",
                    "success": success_ids,
                    "error": error_ids
                }, status=400)

        except Exception as e:
            return JsonResponse({"status": "Error", "message": f"[!] ERROR {str(e)}"}, status=400)


@csrf_exempt
def CreateTest(request):
    """
    Descripción:
    Vista que crea un test.

    Parámetros:
    - request: El objeto HttpRequest enviado por el cliente.

    Returns:
    JsonResponse con el test creado.

    Lógica:
    Crea un test a partir de un JSON.

    Errores:
    -----
    """
    if request.method == 'POST':
        try:
            # Parseamos el JSON recibido
            data = json.loads(request.body)

            # Verificamos que la información necesaria esté presente
            if "id" not in data or "name" not in data or "questions" not in data:
                return JsonResponse({"message": "Formato incorrecto: faltan datos para crear la prueba"}, status=400)
            
            # Verificamos que el test no exista
            if Test.objects.filter(id=data['id']).exists():
                return JsonResponse({"status": "Error", "message": "[!] Test con ese id ya existe"}, status=400)

            # Creamos el objeto Test
            test = Test.objects.create(id=data['id'], name=data['name'])

            # Iteramos sobre las preguntas
            for question_data in data['questions']:
                question = Question.objects.create(
                    statement=question_data['statement'],
                    explanation=question_data.get('explanation', ''),
                    score=question_data.get('score', 1), #  Si no trae score se asigna 1 por defecto
                    tagType=question_data.get('axisType', 'Numeros')  # Si no trae tagType se asigna 'Numeros' por defecto, probablemente no tiene mucho sentido en la realidad, pero para dejar algo. Se podría crear tambien algo como "no especificado" o "sin tag".
                )

                # si no vienen alternativas, retornamos un error
                if "alternatives" not in question_data:
                    return JsonResponse({"status": "Error", "message": "[!] Las preguntas no son de alternativas o las alternativas no fueron proporcionadas"}, status=400)

                # solo pueden tener 5 alternativas por pregunta
                if len(question_data['alternatives']) > 5:
                    return JsonResponse({"status": "Error", "message": "[!] Solo se permiten 5 alternativas por pregunta"}, status=400)

                # Iteramos sobre las alternativas de cada pregunta (Asumimos que vendran las alternativas en formato correcto en el JSON y una será correcta)
                for alternative_data in question_data['alternatives']:
                    alternative = Alternative.objects.create(
                        content=alternative_data['content'],
                        correct=alternative_data['correct'] == 'true'
                    )
                    question.alternatives.add(alternative)  # Relacionamos la alternativa con la pregunta

                # Relacionamos la pregunta con el test
                test.questions.add(question)

            # Devolvemos una respuesta exitosa con el ID del test creado
            return JsonResponse({"status": "OK", "id": test.id, "message":"" }, status=201)

        except Exception as e:
            return JsonResponse({"status": "Error" ,"message" : f"[!] ERROR {str(e)}" }, status=400)

    return JsonResponse({"message": "Método no permitido"}, status=405)

@csrf_exempt
def AddTestToStudent(request, test_id):
    """
    Descripción:
    Vista que asigna un test a un estudiante.

    Parámetros:
    - request: El objeto HttpRequest enviado por el cliente.
    - test_id: El ID del test a asignar.

    Returns:
    JsonResponse con los estudiantes asignados al test.

    Lógica:
    Asigna un test a un estudiante a partir de un JSON.

    Errores:
    -----
    """
    if request.method == 'POST':
        try:
            # Parseamos el JSON recibido
            data = json.loads(request.body)

            # Verificamos que la lista de estudiantes y el test_id estén presentes
            if "students" not in data or not test_id:
                return JsonResponse({"status": "Error", "message": "[!] Estudiantes o Test no proporcionados"}, status=400)

            # Lista para almacenar los IDs de los estudiantes que se asignaron correctamente y erroneamente
            success_ids = []
            error_ids = []

            for id_student in data['students']:
                try:
                    # Buscamos el estudiante
                    student = Student.objects.get(id=id_student)

                    # Buscamos el test
                    test = Test.objects.filter(id=test_id).first()

                    # Verificamos que el test exista
                    if test is None:
                        return JsonResponse({"status": "Error", "message": "[!] Test no existe"}, status=404)

                    # Relacionamos el test con el estudiante
                    # Si esta relación ya existe, Django se encarga de no duplicarla, por ser ManyToManyField. 
                    student.tests.add(test)
                    success_ids.append(id_student)  # Si es exitoso, lo añadimos a la lista de éxito

                # Esto para que verifique todos los estudiantes antes de devolver una respuesta de error.
                except Student.DoesNotExist:
                    error_ids.append(id_student)
                    continue  # Si el estudiante no existe, simplemente lo ignoramos
                except Exception as e:
                    error_ids.append(id_student) 
                    continue # Si hay un error al agregar el test, también lo ignoramos

            # Verificamos si todos los estudiantes fueron procesados
            if len(success_ids) == len(data['students']):
                return JsonResponse({
                    "status": "OK",
                    "success":success_ids ,
                    "error": error_ids
                }, status=201)
            else:
                return JsonResponse({
                    "status": "Error",
                    "message": "[!] Estudiante no existe.",
                    "success": success_ids,
                    "error": error_ids
                }, status=400)

        except Exception as e:
            return JsonResponse({"status": "Error", "message": f"[!] ERROR {str(e)}"}, status=400)

    return JsonResponse({"message": "Método no permitido"}, status=405)


@csrf_exempt
def SendOrGetAnswers(request, test_id):
    """
    Descripción:
    Vista que envía o recibe las respuestas de un test.

    Parámetros:
    - request: El objeto HttpRequest enviado por el cliente.
    - test_id: El ID del test a asignar.

    Returns:
    JsonResponse con las respuestas de los estudiantes.

    Lógica:
    Envía o recibe las respuestas de un test a partir de un JSON.

    Errores:
    -----
    """
    # en esta vista en particular, si es un post, significa que estamos recibiendo las respuestas de los estudiantes
    # si es un get, significa que se nos solicita los puntajes de los estudiantes para una prueba en particular.
    if request.method == 'POST':
        try:
            # Parseamos el JSON recibido
            data = json.loads(request.body)

            # Verificamos que la lista de estudiantes y el test_id estén presentes
            if "students" not in data or not test_id:
                return JsonResponse({"status": "Error", "message": "[!] Estudiantes o Test no proporcionados"}, status=400)
            
            # Lista para almacenar los IDs de los estudiantes que se asignaron correctamente y erroneamente
            success_ids = []
            error_ids = []

            for student_data in data['students']:
                id_student = student_data["id"]  # Obtiene el ID del estudiante
                try:
                    # Buscamos el estudiante
                    student = Student.objects.get(id=id_student)

                    # Buscamos el test
                    test = Test.objects.filter(id=test_id).first()
                    test_questions = test.questions.all().count()

                    # Verificamos que el test exista
                    if test is None:
                        return JsonResponse({"status": "Error", "message": "[!] Test no existe"}, status=404)

                    # Verificamos que el estudiante haya sido asignado al test
                    if not student.tests.filter(id=test.id).exists():
                        return JsonResponse({"status": "Error", "message": "[!] Estudiante no asignado al test"}, status=404)

                    # Obtenemos las respuestas del estudiante
                    questions = student_data["questions"]  # Accede a las preguntas del estudiante

                    # Calculamos la nota del estudiante
                    correct = 0
                    wrong = 0
                    skipped = 0

                    for question_data in questions:
                        question_id = question_data["id"]  # Obtiene el ID de la pregunta
                        answer = question_data["answer"]    # Obtiene la respuesta dada por el estudiante

                        # Verificamos que la pregunta exista
                        question = test.questions.filter(id=question_id).first()
                        if question and question.alternatives.filter(id=answer).exists():
                            if question.alternatives.get(id=answer).correct:
                                correct += question.score  # Sumar puntaje si la respuesta es correcta
                            elif question.alternatives.get(id=answer).correct == False:
                                wrong += 1 # Sumar a las incorrectas si la respuesta es incorrecta
                    skipped = test_questions - (correct + wrong)  # Calculamos las preguntas no respondidas
                    score = correct  # Calculamos el puntaje del estudiante, estamos asumiendo que el puntaje es igual a las respuestas correctas


                    # Asignamos la nota al estudiante, asumimos que el score será igual que las respuestas correctas. (Se podría crear una escala aparte para el score)
                    StudentTestScore.objects.create(student=student, test=test, score=score, correct=correct, wrong=wrong, skipped=skipped)
                    success_ids.append(id_student)
                    
                except Student.DoesNotExist:
                    error_ids.append(id_student)  # Agregar ID del estudiante a error_ids
                    continue
                except Exception as e:
                    error_ids.append(id_student)  # Agregar ID del estudiante a error_ids
                    continue

            # Verificamos si todos los estudiantes fueron procesados
            if len(success_ids) == len(data['students']):
                return JsonResponse({
                    "status": "OK",
                    "success": success_ids,
                    "error": error_ids
                }, status=201)
            else:
                return JsonResponse({
                    "status": "Error",
                    "message": "[!] Estudiante no existe.",
                    "success": success_ids,
                    "error": error_ids
                }, status=400)
            
        except Exception as e:
            return JsonResponse({"status": "Error", "message": f"[!] ERROR {str(e)}"}, status=400)

    if request.method == 'GET':
        try:
            # Verificamos que el test_id esté presente
            if not test_id:
                return JsonResponse({"status": "Error", "message": "[!] Test no proporcionado"}, status=400)

            # Buscamos el test
            test = Test.objects.filter(id=test_id).first()

            # Verificamos que el test exista
            if test is None:
                return JsonResponse({"status": "Error", "message": "[!] Test no existe"}, status=404)

            # Obtenemos los puntajes de los estudiantes
            scores = StudentTestScore.objects.filter(test=test)

            print(len(scores))

            # Creamos un diccionario para almacenar los puntajes
            scores_dict = {}
            scores_dict["id"] = scores[0].test.id  # Usamos el primer score para obtener la info del test
            scores_dict["name"] = scores[0].test.name
            scores_dict["students"] = []  # Lista para almacenar múltiples estudiantes

            for score in scores:
                student_dict = {
                    "id": score.student.id,
                    "name": score.student.name,
                    "score": score.score,
                    "stats": {
                        "correct": score.correct,
                        "wrong": score.wrong,
                        "skipped": score.skipped
                    }
                }
                scores_dict["students"].append(student_dict)  # Añadir cada estudiante al diccionario

            return JsonResponse({"status": "OK", "scores": scores_dict}, status=200)
        
        except Exception as e:
            return JsonResponse({"status": "Error", "message": f"[!] ERROR {str(e)}"}, status=400)
        
    return JsonResponse({"message": "Método no permitido"}, status=405)