# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from sij.apps.home.forms import LoginForm, RegistrationForm, EmpleadoForm, EditarDatosForm
from sij.apps.home.models import Usuario, Receptor, Empleado
from sij.apps.causas.models import Comuna, Tribunal
from django.contrib.auth import login, authenticate, logout
from django.core.urlresolvers import reverse
# from django.contrib.auth.views import password_reset
from django.contrib.auth.models import User
# from django.core.mail import EmailMultiAlternatives
# from django.db.models import Q
from django.views.decorators.csrf import csrf_protect, csrf_exempt, requires_csrf_token, ensure_csrf_cookie

@ensure_csrf_cookie
def login_view(request):
	mensaje = ""
	if request.user.is_authenticated():
		return redireccion(request)
	else:
		if request.method == "POST":
			form = LoginForm(request.POST)
			if form.is_valid():
				username = form.cleaned_data['username']
				password = form.cleaned_data['password']
				usuario = authenticate(username=username, password=password)
				if usuario is not None:
					if usuario.is_active:
						login(request, usuario)
						return redireccion(request)
					else:
						mensaje = "Su cuenta aún no ha sido validada por un administrador."
						ctx = {'form': form, 'mensaje': mensaje}
						return render_to_response('home/login.html', ctx, context_instance=RequestContext(request))
				else:
					mensaje = "Usuario y/o password incorrecto."
					ctx = {'form': form, 'mensaje': mensaje}
					return render_to_response('home/login.html', ctx, context_instance=RequestContext(request))
		form = LoginForm()
		ctx = {'form': form, 'mensaje': mensaje}
		return render_to_response('home/login.html', ctx, context_instance=RequestContext(request))


def login_check_view(request):
	if request.user.is_authenticated():
		return HttpResponse('1')
	else:
		return HttpResponse('0')

def redireccion(request):
	if request.user.is_authenticated():
		try:
			tipo = request.user.usuario.tipo
			if tipo == 0:
				return HttpResponseRedirect('/abogado')
			if tipo == 1:
				return HttpResponseRedirect('/receptor')
			# if tipo == 2:
			# 	return HttpResponseRedirect('/juez')
			else:
				return HttpResponseRedirect('/admin')
		except:
			logout(request) # esto es por si se enfermó el login.
			return HttpResponseRedirect('/')
	else:
		return HttpResponseRedirect('/')

def logout_view(request):
	logout(request)	
	return HttpResponseRedirect('/')

def registro_view(request):
	mensaje=""
	if request.user.is_authenticated():
		return redireccion(request)
	else:
		if request.method == "POST":
			form = RegistrationForm(request.POST)
			if form.is_valid():
				# registro
				rol = form.cleaned_data['rol']
				# rut = form.cleaned_data['rut']
				# nombre = form.cleaned_data['nombre']
				# apellido = form.cleaned_data['apellido']
				username = form.cleaned_data['username']
				email = form.cleaned_data['email']
				password1 = form.cleaned_data['password1']
				password2 = form.cleaned_data['password2']
				# comuna 	= form.cleaned_data['comuna']
				# direccion = form.cleaned_data['direccion']
				# telefono = form.cleaned_data['telefono']

				if rol == '0': #abogado
					try:
						new_user = User.objects.create_user(username=username, email=email, password=password1)
						# new_user.first_name = nombre
						# new_user.last_name = apellido
						new_user.save()
						
						new_abogado = Usuario()
						new_abogado.user = new_user
						# new_abogado.rut = rut
						new_abogado.tipo = int(rol)
						cmna = Comuna.objects.get(id=16101)
						new_abogado.comuna = cmna
						# new_abogado.direccion = direccion
						# if telefono:
							# new_abogado.telefono = telefono
						new_abogado.save()

						# login
						new_user = authenticate(username=username, password=password1)
						login(request, new_user)
						return HttpResponseRedirect('/registro/exito')
					except: #en caso de que no se pueda registrar el usuario completo
						User.objects.get(username = username).delete()
						mensaje = "Ha ocurrido un error al registrar al nuevo usuario."
				if rol == '1': #receptor
					try:
						new_user = User.objects.create_user(username=username, email=email, password=password1)
						# new_user.first_name = nombre
						# new_user.last_name = apellido
						#new_user.is_active = False
						new_user.save()

						new_receptor = Usuario()
						new_receptor.user = new_user
						# new_receptor.rut = rut
						new_receptor.tipo = int(rol)
						cmna = Comuna.objects.get(id=int(16101))
						new_receptor.comuna = cmna
						# new_receptor.direccion = direccion
						# if telefono:
							# new_receptor.telefono = telefono
						new_receptor.save()

						receptor_detalle = Receptor(usuario = new_receptor)
						receptor_detalle.save()

						# login
						new_user = authenticate(username=username, password=password1)
						login(request, new_user)
						return HttpResponseRedirect('/registro/exito')
					except:
						Usuario.objects.get(user__username = username).delete()
						User.objects.get(username=username).delete()
						mensaje = "Ha ocurrido un error al registrar al nuevo receptor."
				# if rol == '2': #juez
				# 	try:
				# 		new_user = User.objects.create_user(username=username, email=email, password=password1)
				# 		new_user.first_name = nombre
				# 		new_user.last_name = apellido
				# 		new_user.is_active = False
				# 		new_user.save()

				# 		new_juez = Usuario()
				# 		new_juez.user = new_user
				# 		new_juez.rut = rut
				# 		new_juez.tipo = int(rol)						
				# 		cmna = Comuna.objects.get(id=int(comuna))
				# 		new_juez.comuna = cmna
				# 		new_juez.direccion = direccion
				# 		new_juez.save()

				# 		return HttpResponseRedirect('/registro/pendiente')
				# 	except:
				# 		User.objects.get(username=username).delete()
				# 		mensaje = "Ha ocurrido un error al registrar al nuevo usuario."

				ctx = {'form': form, 'mensaje': mensaje}
				return render_to_response('home/registro.html', ctx, context_instance=RequestContext(request))
			else:
				data = request.POST.copy()
				data['region'] = 0
				form = RegistrationForm(data)
				ctx = {'form': form, 'mensaje': mensaje}
				return render_to_response('home/registro.html', ctx, context_instance=RequestContext(request))
		form = RegistrationForm()
		ctx = {'form': form, 'mensaje': mensaje}
		return render_to_response('home/registro.html', ctx, context_instance=RequestContext(request))

def registro_exito_view(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/')
	else:
		return render_to_response('home/registro_exito.html', context_instance=RequestContext(request))

def registro_pendiente_view(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/')
	else:
		return render_to_response('home/registro_pendiente.html', context_instance=RequestContext(request))	

# def registro_receptor_view(request,username):
# 	mensaje=""
# 	if request.user.is_authenticated():
# 		return redireccion(request)
# 	else:
# 		if request.method == "POST":
# 			form = EmpleadoForm(request.POST)
# 			if form.is_valid():
# 				tribunal = form.cleaned_data['tribunal']
# 				t = Tribunal.objects.get(id=tribunal)

# 				user = User.objects.get(username=username)
# 				usuario = Usuario.objects.get(user=user)
# 				receptor = Receptor.objects.get(usuario=usuario)

# 				try:
# 					e = Empleado.objects.get(receptor = receptor, tribunal=t)
# 					mensaje = "El tribunal ya ha sido agregado."
# 					ctx = {'form': form,'mensaje': mensaje, 'error': 1, 'username': username}
# 					return render_to_response('home/registro_receptor.html', ctx, context_instance=RequestContext(request))
# 				except:						
# 					e = Empleado(receptor = receptor, tribunal = t)
# 					e.save()
# 					# mensaje = "registro!"
# 					ctx = {'form': form,'mensaje': mensaje, 'username': username}
# 					return render_to_response('home/registro_receptor.html', ctx, context_instance=RequestContext(request))
# 			else:
# 				form = EmpleadoForm()
# 				ctx = {'form': form,'mensaje': mensaje, 'username': username}
# 				return render_to_response('home/registro_receptor.html', ctx, context_instance=RequestContext(request))
# 		form = EmpleadoForm()
# 		ctx = {'form': form,'mensaje': mensaje, 'username': username}
# 		return render_to_response('home/registro_receptor.html', ctx, context_instance=RequestContext(request))

def terminar_registro_receptor_view(request, username):
	user = User.objects.get(username=username)
	usuario = Usuario.objects.get(user=user)
	receptor = Receptor.objects.get(usuario=usuario)

	tribunales = receptor.tribunales.all()
	if not tribunales:
		return HttpResponse('0')
	else:
		return HttpResponse('1')

def listado_tribunales_receptor_view(request):
	mensaje=""
	if request.user.is_authenticated():
		if request.method == "POST":
			form = EmpleadoForm(request.POST)
			if form.is_valid():
				tribunal = form.cleaned_data['tribunal']
				try:
					t = Tribunal.objects.get(id=tribunal)

					usuario = Usuario.objects.get(user=request.user)
					receptor = Receptor.objects.get(usuario=usuario)

					try:
						e = Empleado.objects.get(receptor = receptor, tribunal=t)
						mensaje = "El tribunal ya ha sido agregado."
						ctx = {'form': form,'mensaje': mensaje, 'error': 1}
						return render_to_response('home/tribunales_receptor.html', ctx, context_instance=RequestContext(request))
					except:						
						e = Empleado(receptor = receptor, tribunal = t)
						e.save()
						# mensaje = "registro!
						ctx = {'form': form,'mensaje': mensaje}
						return render_to_response('home/tribunales_receptor.html', ctx, context_instance=RequestContext(request))
				except:
					mensaje = "Debe seleccionar un tribunal."
					ctx = {'form': form, 'mensaje': mensaje, 'error': 1}
					return render_to_response('home/tribunales_receptor.html', ctx, context_instance=RequestContext(request))					
			else:
				mensaje = "Debe seleccionar un tribunal."
				ctx = {'form': form,'mensaje': mensaje, 'error':1}
				return render_to_response('home/tribunales_receptor.html', ctx, context_instance=RequestContext(request))
		else:
			form = EmpleadoForm()
			ctx = {'form': form,'mensaje': mensaje}
			return render_to_response('home/tribunales_receptor.html', ctx, context_instance= RequestContext(request))
	else:
		return redireccion(request)

def tribunales_receptor(request):
	receptor= Receptor.objects.get(usuario=request.user.usuario)
	tribunales = receptor.tribunales.all()
	ctx = {'tribunales': tribunales}
	return render_to_response('tables/table_tribunales.html', ctx, context_instance=RequestContext(request))


def eliminar_empleado(request,tribunal):
	if request.user.is_authenticated():
		t = Tribunal.objects.get(id = tribunal)
		user = User.objects.get(username = request.user.username)
		usuario = Usuario.objects.get(user = user)
		receptor = Receptor.objects.get(usuario = usuario)
		try:
			e = Empleado.objects.get(receptor = receptor, tribunal = t)
			e.delete()
		except Empleado.DoesNotExist:
			pass

		return tribunales_receptor(request)
	else:
		return HttpResponseRedirect('/')

def editar_datos_view(request):
	if request.user.is_authenticated():
		if request.POST:
			form = EditarDatosForm(request.POST)
			if form.is_valid():
				try:
					user = request.user
					usuario = request.user.usuario

					user.email = form.cleaned_data['email']
					cmna = form.cleaned_data['comuna']
					comuna = Comuna.objects.get(id = cmna)
					usuario.comuna = comuna
					usuario.direccion = form.cleaned_data['direccion']
					usuario.telefono = form.cleaned_data['telefono']

					# user.save();
					usuario.save();

					ctx = {'form': form, 'error': 0, 'mensaje': 'Los cambios se han guardado con éxito.'}
				except:
					ctx = {'form': form, 'error': 1, 'mensaje': 'Ha ocurrido un error al guardar los datos. Si el error persiste contacte al administrador.'}
			return render_to_response('home/editar_usuario.html', ctx, context_instance=RequestContext(request))
		else:
			user = request.user
			usuario = request.user.usuario
			form = EditarDatosForm(initial={'email': user.email, 'region': usuario.comuna.provincia.region.id, 'provincia': usuario.comuna.provincia.id, 'comuna': usuario.comuna.id, 'direccion': usuario.direccion, 'telefono': usuario.telefono})
			ctx = {'form': form}
			return render_to_response('home/editar_usuario.html', ctx, context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/')


def spinner_view(request):
	return render_to_response('spinner.html', context_instance=RequestContext(request))
