from django.contrib import admin
from .models import ToDoList

class ToDoAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)


admin.site.register(ToDoList, ToDoAdmin)
