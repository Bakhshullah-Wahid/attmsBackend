from django.contrib import admin
from .models import  *

admin.site.register(Department)
admin.site.register(Class)
admin.site.register(User)
admin.site.register(Teacher)
admin.site.register(Subject)
admin.site.register(FreeClassSlot)  
admin.site.register(Scheduler)

