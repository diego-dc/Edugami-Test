from django.contrib import admin
from edugami_app.models import *
# Register your models here.

admin.site.register(Student)
admin.site.register(Test)
admin.site.register(Question)
admin.site.register(Alternative)
admin.site.register(StudentTestScore)
