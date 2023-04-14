from django.contrib import admin
from .models import UserAccount,Teacher,Student,Test

# Register your models here.
admin.site.register(UserAccount)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Test)