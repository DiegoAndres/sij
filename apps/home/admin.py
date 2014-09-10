from django.contrib import admin
from sij.apps.home.models import Usuario, Receptor, Empleado, Evento, Notificacion

admin.site.register(Usuario)
admin.site.register(Receptor)
admin.site.register(Empleado)
admin.site.register(Evento)
admin.site.register(Notificacion)

# Register your models here.
