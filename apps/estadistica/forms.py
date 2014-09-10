from django import forms
from sij.apps.causas.models import Jurisdiccion


CHOICES_JURISDICCION = Jurisdiccion.objects.all().values_list('id', 'nombrejurisdiccion')

class filtroGrafico(forms.Form):
	jurisdiccion = forms.CharField(widget=forms.Select(choices=CHOICES_JURISDICCION, attrs={'class':'form-control', 'required':'required'}))
	tribunal    = forms.CharField(widget=forms.Select(attrs={'class':'form-control', 'required': 'required'}))
	datefield 	= forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'id':'datepicker'}))
	startdate 	= forms.DateField(widget=forms.HiddenInput())
	enddate 	= forms.DateField(widget=forms.HiddenInput())

