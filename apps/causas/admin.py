from django.contrib import admin
from sij.apps.causas.models import Causa, Jurisdiccion ,Tribunal, Diligencia, ResultadoDiligencia, FotoDiligencia

admin.site.register(Causa)
admin.site.register(Tribunal)
admin.site.register(Jurisdiccion)
admin.site.register(Diligencia)
admin.site.register(ResultadoDiligencia)
admin.site.register(FotoDiligencia)
