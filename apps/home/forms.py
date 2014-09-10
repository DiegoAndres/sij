# -*- coding: utf-8 -*-
from django import forms 
from sij.apps.causas.models import Jurisdiccion, Region, Provincia, Comuna, Tribunal
from sij.apps.home.models import Empleado
from django.contrib.auth.models import User
from itertools import cycle
 
def digito_verificador(rut):
	reversed_digits = map(int, reversed(str(rut)))
	factors = cycle(range(2, 8))
	s = sum(d * f for d, f in zip(reversed_digits, factors))
	return (-s) % 11

class LoginForm(forms.Form):
	username 	= forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control input-lg', 'required': 'required', 'placeholder': 'Nombre de usuario'}))
	password 	= forms.CharField(widget=forms.PasswordInput(render_value=False, attrs={'class':'form-control input-lg', 'required':'required', 'placeholder': 'Contraseña'}))

RADIO_ROL=[[0,'Abogado'],[1,'Receptor']]
CHOICES_REGION = Region.objects.all().values_list('id','nombreregion').exclude(nombreregion='-')
CHOICES_COMUNA = Comuna.objects.all().values_list('id','nombrecomuna').exclude(nombrecomuna='-')
CHOICES_JURISDICCION = Jurisdiccion.objects.all().values_list('id', 'nombrejurisdiccion')


# *************FORM DE REGISTRO COMPLETO****************
# class RegistrationForm(forms.Form):
# 	error_messages={
# 		'duplicate_username': "El nombre de usuario ya existe.",
# 	}

# 	rol 		= forms.ChoiceField(widget=forms.RadioSelect(attrs={'required':'required'}),choices=RADIO_ROL)	
# 	rut 		= forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'required':'required', 'pattern':'[0-9]{6,8}[\-][a-zA-Z0-9]{1}'}))
# 	nombre 		= forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control', 'required':'required'}))
# 	apellido 	= forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'required':'required'}))
# 	username	= forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control', 'required':'required'}))
# 	email 		= forms.CharField(widget=forms.EmailInput(attrs={'class' : 'form-control', 'required':'required'}))
# 	password1 	= forms.CharField(widget=forms.PasswordInput(render_value=False,attrs={'class' : 'form-control', 'required':'required'}))
# 	password2 	= forms.CharField(widget=forms.PasswordInput(render_value=False,attrs={'class' : 'form-control', 'required':'required'}))
# 	region 		= forms.CharField(widget=forms.Select(choices=CHOICES_REGION, attrs={'class':'form-control', 'required':'required'}))
# 	provincia 	= forms.CharField(widget=forms.Select(attrs={'class':'form-control', 'required':'required'}))
# 	comuna 		= forms.CharField(widget=forms.Select(attrs={'class':'form-control', 'required':'required'}))
# 	direccion 	= forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'required':'required'}))
# 	telefono 	= forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
# ********************************************************

class RegistrationForm(forms.Form):
	error_messages={
		'duplicate_username': "El nombre de usuario ya existe.",
	}

	rol 		= forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control input-lg', 'required':'required'}),choices=RADIO_ROL)	
	username	= forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control input-lg', 'required':'required', 'placeholder': 'Nombre de usuario'}))
	email 		= forms.CharField(widget=forms.EmailInput(attrs={'class' : 'form-control input-lg', 'required':'required', 'placeholder': 'Correo electrónico'}))
	password1 	= forms.CharField(widget=forms.PasswordInput(render_value=False,attrs={'class' : 'form-control input-lg', 'required':'required', 'placeholder': 'Contraseña'}))
	password2 	= forms.CharField(widget=forms.PasswordInput(render_value=False,attrs={'class' : 'form-control input-lg', 'required':'required', 'placeholder': 'Repetir contraseña'}))

	def clean_telefono(self):
		telefono = self.cleaned_data['telefono']
		return telefono

	def clean_rut(self):
		rut = self.cleaned_data['rut']
		rut, digito = rut.split("-",1)

		revisar = digito_verificador(rut)

		if revisar == 10 and digito == 'k':
			return rut
		else:
			if revisar == int(digito):
				return rut
			else:
				raise forms.ValidationError('El rut ingresado no es válido.')



	def clean_username(self):
		username = self.cleaned_data['username']
		try:
			u = User.objects.get(username=username)
			raise forms.ValidationError('El nombre de usuario ya existe.')
		except User.DoesNotExist:
			return username	

	def clean_email(self):
		email = self.cleaned_data['email']
		try:
			u = User.objects.get(email=email)
			raise forms.ValidationError('El correo ya existe.')
		except User.DoesNotExist:
			return email
		
	def clean_password2(self):
		password1 = self.cleaned_data['password1']
		password2 = self.cleaned_data['password2']
		if password1 == password2:
			return password2
		else:
			raise forms.ValidationError('Las contraseñas no coinciden')


class PasswordForm(forms.Form):
	email 	= forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}))

class EmpleadoForm(forms.Form):
	jurisdiccion = forms.CharField(widget=forms.Select(choices = CHOICES_JURISDICCION, attrs={'class': 'form-control', 'required':'required'}))
	tribunal 	= forms.CharField(widget=forms.Select(attrs={'class':'form-control', 'required':'required'}))
	
	def clean_tribunal(self):
		tribunal = self.cleaned_data['tribunal']
		try:
			t = Tribunal.objects.get(id=tribunal)
			return tribunal
		except:
			raise forms.ValidationError('Debe seleccionar un tribunal.')

class EditarDatosForm(forms.Form):
	email 	= forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control input-lg', 'placeholder': 'Correo electrónico'}))
	region 		= forms.CharField(widget=forms.Select(choices=CHOICES_REGION, attrs={'class':'form-control input-lg', 'required':'required', 'placeholder': 'Región'}))
	provincia 	= forms.CharField(widget=forms.Select(attrs={'class':'form-control input-lg', 'required':'required', 'placeholder': 'Provincia'}))
	comuna 		= forms.CharField(widget=forms.Select(attrs={'class':'form-control input-lg', 'required':'required', 'placeholder': 'Comuna'}))
	direccion 	= forms.CharField(widget=forms.TextInput(attrs={'class':'form-control input-lg', 'required':'required', 'placeholder': 'Dirección'}))
	telefono 	= forms.CharField(widget=forms.TextInput(attrs={'class':'form-control input-lg', 'placeholder': 'Teléfono'}), required=False)


class RegistrarReceptorForm(forms.Form):
	nombre 			= forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Nombre'}))
	apellido 		= forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Apellido'}))
	email 			= forms.CharField(widget=forms.TextInput(attrs={'placeholder' : 'Correo electrónico'}))
	direccion 		= forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Dirección', 'required':'required'}))
	comuna 			= forms.CharField(widget=forms.Select(choices= CHOICES_COMUNA, attrs={'required':'required'}))
	telefono 		= forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Teléfono'}), required=False)
	jurisdiccion 	= forms.CharField(widget=forms.Select(choices = CHOICES_JURISDICCION, attrs={'required':'required'}))