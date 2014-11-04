# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone

class Usuario(models.Model):
	user 				= models.OneToOneField(User)
	rut 				= models.CharField(max_length=15)
	tipo 				= models.IntegerField(max_length=1) #0: abogado, 1: receptor, 2: juez
	telefono 			= models.CharField(max_length=15, null=True)
	direccion 			= models.CharField(max_length=200, null=True)
	comuna 				= models.ForeignKey('causas.Comuna')
	cuenta 				= models.CharField(max_length=20, null=True)
	banco				= models.CharField(max_length=30,null=True)
	tipo_cuenta			= models.CharField(max_length=30,null=True)

	def __unicode__(self):
		nombre = self.user.first_name+' '+self.user.last_name
		return nombre

	@property
	def nombre(self):
		return self.user.first_name+' '+self.user.last_name

	@property
	def notificaciones(self):
		return Notificacion.objects.filter(usuario = self).order_by('fechanotificacion')

	@property
	def notificaciones_nuevas(self):
		return Notificacion.objects.filter(usuario = self, nueva = True).order_by('fechanotificacion')

	@property
	def notificaciones_nuevas_top(self):
		return Notificacion.objects.filter(usuario = self, nueva = True).order_by('fechanotificacion')[:5]


	@property
	def es_juez(self):
		if self.tipo == 2:
			return True
		else:
			return False


	# def nuevoUsuario():
	# defgetCausas(fechaInicio, fechaFin):
	# def getCausasUsuarioComuna(comuna):
	# def getNotificaciones(numero):
	# def getHistorial():


class Receptor(models.Model):
	usuario 			= models.OneToOneField(Usuario)
	causaspendientes 	= models.IntegerField(db_column='causasPendientes', default=0)
	causasatrasadas 	= models.IntegerField(db_column='causasAtrasadas', default=0)
	causasresueltas 	= models.IntegerField(db_column='causasResueltas', default=0)
	causasenruta 		= models.IntegerField(db_column='causasEnRuta', default=0)
	tiempopromedio 		= models.FloatField(db_column='tiempoPromedio', default=0.0)
	diligenciasdiariaspromedio = models.FloatField(db_column='diligenciasDiariasPromedio', default=0.0)


	def __unicode__(self):
		nombre = self.usuario.user.first_name+' '+self.usuario.user.last_name
		return nombre

	@property
	def activo(self):
		activo = self.usuario.user.is_active
		return activo

	def aumentarCausasPendientes(self):
		self.update(causaspendientes = self.causaspendientes+1)
		return self.causaspendientes

	@property
	def numero_tribunales(self):
		return self.tribunales.count()


	# def actualizarCausaPendiente()
	# def actualizarCausaAtrasada()
	# def actualizarCausaResuelta()
	# def actualizarTiempoPromedio()
	# def verDetalleReceptor()


class Empleado(models.Model):
	receptor 			= models.ForeignKey('home.Receptor')
	tribunal			= models.ForeignKey('causas.Tribunal')

	def __unicode__(self):
		tupla = "%s - %s"%(self.receptor.usuario.user.username, self.tribunal.nombretribunal)
		return tupla


class Notificacion(models.Model):
	usuario 			= models.ForeignKey('home.Usuario')
	fechanotificacion 	= models.DateTimeField(db_column='fechaNotificacion')
	causa 				= models.ForeignKey('causas.Causa')
	detallenotificacion	= models.CharField(max_length=200)
	nueva 				= models.BooleanField(default=True)

	# def enviarCorreo():

class Evento(models.Model):
	usuario 			= models.ForeignKey('home.Usuario')
	fechaevento			= models.DateTimeField(db_column='fechaEvento')
	tipoevento			= models.IntegerField(db_column='tipoEvento')
	#0 : ingreso, 7:confirmacion, 1: aceptacion, 2: diligencia, 3: edicion, 4: rechazo, 5: eliminado, 6: reasignación
	causa 				= models.ForeignKey('causas.Causa')

	def __unicode__(self):
		return 'Causa: '+self.causa.ncausa+' Evento: '+str(self.tipoevento)+' ('+self.usuario.user.first_name+' '+self.usuario.user.last_name+')'

	def aceptacion(causa):
		try:
			e = Evento(usuario = causa.receptor,fechaevento = datetime.now() , tipoevento = 1, causa = causa)
			e.save()
			return 1
		except:
			return 0