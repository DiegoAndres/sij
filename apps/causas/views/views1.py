# -*- coding: utf-8 -*-
from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from django.utils import timezone
from datetime import datetime
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from sij.apps.causas.forms import pagoDiligenciaForm, filtroEstadoForm, filtroSortPagForm, diligenciarCausaForm, fotoDiligenciarCausaForm
from sij.apps.causas.models import Causa, Region, Provincia, Comuna, Tribunal, Diligencia, ResultadoDiligencia, FotoDiligencia
from sij.apps.home.models import Receptor, Usuario, Empleado, Evento, Notificacion
from django.core.mail import EmailMessage

import os
import string
import random

from PIL import Image as PilImage

#tiempo en segundos dentro del que se permite editar o arrepentirse de una aceptación o diligencia de causa
def tiempo_undo():
	# return 7200
	return 720000

def max_fotos():
	return 15

def tabla_causas_view(request):
	if request.user.usuario.tipo == 0:
		filter_args = {'abogado': request.user.usuario}
	else:
		if request.user.usuario.tipo == 1:
			filter_args = {'receptor': request.user.usuario}
		else:
			if request.user.usuario.tipo == 2:
				filter_args = {}

	causas = Causa.objects.filter(**filter_args)

	for c in causas:	# la primera vez se calculan los dias pendientes para cada causa y se actualizan
		c.diaspendiente = c.diaspendientes()
		c.save()

	if request.GET:
		sort = request.GET['sort']
	else:
		sort = '-diaspendiente'

	causas = causas.order_by(sort)

	paginator = Paginator(causas,6)
	page = request.GET.get('page')
	try:
		causasp = paginator.page(page)
	except PageNotAnInteger: # If page is not an integer, deliver first page.
		causasp = paginator.page(1)
	except EmptyPage:
		causasp = paginator.page(paginator.num_pages)

	form = filtroSortPagForm(initial={'sort': sort})
	ctx = {'causas': causasp, 'form': form}
	return render_to_response('tables/table_causas.html',ctx, context_instance=RequestContext(request))


def panel_causas_view(request):
	date = 0
	if request.user.usuario.tipo == 0:
		filter_args = {'abogado': request.user.usuario}
	else:
		if request.user.usuario.tipo == 1:
			filter_args = {'receptor': request.user.usuario}
		else:
			if request.user.usuario.tipo == 2:
				filter_args = {}

	estados_excluidos = ['rechazada','diligenciada', 'eliminada']
	if request.GET:
		form = filtroEstadoForm(request.GET)
		estado = form.data['estado']
		sort = form.data['sort']
		searchtype = form.data['searchtype']
		search = form.data['search']

		if search != '':
			if searchtype == 'ncausa':
				filter_args['ncausa__contains'] = search
			else:
			 	try:
			 		startdate = form.data['startdate']
			 		enddate = form.data['enddate']
			 		filter_args['fechaingreso__range'] = [startdate,enddate]
			 	except:
			 		ctx = {'error': 'La fecha no cumple con el formato. ', 'form': form}
			 		return render_to_response('tables/panel_causas.html',ctx, context_instance=RequestContext(request))

		if estado != '':
			if estado != 'incompleta':
				filter_args['estado'] = estado
				if estado == 'diligenciada':
					estados_excluidos.remove('diligenciada')

		else:
			estados_excluidos.remove('diligenciada')

		causas = Causa.objects.order_by(sort).filter(**filter_args).exclude(estado__in=estados_excluidos)

		paginator = Paginator(causas,6)

		page = request.GET.get('page')
		try:
			causasp = paginator.page(page)
		except PageNotAnInteger: # If page is not an integer, deliver first page.
			causasp = paginator.page(1)
		except EmptyPage:
			causasp = paginator.page(paginator.num_pages)

		ctx = {'causas': causasp, 'form': form, 'date': date}
		return render_to_response('tables/panel_causas.html',ctx, context_instance=RequestContext(request))

	else:	# esto se muestra por primera vez. se muestran todas las causas y van ordenadas por dias pendiente.
		causas = Causa.objects.filter(**filter_args).exclude(estado__in=estados_excluidos)
		for c in causas:	# la primera vez se calculan los dias pendientes para cada causa y se actualizan
			c.diaspendiente = c.diaspendientes()
			c.save()

		causas = causas.order_by('-diaspendiente')

		paginator = Paginator(causas,6)
		page = request.GET.get('page')
		try:
			causasp = paginator.page(page)
		except PageNotAnInteger: # If page is not an integer, deliver first page.
			causasp = paginator.page(1)
		except EmptyPage:
			causasp = paginator.page(paginator.num_pages)

		form = filtroEstadoForm(initial={'estado': 'incompleta', 'sort': '-diaspendiente', 'searchtype': 'ncausa'})
		ctx = {'causas': causasp, 'form': form}
		return render_to_response('tables/panel_causas.html',ctx, context_instance=RequestContext(request))

def receptor_view(request):
	if request.user.is_authenticated() and request.user.usuario.tipo == 1:
		return render_to_response('causas/receptor.html', context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/')

def detalle_causa_view(request, idcausa):
	if request.user.is_authenticated():
		form = pagoDiligenciaForm()
		try:
			causa = Causa.objects.get(id = idcausa)
			causa.diaspendiente = causa.diaspendientes()
			causa.save()
			ctx = {'causa': causa, 'form':form}
			return render_to_response('causas/detalle.html',ctx, context_instance=RequestContext(request))
		except:
			ctx = {'error': 'No existe la causa.'}
			return render_to_response('causas/detalle.html',ctx, context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/')

def detalle_diligencia_causa_view(request, idcausa):
	if request.user.is_authenticated():
		try:
			causa = Causa.objects.get(id = idcausa)
			resultado = ResultadoDiligencia.objects.get(causa = causa)
			fotos = FotoDiligencia.objects.filter(resultadodiligencia = resultado)
			ctx = {'causa': causa, 'resultado': resultado, 'fotos': fotos}
			return render_to_response('causas/detalle_diligencia.html', ctx, context_instance=RequestContext(request))
		except:
			ctx = {'error': 'No existe la causa o aún no se ha diligenciado.'}
			return render_to_response('causas/detalle_diligencia.html', ctx, context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/')

def opciones_receptor_causa_view(request,idcausa):
	if request.user.is_authenticated() and request.user.usuario.tipo == 1:
		aceptar = 0
		rechazar = 0
		diligenciar = 0
		undo_aceptar = 0

		try:
			causa = Causa.objects.get(id = idcausa)
			causa.diaspendiente = causa.diaspendientes()
			causa.save()

			try: #ya fue diligenciada
				evento2 = Evento.objects.get(causa = causa, tipoevento = 2)
				ctx = {'causa': causa, 'aceptar': aceptar, 'rechazar': rechazar, 'diligenciar': diligenciar, 'undo_aceptar': undo_aceptar}
				return render_to_response('causas/opciones_causa.html',ctx, context_instance=RequestContext(request))
			except: #si ya se aceptó por un receptor
				try:
					evento1 = Evento.objects.get(causa = causa, tipoevento = 1)
					# evento1 = historial.order_by('fechaevento').filter(tipoevento = 1)[0]
					diligenciar = 1
					diff = evento1.fechaevento  - timezone.now()
					diff = diff.seconds
					if diff < tiempo_undo():
					 	undo_aceptar = 1
					ctx = {'causa': causa, 'aceptar': aceptar,'rechazar': rechazar, 'diligenciar': diligenciar, 'undo_aceptar': undo_aceptar}
					return render_to_response('causas/opciones_causa.html',ctx, context_instance=RequestContext(request))
				except:
					try:
						evento3 = Evento.objects.get(causa = causa, tipoevento = 7)
						rechazar = 1
						ctx = {'causa': causa, 'aceptar': aceptar,'rechazar': rechazar, 'diligenciar': diligenciar, 'undo_aceptar': undo_aceptar}
						return render_to_response('causas/opciones_causa.html',ctx, context_instance=RequestContext(request))
					except:
						aceptar = 1
						rechazar = 1
						ctx = {'causa': causa, 'aceptar': aceptar,'rechazar': rechazar, 'diligenciar': diligenciar, 'undo_aceptar': undo_aceptar}
						return render_to_response('causas/opciones_causa.html',ctx, context_instance=RequestContext(request))
		except:
			ctx = {'error': 'No existe la causa.', 'causa': causa.ncausa}
			return render_to_response('causas/opciones_causa.html',ctx, context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/')

def aceptar_causa_view(request):
	if request.user.is_authenticated() and request.POST:
		form = pagoDiligenciaForm(request.POST)
		if request.user.usuario.tipo == 1:
			try:
				try:
					causa = Causa.objects.get(id = form.data['idcausa'])
					causa.estado = 'confirmacion'
					causa.valor = form.data['valor']
				except:
					return HttpResponse('error datos causa')

				try:
					usuario = Usuario.objects.get(user=request.user)
					usuario.rut = form.data['rut']
					usuario.banco = form.data['banco']
					usuario.tipo_cuenta = form.data['tipo_cuenta']
					usuario.cuenta = form.data['cuenta']
				except:
					return HttpResponse('error datos usuario')

				try:
					e = Evento()
					e.usuario = request.user.usuario
					e.fechaevento = timezone.now()
					e.tipoevento = 7
					e.causa = causa
				except:
					return HttpResponse('error datos evento')

				try:
					n = Notificacion()
					n.usuario 	= causa.abogado
					n.fechanotificacion 	= timezone.now()
					n.causa 				= causa
					n.detallenotificacion	= 'El receptor '+str(request.user.usuario.nombre)+' ha solicitado la confirmación de la solicitud de causa '+str(causa.ncausa)+'.'
					n.nueva = True
				except:
					return HttpResponse('error datos notificacion')

				try:
					causa.save()
					# pass
				except:
					return HttpResponse('error causa')

				try:
					usuario.save()
					# pass
				except:
					return HttpResponse('error usuario')

				try:
					e.save()
					# pass
				except:
					return HttpResponse('error evento')

				try:
					n.save()
					# pass
				except:
					return HttpResponse('error notificacion')

				title = "Notificación: Causa " + str(causa.ncausa)
				body = 'El receptor '+str(request.user.usuario.nombre)+' ha solicitado la confirmación de la solicitud de causa '+str(causa.ncausa)+'. Para mayor informacion de la causa, debe ingresar al plataforma www.sij.cl/login'
				email = EmailMessage(title, body, 'no-reply@sij.cl', [causa.abogado.user.email])					
				email.send()

				return HttpResponse('La solicitud ha sido confirmada.')
			except:
				return HttpResponseRedirect('/')

		if request.user.usuario.tipo == 0:
			try:
				try:
					causa = Causa.objects.get(id = form.data['idcausa'])
					causa.estado = 'en ruta'
				except:
					return HttpResponse('error datos causa')

				try:
					pendientes = causa.receptor.receptor.causaspendientes
					pendientes = pendientes+1
					receptor = causa.receptor.receptor
					receptor.causaspendientes = pendientes
				except:
					return HttpResponse('error Datos receptor')

				try:
					e = Evento()
					e.usuario = request.user.usuario
					e.fechaevento = timezone.now()
					e.tipoevento = 1
					e.causa = causa
				except:
					return HttpResponse('error datos eventos')

				try:
					n = Notificacion()
					n.usuario 	= causa.abogado
					n.fechanotificacion 	= timezone.now()
					n.causa 				= causa
					n.detallenotificacion	= 'El abogado '+str(request.user.usuario.nombre)+' ha confirmado el valor de la diligencia de la solicitud de causa '+str(causa.ncausa)+'.'
					n.nueva = True
				except:
					return HttpResponse('error datos notificacion')

				try:
					causa.save()
				except:
					return HttpResponse('error causa')

				try:
					receptor.save()
				except:
					return HttpResponse('error receptor')

				try:
					e.save()
				except:
					return HttpResponse('error evento')

				try:
					n.save()
				except:
					return HttpResponse('error notificacion')

				title = 'Notificacion: Causa '+str(causa.ncausa)
				body = 'El abogado '+str(request.user.usuario.nombre)+' ha confirmado el valor de la diligencia de la solicitud de causa '+str(causa.ncausa)+'. Para mayor informacion de la causa, debe ingresar al plataforma www.sij.cl/login'
				email = EmailMessage(title, body, 'no-reply@sij.cl', [causa.receptor.user.email])
				email.send()

				return HttpResponse('La solicitud ha sido aceptada.')

			except:
				return HttpResponseRedirect('/')
	else:
		return HttpResponseRedirect('/')

def deshacer_aceptar_causa_view(request,idcausa):
	if request.user.is_authenticated() and request.user.usuario.tipo == 1:
		try:
			causa = Causa.objects.get(id = idcausa)
			causa.estado = 'pendiente'

			pendientes = causa.receptor.receptor.causaspendientes
			pendientes = pendientes-1
			receptor = causa.receptor.receptor
			receptor.causaspendientes = pendientes

			e = Evento.objects.get(causa = causa, tipoevento = 1)

			n = Notificacion()
			n.usuario 	= causa.abogado
			n.fechanotificacion 	= timezone.now()
			n.causa 				= causa
			n.detallenotificacion	= 'El receptor '+request.user.usuario.nombre+' se ha retractado de aceptar la solicitud de causa '+causa.ncausa+'.'

			causa.save()
			receptor.save()
			e.delete()
			n.save()
			return HttpResponse('La aceptación ha sido deshecha.')
		except:
			return HttpResponse('0')
	else:
		return HttpResponseRedirect('/')

def rechazar_causa_view(request,idcausa):
	if request.user.is_authenticated() and request.user.usuario.tipo == 1:
		try:
			causa = Causa.objects.get(id = idcausa)
			causa.estado = 'rechazada'

			e = Evento()
			e.usuario = request.user.usuario
			e.fechaevento = timezone.now()
			e.tipoevento = 4
			e.causa = causa

			n = Notificacion()
			n.usuario 	= causa.abogado
			n.fechanotificacion 	= timezone.now()
			n.causa 				= causa
			n.detallenotificacion	= 'El receptor '+request.user.usuario.nombre+' ha rechazado la solicitud de causa '+causa.ncausa+'.'

			causa.save()
			e.save()
			n.save()

			return HttpResponse('La causa ha sido rechazada.')
		except:
			return HttpResponse('0')
	else:
		return HttpResponseRedirect('/')

def eliminar_causa_view(request, idcausa):
	if request.user.is_authenticated() and request.user.usuario.tipo == 0:
		try:
			causa = Causa.objects.get(id = idcausa)
			causa.estado = 'eliminada'

			e = Evento()
			e.usuario = request.user.usuario
			e.fechaevento = timezone.now()
			e.tipoevento = 5
			e.causa = causa

			n = Notificacion()
			n.usuario = causa.receptor
			n.fechanotificacion = timezone.now()
			n.causa = causa
			n.detallenotificacion = 'El abogado '+str(request.user.usuario.nombre)+' ha eliminado la solicitud de causa '+str(causa.ncausa)+'.'

			causa.save()
			e.save()
			n.save()

			title = 'Notificacion: Causa '+str(causa.ncausa)
			body = 'El abogado '+str(request.user.usuario.nombre)+' ha eliminado la solicitud de causa '+str(causa.ncausa)+'.'
			email = EmailMessage(title, body, 'no-reply@sij.cl', [causa.receptor.user.email])
			email.send()

			return HttpResponse('La causa ha sido eliminada.')
		except:
			return HttpResponse('0')
	else:
		return HttpResponseRedirect('/')

def diligenciar_causa_view(request,idcausa):
	if request.user.is_authenticated() and request.user.usuario.tipo == 1:
		causa = Causa.objects.get(id = idcausa)
		form = diligenciarCausaForm(initial={'lat': 0.0, 'lon': 0.0, 'objetivodiligencia': causa.tipodiligencia.id})
		ctx = {'form': form}
		return render_to_response('causas/diligenciar.html',ctx, context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/')

def opciones_diligenciar_causa_view(request, idcausa):
	ctx = {'idcausa': idcausa}
	return render_to_response('causas/opciones_diligenciar.html',ctx, context_instance=RequestContext(request))

def registrar_diligenciar_causa_view(request, idcausa):
	if request.user.is_authenticated() and request.user.usuario.tipo == 1:
		if request.POST and request.is_ajax():
			form = diligenciarCausaForm(request.POST)
			if form.is_valid():
				causa = Causa.objects.get(id = idcausa)

				causa.estado = 'diligenciada'
				objetivo = Diligencia.objects.get(id=form.data['objetivodiligencia'])
				resultado = Diligencia.objects.get(id=form.data['resultadodiligencia'])

				if causa.tipodiligencia != objetivo:
					nn = Notificacion()
					nn.usuario = causa.abogado
					nn.fechanotificacion = timezone.now()
					nn.causa = causa
					nn.detallenotificacion = 'El receptor '+request.user.usuario.nombre+' ha cambiado el objetivo de la diligencia correspondiente a la causa '+causa.ncausa+'.'
					nn.save()

				causa.tipodiligencia = objetivo
				causa.tiporesultadodiligencia = resultado

				e = Evento()
				e.usuario = request.user.usuario
				e.fechaevento = timezone.now()
				e.tipoevento = 2
				e.causa = causa

				n = Notificacion()
				n.usuario = causa.abogado
				n.fechanotificacion = timezone.now()
				n.causa = causa
				n.detallenotificacion = 'El receptor '+request.user.usuario.nombre+' ha diligenciado la causa '+str(causa.ncausa)+'.'

				resultado = ResultadoDiligencia()
				resultado.causa = causa
				if resultado.comentario:
					resultado.comentario = form.data['comentario']
				resultado.fechadiligencia = timezone.now()

				resultado.demandado = form.data['demandado']
				resultado.demandante = form.data['demandante']
				resultado.fojas = form.data['fojas']

				resultado.derechos = form.data['derechos']

				try:
					lat = form.data['lat']
					lon = form.data['lon']
					resultado.gpslat = lat
					resultado.gpslon = lon
				except:
					resultado.gpslat = 0.0
					resultado.gpslon = 0.0

				causa.save()
				resultado.save()
				e.save()
				n.save()

				title = 'Notificacion: Causa '+str(causa.ncausa)
				body = 'El receptor '+str(request.user.usuario.nombre)+' ha diligenciado la causa '+str(causa.ncausa)+'.'
				email = EmailMessage(title, body, 'no-reply@sij.cl', [causa.abogado.user.email])
				email.send()

				return HttpResponse('0')
			else:
				return HttpResponse('Debe completar todos los campos requeridos.')
		else:
			return HttpResponse('fail. request no es post Y ajax.')
	else:
		return HttpResponseRedirect('/')

def foto_diligenciar_causa_view(request, idcausa):
	if request.user.is_authenticated() and request.user.usuario.tipo == 1:
		causa = Causa.objects.get(id = idcausa)
		form = fotoDiligenciarCausaForm()
		try:
			resultado = ResultadoDiligencia.objects.get(causa = causa)
			fotos = FotoDiligencia.objects.filter(resultadodiligencia = resultado)
			ctx = {'form': form, 'idcausa': causa.id, 'fotos': fotos}
		except:
			ctx = {'form': form, 'idcausa': causa.id}
		return render_to_response('causas/subirfoto.html',ctx, context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/')

def opciones_foto_diligenciar_causa_view(request, idcausa):
	ctx = {'idcausa': idcausa}
	return render_to_response('causas/opciones_foto_causa.html',ctx, context_instance=RequestContext(request))


def registrar_foto_diligenciar_causa_view(request, idcausa):
	if request.POST and request.is_ajax():
		form = fotoDiligenciarCausaForm(request.POST, request.FILES)
		causa = Causa.objects.get(id = idcausa)
		resultado = ResultadoDiligencia.objects.get(causa = causa)

		n_fotos = FotoDiligencia.objects.filter(resultadodiligencia = resultado).count()
		if n_fotos < max_fotos():
			nueva_foto = FotoDiligencia()
			nueva_foto.resultadodiligencia = resultado

			foto = request.FILES['foto']

			rndm = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20))
			ext = foto.name.split('.')[-1]
			nombre = "%s.%s" % (rndm, ext)
			content_type = foto.content_type
			if content_type in settings.CONTENT_TYPES:
				if foto._size < settings.MAX_UPLOAD_SIZE:
					folder = settings.MEDIA_ROOT+'/causas/'+idcausa+'/'
					if not os.path.exists(folder):
						os.mkdir(folder)
						# os.chmod(folder, 0777)
					savepath = os.path.join(settings.MEDIA_ROOT, 'causas', idcausa, nombre)
					destination = open(savepath, 'wb+')
					for chunk in foto.chunks():
						destination.write(chunk)

					destination.close()
					nueva_foto.foto = os.path.join(settings.MEDIA_URL, 'causas', idcausa, nombre)
					# nueva_foto.foto = foto
				else:
					return HttpResponse('El archivo supera el máximo permitido (20MB)')
			else:
				return HttpResponse('El formato no es permitido. (jpg, jpeg)')

			nueva_foto.save()
			return HttpResponse('0')
		else:
			return HttpResponse('Ha alcanzado el número máximo de fotos para la causa.')
	else:
		return HttpResponseRedirect('/')


def rotar_imagen_view(request, id_imagen):
	foto_resultado = FotoDiligencia.objects.get(id = id_imagen)

	# img = PilImage.open('/var/zpanel/hostdata/qwerty/public_html/sij_qwerty_cl/sij/sij'+foto_resultado.foto.url)
	img = PilImage.open('sij'+foto_resultado.foto.url)
	rotated_img = img.rotate(-90, expand=False)

	# rotated_img.save('/var/zpanel/hostdata/qwerty/public_html/sij_qwerty_cl/sij/sij'+foto_resultado.foto.url, overwrite=True)
	rotated_img.save('sij'+foto_resultado.foto.url, overwrite=True)
	return HttpResponse(foto_resultado.foto.url)