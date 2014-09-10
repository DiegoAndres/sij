# -*- coding: utf-8 -*-
import django_tables2 as tables
from sij.apps.causas.models import Causa
from sij.apps.home.models import Receptor

class CausasTable(tables.Table):
    ncausa = tables.Column()
    fechaingreso = tables.DateColumn()
    abogado	= tables.Column()
    receptor = tables.Column()
    direccioncompleta = tables.Column()
    #comuna = tables.Column(verbose_name="comuna")
    tipodiligencia = tables.Column(verbose_name="tipodiligencia")
    estado = tables.Column(verbose_name="estado")
    observacion = tables.Column()	

    class Meta:
        #model = Causa
        #add class="paleblue" to <table> tag
    	attrs = {"class": "table table-striped"}

class asignarReceptorTable(tables.Table):
	# usuario = tables.Column()
	# causaspendientes = tables.Column()
	# causasatrasadas = tables.Column()
	# causasresueltas = tables.Column()
	# tiempopromedio = tables.Column()
	boton = tables.TemplateColumn('<a href="#"><button type="submit" class="btn btn-default">Asignar</button></a>')

	class Meta:
		model = Receptor
        fields = ('usuario','causaspendientes')
        attrs = {"class": "table table-striped"}

class causasReceptorTable(tables.Table):
    diaspendiente = tables.Column(verbose_name='Dias Pendiente')
    fechaingreso = tables.DateColumn(verbose_name='Fecha Solicitud')
    ncausa  = tables.Column(verbose_name='N° Causa')
    tipodiligencia = tables.Column(verbose_name='Tipo Diligencia')
    observaciones  = tables.Column(verbose_name='observaciones')




