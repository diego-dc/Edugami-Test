from django.urls import path
from . import views

# url patterns para la aplicación. 

app_name = "edugami_test"

urlpatterns = [
    path("", views.Index, name="index"),
    path("add_students/", views.AddStudents, name="students"),
    path("get_students/", views.GetStudents, name="get_students"),
    path("get_tests/", views.GetTests, name="get_tests"),
    path('test/', views.CreateTest, name='test'),
    path('test/<int:test_id>/assign', views.AddTestToStudent, name='addTestToStudent'),
    path('test/<int:test_id>/answers', views.SendOrGetAnswers, name='answers'),
]