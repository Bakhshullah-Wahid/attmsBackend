from django.contrib import admin
from .models import Department, Class, User, Teacher

admin.site.register(Department)
admin.site.register(Class)
admin.site.register(User)
admin.site.register(Teacher)
