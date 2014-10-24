from django.db import models
from sij.apps.home.models import Evento
from django.utils import timezone
from datetime import datetime
from django.http import HttpResponseRedirect, HttpResponse

def tiempo_atraso():
	return 7

class Causa(models.Model):
	ncausa 					= models.CharField(max_length=15)
	materia					= models.CharField(max_length=20)
	abogado 				= models.ForeignKey('home.Usuario')
	receptor 				= models.ForeignKey('home.Usuario', related_name='receptor_causa')
	direccion 				= models.CharField(max_length=150)
	comuna 					= models.ForeignKey('causas.Comuna')
	tribunal 				= models.ForeignKey('causas.Tribunal') # esto es nuevo
	tipodiligencia			= models.ForeignKey('causas.Diligencia')
	observacion 			= models.CharField(max_length=200, null=True, blank=True)
	fechaingreso 			= models.DateTimeField(db_column='fechaIngreso')
	estado 					= models.CharField(max_length=50)
	tiporesultadodiligencia	= models.ForeignKey('causas.Diligencia', related_name='resultado_diligencia')
	diaspendiente			= models.IntegerField(db_column='diasPendiente', null=True)
	atrasada				= models.BooleanField(default=False)
	valor                   = models.IntegerField(null=True)

	def __unicode__(self):
		datos = "numero: %s, estado: %s"%(self.ncausa, self.estado)
		return datos

	def direccioncompleta(self):
		return u"%s, %s"%(self.direccion,self.comuna.nombrecomuna)

	def gethistorial(self):
		historial = Evento.objects.filter(usuario = self.abogado, causa = self)
		return historial

	def diaspendientes(self):
		if self.estado == "pendiente" or self.estado == "confirmacion":
			return None
		else:
			if self.estado == "en ruta":

				e = self.gethistorial().get(tipoevento = 1)
				diff = timezone.now() - e.fechaevento
				return int(diff.days)
			else:
				return None

	#def nuevaCausa():
	# def aceptar_causa(self):
	# 	try:
	# 		self.estado = 'en ruta';
	# 		self.save()
	# 		# Evento.aceptacion(self)
	# 		return 1
	# 	except:
	# 		return 0

	#def diligenciarCausa():


class ResultadoDiligencia(models.Model):
	causa 			= models.OneToOneField(Causa,primary_key=True)
	comentario 		= models.CharField(max_length=500)
	demandado		= models.CharField(max_length=300, blank = True, null = True)
	demandante 		= models.CharField(max_length=300, blank = True, null = True)
	fojas 			= models.CharField(max_length=100, blank = True, null = True)
	derechos 		= models.CharField(max_length=100, blank= True, null = True)
	fechadiligencia	= models.DateTimeField(db_column='fechaDiligencia')
	gpslat 			= models.FloatField(db_column='gpsLat', blank=True, null=True)
	gpslon 			= models.FloatField(db_column='gpsLon', blank=True, null=True)

def url_foto(instance, filename):
	ruta = '/'.join(['causas', str(instance.resultadodiligencia.causa.id), filename])
	return ruta

from PIL import Image
import os

class FotoDiligencia(models.Model):
	resultadodiligencia 	= models.ForeignKey(ResultadoDiligencia)
	foto 					= models.FileField(upload_to=url_foto)

	def __unicode__(self):
		return self.foto.name


	def rotar(self):
		img = Image.open(self.foto)

		# rotated_img = img.rotate(90)

		# os.remove('sij'+self.foto.url)
		# destination = open('sij'+self.foto.url, 'wb+')
		# for chunk in rotated_img.chunks():
		# 	destination.write(chunk)

		# destination.close()

		rotated_img.save('sij/'+self.foto.url, overwrite = True)

		return 1



class Tribunal(models.Model):
	nombretribunal 			= models.CharField(db_column='nombreTribunal', max_length=200)
	direccion 				= models.CharField(max_length=150)
	jurisdiccion 			= models.ForeignKey('causas.Jurisdiccion')
	telefono 				= models.CharField(max_length=15)
	empleados 				= models.ManyToManyField('home.Receptor', related_name='tribunales', through='home.Empleado')


	def __unicode__(self):
		return self.nombretribunal



class Diligencia(models.Model):
	tipodiligencia 			= models.CharField(db_column='tipoDiligencia', max_length=15)
	detallediligencia		= models.CharField(db_column='detalleDiligencia', max_length=150)
	objetivo 				= models.ForeignKey('self', db_column='diligencia_id', blank=True, null=True)


	def __unicode__(self):
		nombreCompleto = "%s: %s"%(self.tipodiligencia,self.detallediligencia)
		return nombreCompleto

	# def getCausas(fechaInicio, fechaFin)
	# def getCausasDiligencia()

class Jurisdiccion(models.Model):
	nombrejurisdiccion 	= models.CharField(db_column='nombreJurisdiccion', max_length=80)

	def __unicode__(self):
		return self.nombrejurisdiccion

	# def getCausas(fechaInicio, fechaFin):
	# def getCausasRegion():
	# def getTribunales():
	# def getReceptores():

class Region(models.Model):
	nombreregion 		= models.CharField(db_column='nombreRegion', max_length=80)

	def __unicode__(self):
		return self.nombreregion

class Provincia(models.Model):
	nombreprovincia		= models.CharField(db_column='nombreProvincia', max_length=80)
	region 				= models.ForeignKey('causas.Region')

	def __unicode__(self):
		return self.nombreprovincia

class Comuna(models.Model):
	nombrecomuna 		= models.CharField(db_column='nombreComuna', max_length=50)
	provincia 			= models.ForeignKey('causas.Provincia')

	def __unicode__(self):
		return self.nombrecomuna
