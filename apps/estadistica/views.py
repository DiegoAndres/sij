# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponseRedirect
from sij.apps.causas.forms import filtroEstadoForm
from sij.apps.estadistica.datos import datos_tribunal, datos_jurisdiccion, datos_nacional, tiempo_promedio_receptor, diligencias_diarias_promedio
from sij.apps.estadistica.forms import filtroGrafico
from sij.apps.causas.models import Jurisdiccion, Causa, Region, Provincia, Comuna, Tribunal
from sij.apps.home.models import Receptor, Empleado
from django.core.paginator import Paginator, EmptyPage, InvalidPage, PageNotAnInteger
from django.utils import timezone
from datetime import datetime




# Vista de la pagina principal del Juez. Incluye el manejo de datos del grafico y tablas
# INPUT: -
# CONTEXTO: datos locales y nacionales
# OUTPUT: juez.html
def juez_view(request):
	if request.user.is_authenticated() and request.user.usuario.tipo == 2:
		if request.GET:
			flag = 0
			form = filtroGrafico(request.GET)

			try:
	 			startdate = request.GET['startdate']
	 			enddate = request.GET['enddate']
 				nacional = datos_nacional(startdate, enddate)
		 	except:
		 		flag = 1
		 		nacional = datos_nacional(datetime(2013, 05, 13, 18, 38, 50),datetime.now())
		 	try:
				t=Tribunal.objects.get(id=request.GET['tribunal'])
				if flag == 0:
	 				datos = datos_tribunal(t, stardate, enddate)
	 			else:
	 				datos = datos_tribunal(t, datetime(2013, 05, 13, 18, 38, 50),datetime.now())
			 	ctx= {'form': form, 'datos':datos, 'nacional':nacional, 'tipo': "Tribunal", 'tribunal':t}
				return render_to_response('estadistica/juez.html',ctx,context_instance=RequestContext(request))

			except:
				try:
					j = Jurisdiccion.objects.get(id=request.GET['jurisdiccion'])
					if flag == 0:
						datos = datos_jurisdiccion(j, startdate, enddate)
					else:
						datos = datos_jurisdiccion(j, datetime(2013, 05, 13, 18, 38, 50),datetime.now())
					ctx= {'form': form, 'datos':datos, 'tipo': "Jurisdiccion",'nacional':nacional,  'jurisdiccion': j}
					return render_to_response('estadistica/juez.html',ctx,context_instance=RequestContext(request))
				except:
					ctx = {'form': form, 'mensaje': 'Debe seleccionar algún filtro para comparar.'}
					return render_to_response('estadistica/juez.html', ctx, context_instance=RequestContext(request))
		else:
			form = filtroGrafico()
			ctx= {'form': form}
			return render_to_response('estadistica/juez.html',ctx,context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/')
	


# Vista de los receptores de un tribunal en el panel del Juez
# INPUT: id tribunal
# CONTEXTO: receptores
# OUTPUT: table_receptores.html
def juez_receptores_tribunal_view(request,tribunal):
	if request.user.is_authenticated() and request.user.usuario.tipo == 2:
		trib = Tribunal.objects.get(id = tribunal)
		receptores = trib.empleados.all()
		rs = set()
		
		for r in receptores:		
			r.causasenruta = Causa.objects.filter(receptor = r.usuario, estado = 'en ruta').count()
			r.tiempopromedio = tiempo_promedio_receptor(r)
			r.diligenciasdiariaspromedio = diligencias_diarias_promedio(r)
			r.save()
			rs.add(r)

		ctx = {'receptores': rs}
		return render_to_response('tables/table_receptores.html',ctx, context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/')	



# Vista de los receptores de una jurisdicción en el panel del Juez
# INPUT: id jurisdicción
# CONTEXTO: receptores
# OUTPUT: table_receptores.html
def juez_receptores_jurisdiccion_view(request,jurisdiccion):
	if request.user.is_authenticated() and request.user.usuario.tipo == 2:
		tribs = Tribunal.objects.filter(jurisdiccion = jurisdiccion)
		empleados = Empleado.objects.filter(tribunal__in = tribs)
		receptores = set()

		for e in empleados:
			e.receptor.causasenruta = Causa.objects.filter(receptor = e.receptor.usuario, estado = 'en ruta').count()
			e.receptor.tiempopromedio = tiempo_promedio_receptor(e.receptor)
			e.receptor.diligenciasdiariaspromedio = diligencias_diarias_promedio(e.receptor)
			e.receptor.save()
			receptores.add(e.receptor)

		ctx = {'receptores': receptores}
		return render_to_response('tables/table_receptores.html',ctx, context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/')	

# Vista de las causas en el panel del Juez
# INPUT: -
# CONTEXTO: causas, form, date
# OUTPUT: table_causas_juez.html
def causas_view(request):
	if request.user.is_authenticated():
		date = 0
		filter_args = {}
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
				 		ctx = {'error': 'La fecha no cumple con el formato.', 'form': form}
				 		return render_to_response('tables/table_causas_juez.html',ctx, context_instance=RequestContext(request))

			if estado != '':
				if estado != 'incompleta':
					filter_args['estado'] = estado
					if estado == 'diligenciada':
						estados_excluidos.remove('diligenciada')
					else:
						if estado == 'eliminada':
							estados_excluidos.remove('eliminada')
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
			return render_to_response('tables/table_causas_juez.html',ctx, context_instance=RequestContext(request))

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
			return render_to_response('tables/table_causas_juez.html',ctx, context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/')

