from django.db import models
from enum import Enum

# Modelos creados para el test.

# Enumeración para los tags
class TagEnum(models.TextChoices):
    NUMEROS = 'Numeros', 'Numeros'
    GEOMETRIA = 'Geometria', 'Geometria'
    ALGEBRA_FUNCIONES = 'Álgebra y Funciones', 'Álgebra y Funciones'
    PROBABILIDAD = 'Probabilidad', 'Probabilidad'

# Modelo para AlternativeSchema
class Alternative(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.TextField()  # El contenido de la alternativa.-
    correct = models.BooleanField()  # Si la alternativa es correcta o no.-

    def __str__(self):
        return self.content

# Modelo para QuestionSchema
class Question(models.Model):
    id = models.AutoField(primary_key=True)
    statement = models.TextField()  # El enunciado de la pregunta.-
    explanation = models.TextField()  # Explicación de la respuesta.-
    alternatives = models.ManyToManyField(Alternative)  # Relación con Alternative.-
    score = models.FloatField()  # Puntuación de la pregunta.-
    tagType = models.CharField(max_length=50, choices=TagEnum.choices)  # Tipo de tag.-

    def __str__(self):
        return self.statement

# Modelo para Test
class Test(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)  # Nombre del test.-
    questions = models.ManyToManyField(Question) # Relación con Question.-

    def __str__(self):
        return self.name

class Student(models.Model):
    id = models.AutoField(primary_key=True)
    rut = models.CharField(max_length=10) # Considerando un rut de 9 digitos sin puntos, pero con guión.-
    name = models.CharField(max_length=50) # Nombre del estudiante.-
    tests = models.ManyToManyField(Test) # Relación con Test.-

    def __str__(self):
        return self.name

class StudentTestScore(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)  # Relación con el estudiante .-
    test = models.ForeignKey(Test, on_delete=models.CASCADE)  # Relación con el test .-
    score = models.FloatField()  # Puntaje obtenido por el estudiante en el test .-
    correct = models.FloatField()  # Preguntas que el estudiante respondió correctamente .-
    wrong = models.FloatField()  # Preguntas que el estudiante respondió incorrectamente .-
    skipped = models.FloatField()  # Preguntas que el estudiante no respondió .-

    class Meta:
        unique_together = ('student', 'test')  # Garantizamos que un estudiante solo tenga un score por test .-

    def __str__(self):
        return f"{self.student} - {self.test} - Score: {self.score}"