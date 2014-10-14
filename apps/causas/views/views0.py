# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from sij.apps.causas.forms import nuevaCausaForm, filtroEstadoForm, receptorForm, reasignarForm
from sij.apps.causas.models import Causa, Jurisdiccion, Region, Provincia, Comuna, Tribunal, Diligencia
from sij.apps.home.models import Receptor, Usuario, Empleado, Evento, Notificacion
# from django.utils.simplejson import simplejson
import json
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, InvalidPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.core.mail import EmailMessage


# Vista de la pagina principal de abogados
# INPUT: -
# CONTEXTO: PAGINADOR CAUSAS, FORM, DATE
# OUTPUT: Abogado.html
def abogado_view(request):
	if request.user.is_authenticated() and request.user.usuario.tipo == 0:
		date = 0
		filter_args = {'abogado': request.user.usuario}
		estados_excluidos = ['diligenciada', 'eliminada']
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
				 		return render_to_response('causas/abogado.html',ctx, context_instance=RequestContext(request))

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
			return render_to_response('causas/abogado.html',ctx, context_instance=RequestContext(request))

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
			return render_to_response('causas/abogado.html',ctx, context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/')


# Vista de opciones de las causas del abogado
# INPUT: id de la causa
# CONTEXTO: CAUSA, BOOL EDITAR, BOOL REASIGNAR, BOOL ELIMINAR, BOOL RESULTADOS
# OUTPUT: opciones_causa.html
def opciones_abogado_causa_view(request, idcausa):
	if request.user.is_authenticated():
		editar = 0
		reasignar = 0
		eliminar = 0
		resultados = 0

		try:
			causa = Causa.objects.get(id = idcausa)
			causa.diaspendiente = causa.diaspendientes()
			causa.save()

			try: #ya fue diligenciada
				evento2 = Evento.objects.get(causa = causa, tipoevento = 2)
				resultados = 1
				ctx = {'causa': causa, 'editar': editar, 'reasignar': reasignar, 'eliminar': eliminar, 'resultados': resultados}
				return render_to_response('causas/opciones_causa.html',ctx, context_instance=RequestContext(request))
			except: #si ya se aceptó por un receptor
				try:
					evento1 = Evento.objects.get(causa = causa, tipoevento = 1)
					# evento1 = historial.order_by('fechaevento').filter(tipoevento = 1)[0]
					editar = 1
					ctx = {'causa': causa, 'editar': editar, 'reasignar': reasignar, 'eliminar': eliminar}
					return render_to_response('causas/opciones_causa.html',ctx, context_instance=RequestContext(request))
				except:
					try:
						evento4 = Evento.objects.get(causa = causa, tipoevento = 4)
						reasignar = 1
						ctx = {'causa': causa, 'editar': editar, 'reasignar': reasignar, 'eliminar': eliminar}
						return render_to_response('causas/opciones_causa.html',ctx, context_instance=RequestContext(request))
					except:
						reasignar = 1
						editar = 1
						eliminar = 1
						ctx = {'causa': causa, 'editar': editar, 'reasignar': reasignar, 'eliminar': eliminar}
						return render_to_response('causas/opciones_causa.html',ctx, context_instance=RequestContext(request))
		except:
			ctx = {'error': 'No existe la causa.', 'causa': idcausa}
			return render_to_response('causas/opciones_causa.html',ctx, context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/')


# Vista para la creacion de una nueva causa. Incluye el ingreso a la BD de la causa
# INPUT: -
# CONTEXTO: FORM
# OUTPUT: nuevaCausa.html
def nueva_causa_view(request):
	mensaje = ""
	if request.user.is_authenticated():
		if request.method == "POST":
			form = nuevaCausaForm(request.POST)
			if form.is_valid():
				#Ingresa datos Causa
				c = Causa()
				c.ncausa = form.cleaned_data['ncausa']
				c.materia = form.cleaned_data['materia']
				c.abogado = request.user.usuario
				c.receptor = Usuario.objects.get(id=form.cleaned_data['receptor'])
				c.direccion = form.cleaned_data['direccion']
				c.comuna = Comuna(id=form.cleaned_data['comuna'])
				c.tribunal = Tribunal.objects.get(id=form.cleaned_data['tribunalOrigen'])
				c.tipodiligencia = Diligencia.objects.get(id=form.cleaned_data['tipoDiligencia'])
				c.observacion = form.cleaned_data['observacion']
				c.fechaingreso = datetime.now()
				c.estado = "pendiente"
				c.tiporesultadodiligencia = Diligencia.objects.get(detallediligencia="sin diligenciar")

				c.save()

				#Ingresa datos Evento
				e = Evento()
				e.usuario = request.user.usuario
				e.fechaevento = datetime.now()
				e.tipoevento = 0
				e.causa = c

				e.save()

				#Ingresa datos Notificacion
				n = Notificacion()
				n.usuario = c.receptor
				n.fechanotificacion = datetime.now()
				n.causa = c
				n.detallenotificacion = "El abogado "+c.abogado.nombre+" le ha asignado diligenciar una nueva causa.(rol "+c.ncausa+")."
				n.save()

				title = 'Notificacion: Causa '+c.ncausa
				body = "El abogado "+c.abogado.nombre+" le ha asignado diligenciar una nueva causa.(rol "+c.ncausa+"). Para mayor informacion de la causa, debe ingresar al plataforma www.sij.cl/login"
				email = EmailMessage(title, body, 'no-reply@sij.cl', [c.receptor.user.email])
				email.send()

				return HttpResponseRedirect('/abogado/')

			else:
				#mensaje = "formulario invalido"
				mensaje = form.errors


		form = nuevaCausaForm()
		ctx = {'form': form, 'msj': mensaje}
		return render_to_response('causas/nuevaCausa.html', ctx, context_instance=RequestContext(request))

	else:
		return HttpResponseRedirect('/')


# Vista para tabla de asignacion del receptor a la hora de crear una causa
# INPUT: id tribunal
# CONTEXTO: receptores_activos
# OUTPUT: table_receptores.html
def asignar_receptor_view(request,tribunal):
	tribunal_actual = Tribunal.objects.get(id = tribunal)
	receptores = tribunal_actual.empleados.all()

	receptores_activos = set()

	for r in receptores:
		if r.usuario.user.is_active == True:
			receptores_activos.add(r)

	ctx = {'receptores':receptores_activos}
	return render_to_response('tables/table_receptores.html',ctx, context_instance=RequestContext(request))


# Vista para la reasignacion de receptores a una causa
# INPUT: id causa
# CONTEXTO: receptores_activos
# OUTPUT: reasignar.html
def reasignar_causa_view(request,idcausa):
	if request.user.is_authenticated() and request.user.usuario.tipo == 0:

		form = reasignarForm()
		ctx ={'form': form, 'causa':idcausa}
		return render_to_response('causas/reasignar.html',ctx, context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/')


# Vista para el registro en BD de la reasignacion de receptores a una causa
# INPUT: id causa
# CONTEXTO: -
# OUTPUT: -
def registro_reasignar_causa_view(request,idcausa):
	if request.user.is_authenticated() and request.user.usuario.tipo == 0:
		if request.POST and request.is_ajax():
			form = reasignarForm(request.POST)
			try:
				#Causa
				c = Causa.objects.get(id=idcausa)
				c.tribunal = Tribunal.objects.get(id = form.data['tribunal'])
				c.receptor = Usuario.objects.get(id = form.data['receptorNuevo'])
				c.diaspendiente = 0
				c.estado = 'pendiente'
				c.save()

				#Evento
				e = Evento()
				e.usuario = request.user.usuario
				e.fechaevento = datetime.now()
				e.tipoevento = 6
				e.causa = c

				#Notificacion
				n = Notificacion()
				n.usuario = c.receptor
				n.fechanotificacion = datetime.now()
				n.causa = c
				n.detallenotificacion = "El abogado "+c.abogado.nombre+" le ha solicitado diligenciar una nueva causa.(rol "+c.ncausa+")."
				n.save()
				return HttpResponse('Sea ha reasignado correctamente el receptor')
			except:
				return HttpResponse('errorBD')
		else:
			return HttpResponse('Fail. Request no es POST ni AJAX')
	else:
		return HttpResponseRedirect('/')



# Vista para el icono de las notificaciones
# INPUT: -
# CONTEXTO: -
# OUTPUT: codigo html de notificaciones
def icono_notificaciones(request):
	n = Notificacion.objects.filter(usuario = request.user.usuario).filter(nueva=True)
	count = n.count()
	if count > 0:
		return HttpResponse('<div class="visible-xs text-center">Notificaciones <span class="badge alert-info">'+str(n.count())+'</span></div><div class="hidden-xs"><span class="glyphicon glyphicon-bell"></span><span class="badge alert-info">'+str(n.count())+'</span></div>')
	else:
		return HttpResponse('<div class="visible-xs text-center">Notificaciones <span class="badge">'+str(n.count())+'</span></div><div class="hidden-xs"><span class="glyphicon glyphicon-bell"></span><span class="badge">'+str(n.count())+'</span></div>')



# Vista de las notificaciones
# INPUT: -
# CONTEXTO: notificaciones
# OUTPUT: notificaciones.html
def notificaciones_view(request):
	if request.user.is_authenticated():
		n = request.user.usuario.notificaciones_nuevas_top
		# n = Notificacion.objects.filter(usuario = request.user.usuario)
		ctx ={'notificacion': n}
		return render_to_response('causas/notificaciones.html', ctx, context_instance = RequestContext(request))
	else:
		return HttpResponseRedirect('/')



# Vista para marcar las notificaciones como leidas
# INPUT: -
# CONTEXTO: -
# OUTPUT: codigo html
def notificaciones_leidas_view(request):
	if request.user.is_authenticated():
		Notificacion.objects.filter(usuario = request.user.usuario).update(nueva=False)
	return HttpResponse('<div class="visible-xs text-center">Notificaciones <span class="badge">0</span></div><div class="hidden-xs"><span class="glyphicon glyphicon-bell"></span><span class="badge">0</span></div>')


# Vista de todas las notificaciones
# INPUT: pagina
# CONTEXTO: notificaciones
# OUTPUT: todasNotificaciones.html
def notificaciones_todas_view(request,pagina):
	if request.user.is_authenticated():
		n = Notificacion.objects.filter(usuario = request.user.usuario)
		paginator = Paginator(n,5)
		try:
			page = int(pagina)
		except:
			page = 1
		try:
			notificaciones = paginator.page(page)
		except (EmptyPage, InvalidPage):
			notificaciones = paginator.page(paginator.num_pages)

		ctx = {'notificaciones': notificaciones}
		return render_to_response('causas/todasNotificaciones.html', ctx, context_instance = RequestContext(request))
	else:
		return HttpResponseRedirect('/')



# Vista de las respuestas de diligencias
# INPUT: diligencia
# CONTEXTO: opciones de diligencia, tipo de la opcion
# OUTPUT: select_options.html
def diligencias(request, diligencia):
	try:
		diligencia_objetivo = Diligencia.objects.get(id = diligencia)
		diligencia_respuesta = Diligencia.objects.filter(objetivo = diligencia_objetivo).values_list('id','detallediligencia')
		ctx = {'opciones': diligencia_respuesta, 'tipo': "respuesta diligencia"}
		return render_to_response('select_options.html',ctx, context_instance=RequestContext(request))
	except:
		return HttpResponse("<option value='0'>Seleccione una respuesta diligencia</option>")



# Vista de las provincias
# INPUT: region
# CONTEXTO: opciones de provincias, tipo de la opcion
# OUTPUT: select_options.html
def provincias(request, region):
	try:
		region_actual = Region.objects.get(id = region)
		provincias = Provincia.objects.all().filter(region=region_actual).values_list('id','nombreprovincia')
		ctx = {'opciones': provincias, 'tipo': "provincia"}
		return render_to_response('select_options.html',ctx, context_instance=RequestContext(request))
	except:
		return HttpResponse("<option value='0'>Seleccione una provincia</option>")



# Vista de las comunas
# INPUT: provincia
# CONTEXTO: opciones de comunas, tipo de la opcion
# OUTPUT: select_options.html
def comunas(request,provincia):
	try:
		provincia_actual = Provincia.objects.get(id= provincia)
		comunas = Comuna.objects.all().filter(provincia = provincia_actual).values_list('id','nombrecomuna')
		ctx = {'opciones': comunas,'tipo': "comuna"}
		return render_to_response('select_options.html', ctx, context_instance=RequestContext(request))
	except:
		return HttpResponse("<option value='0'>Seleccione una comuna</option>")



# Vista de los tribunales
# INPUT: comuna
# CONTEXTO: opciones de tribunales, tipo de la opcion
# OUTPUT: select_options.html
def tribunales(request,comuna):
	try:
		comuna_actual = Comuna.objects.get(id=comuna)
		tribunales = Tribunal.objects.all().filter(comuna = comuna_actual).values_list('id','nombretribunal')
		ctx = {'opciones': tribunales, 'tipo': "tribunal"}
		return render_to_response('select_options.html', ctx, context_instance=RequestContext(request))
	except:
		return HttpResponse("<option value='0'>Seleccione un tribunal</option>")


def tribunales_jurisdiccion(request,jurisdiccion):
	try:
		jurisdiccion_actual = Jurisdiccion.objects.get(id=jurisdiccion)
		tribunales = Tribunal.objects.all().filter(jurisdiccion = jurisdiccion_actual).values_list('id','nombretribunal').order_by('nombretribunal')
		ctx = {'opciones': tribunales, 'tipo': "tribunal"}
		return render_to_response('select_options.html', ctx, context_instance=RequestContext(request))
	except:
		return HttpResponse("<option value='0'>Seleccione un tribunal</option>")
