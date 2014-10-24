# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings
from sij.apps.causas.models import Causa,Region,Tribunal, Diligencia, ResultadoDiligencia, Jurisdiccion

CHOICES_REGION = Region.objects.all().values_list('id','nombreregion').exclude(nombreregion='-')
CHOICES_MATERIA = (('civil','Civil'),
					('cobranza', 'Cobranza'),
					('cobranza laboral','Cobranza Laboral'),
					('familia','Familia'),
					('penal','Penal'),
					('laboral', 'Laboral'),
					('laboral antiguo','Laboral Antiguo'),
					('otro', 'Otro'))
CHOICES_JURISDICCION = Jurisdiccion.objects.all().values_list('id','nombrejurisdiccion')
CHOICES_DILIGENCIA = Diligencia.objects.filter(tipodiligencia='objetivo').values_list('id', 'detallediligencia')
CHOICES_RESULTADO_DILIGENCIA = Diligencia.objects.filter(tipodiligencia = 'respuesta').exclude(detallediligencia = 'sin diligenciar').values_list('id','detallediligencia')
CHOICES_ESTADOS = (('pendiente','Pendientes'),
					('en ruta','En ruta'),
					('diligenciada','Diligenciadas'),
					('','Todas'))

class nuevaCausaForm(forms.Form):
	ncausa = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control input-lg', 'required': 'required', 'placeholder': 'N° de causa'}))
	materia = forms.CharField(widget=forms.Select(choices=CHOICES_MATERIA, attrs={'class':'form-control input-lg', 'required': 'required'}))
	region 		= forms.CharField(widget=forms.Select(choices=CHOICES_REGION, attrs={'class':'form-control input-lg', 'required': 'required'}))
	provincia 	= forms.CharField(widget=forms.Select(attrs={'class':'form-control input-lg', 'required': 'required'}))
	comuna 		= forms.CharField(widget=forms.Select(attrs={'class':'form-control input-lg', 'required': 'required'}))
	direccion 		= forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control input-lg', 'placeholder': 'Dirección'}))
	jurisdiccion 	= forms.CharField(widget=forms.Select(choices=CHOICES_JURISDICCION, attrs={'class':'form-control input-lg', 'required': 'required'}))
	tribunalOrigen 	= forms.CharField(widget=forms.Select(attrs={'class':'form-control input-lg', 'required': 'required'}))
	tipoDiligencia  = forms.CharField(widget=forms.Select(choices=CHOICES_DILIGENCIA,attrs={'class':'form-control input-lg', 'required': 'required'}))
	observacion = forms.CharField(widget=forms.Textarea(attrs={'class' : 'form-control input-lg','style':'height: 30%;', 'placeholder': 'Observación'}),required=False)
	receptor = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control input-lg', 'required': 'required', 'Disabled': True}))

class receptorForm(forms.Form):
	idr = forms.IntegerField(widget=forms.TextInput(attrs={'class' : 'form-control', 'required': 'required'}))

class reasignarForm(forms.Form):
	jurisdiccion 	= forms.CharField(widget=forms.Select(choices=CHOICES_JURISDICCION, attrs={'class':'form-control', 'required': 'required'}))
	tribunal 		= forms.CharField(widget=forms.Select(attrs={'class':'form-control', 'required': 'required'}))
	receptorNuevo 	= forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}))
	causa 			= forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}))

class filtroEstadoForm(forms.Form):
	estado 		= forms.CharField(widget=forms.HiddenInput())
	sort 		= forms.CharField(widget=forms.HiddenInput())
	page 		= forms.IntegerField(widget=forms.HiddenInput())
	searchtype 	= forms.CharField(widget=forms.HiddenInput())
	search 		= forms.CharField(widget=forms.HiddenInput())
	startdate 	= forms.DateField(widget=forms.HiddenInput())
	enddate 	= forms.DateField(widget=forms.HiddenInput())

class filtroSortPagForm(forms.Form):
	sort 		= forms.CharField(widget=forms.HiddenInput())
	page 		= forms.IntegerField(widget=forms.HiddenInput())

class diligenciarCausaForm(forms.Form):
	objetivodiligencia  = forms.CharField(widget=forms.Select(choices=CHOICES_DILIGENCIA,attrs={'class':'form-control', 'required': 'required'}))
	resultadodiligencia = forms.CharField(widget=forms.Select(attrs={'class':'form-control', 'required': 'required'}))
	demandante  		= forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'required': 'required'}))
	demandado  			= forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'required': 'required'}))
	fojas  				= forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'required': 'required'}))
	comentario 			= forms.CharField(required=False, widget=forms.Textarea(attrs={'class' : 'form-control', 'rows': 5}))
	derechos 			= forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'required': 'required'}))
	lat   				= forms.FloatField(widget=forms.HiddenInput())
	lon  				= forms.FloatField(widget=forms.HiddenInput())

	# def clean_tipodiligencia(self):
	# 	tipo = self.cleaned_data['tipodiligencia']
	# 	return tipo

	def clean_comentario(self):
		comentario = self.cleaned_data['comentario']
		return comentario


class fotoDiligenciarCausaForm(forms.Form):
	foto 			= forms.FileField()

	def clean_foto(self):
		foto = self.cleaned_data['foto']
		# content_type = foto.content_type
		# if content_type in settings.CONTENT_TYPES:
		# 	if foto._size > settings.MAX_UPLOAD_SIZE:
		# 		raise forms.ValidationError('size muy grande')
		# else:
		# 	raise forms.ValidationError('formato no soportado')
		return foto

class pagoDiligenciaForm(forms.Form):
	idcausa = forms.CharField(widget=forms.HiddenInput())
	valor = forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control input-lg', 'required': 'required', 'placeholder': 'Valor Diligencia'}))
	rut = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control input-lg', 'required':'required', 'pattern':'[0-9]{6,8}[\-][a-zA-Z0-9]{1}', 'placeholder': 'Rut'}))
	cuenta = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control input-lg', 'required':'required', 'placeholder': 'N° Cuenta'}))
	banco = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control input-lg', 'required':'required', 'placeholder': 'Banco'}))