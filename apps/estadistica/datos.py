from sij.apps.home.models import Evento, Empleado
from sij.apps.causas.models import Jurisdiccion, Causa, Tribunal
from django.utils import timezone
from datetime import datetime, timedelta

def tiempo_atraso():
	return 7

def tiempo_promedio_receptor(receptor):

		todasCausasDiligenciadas = Causa.objects.filter(estado="diligenciada",receptor = receptor.usuario, fechaingreso__range=[datetime.today()-timedelta(days=30)
,datetime.today()])
		ncausas = 0
		tiempo = 0.0

		for c in todasCausasDiligenciadas:
			e = Evento.objects.filter(tipoevento=2, causa=c, fechaevento__range=[datetime.today()-timedelta(days=30)
,datetime.today()])
			e1 = Evento.objects.filter(tipoevento=1, causa=c, fechaevento__range=[datetime.today()-timedelta(days=30)
,datetime.today()])
			diff = e[0].fechaevento - e1[0].fechaevento
			diff = diff.days
			ncausas = ncausas + 1
			tiempo = tiempo + diff


		if ncausas > 0:
			tiempo = float(tiempo / float(ncausas))
		else:
			tiempo = 0.0

		return tiempo

def diligencias_diarias_promedio(receptor):

	ncausas = Causa.objects.filter(estado="diligenciada",receptor = receptor.usuario, fechaingreso__range=[datetime.today()-timedelta(days=30)
,datetime.today()]).count()
	promedio = float(ncausas / float(30))


	return promedio


def datos_tribunal(tribunal, startdate, enddate):
	CP = 0
	CE = 0
	CR = 0
	CA = 0
	TP = 0.0
	DD = 0.0
	
	todasCausasPendientes = Causa.objects.filter(estado="pendiente", tribunal = tribunal, fechaingreso__range=[startdate,enddate]) #Todas las causas pendientes
	CP = todasCausasPendientes.count()

	
	todasCausasResueltas = Causa.objects.filter(estado="diligenciada", tribunal = tribunal, fechaingreso__range=[startdate,enddate]) #Todas las causas Resueltas
	
	diff = enddate - startdate
	DD = float(todasCausasResueltas.count()/float(diff.days))

	for c in todasCausasResueltas:
		try:
			e = Evento.objects.get(tipoevento=2, causa=c, fechaevento__range=[startdate,enddate])
			e1 = Evento.objects.get(tipoevento=1, causa=c, fechaevento__range=[startdate, enddate])
			diff = e.fechaevento - e1.fechaevento
			diff = diff.days
			TP = TP + diff
			CR = CR + 1	
		except:
			pass

	if todasCausasResueltas.count() > 0:
		TP = float(TP / float(todasCausasResueltas.count()))
	else:
		TP = 0.0

	todasCausasEnruta = Causa.objects.filter(estado="en ruta", tribunal = tribunal, fechaingreso__range=[startdate,enddate])
	causasAldia = todasCausasEnruta.filter(atrasada=False)

	CE = todasCausasEnruta.count()

	for c in causasAldia:
		e = Evento.objects.filter(tipoevento=1,causa=c).order_by('-fechaevento')[0]
		diff = timezone.now() - e.fechaevento	
		diff = diff.days
		if diff >= 7:
			c.atrasada = True
			c.save()

	todasCausasAtrasadas = Causa.objects.filter(atrasada=True, tribunal = tribunal, fechaingreso__range=[startdate,enddate]) #Todas las causas Atrasadas
	
	CA = todasCausasAtrasadas.count()

	datos = {'CPT':CP,'CRT':CR,'CAT':CA, 'TPT': TP, 'CET': CE, 'DDT': DD }
	return datos

def datos_jurisdiccion(jurisdiccion, startdate, enddate):
	CP = 0
	CR = 0
	CA = 0
	TP = 0.0
	n_t = 0
	CE = 0
	DD = 0.0

	tribunales = Tribunal.objects.filter(jurisdiccion = jurisdiccion)

	for t in tribunales:
		calc = datos_tribunal(t, startdate, enddate)
		CP = CP + calc['CPT']
		CR = CR + calc['CRT']
		CA = CA + calc['CAT']
		TP = TP + calc['TPT']
		CE = CE + calc['CET']
		DD = DD + calc['DDT']
		if calc['TPT'] != 0:
			n_t = n_t + 1

	if n_t > 0:
		TP = float(TP / float(n_t))
	else:
		TP = 0.0	

	datos = {'CPJ':CP,'CRJ':CR,'CAJ':CA, 'TPJ':TP, 'CEJ': CE, 'DDJ': DD }
	return datos

def datos_nacional(startdate, enddate):
	CP = 0
	CR = 0
	CA = 0
	TP = 0.0 
	n_r = 0
	CE = 0
	DD = 0

	jurisdicciones = Jurisdiccion.objects.all()

	for j in jurisdicciones:
		calc = datos_jurisdiccion(j, startdate, enddate)
		CP = CP + calc['CPJ']
		CR = CR + calc['CRJ']
		CA = CA + calc['CAJ']
		TP = TP + calc['TPJ']
		CE = CE + calc['CEJ']
		DD = DD + calc['DDJ']
		if calc['TPJ'] != 0:
			n_r = n_r + 1

	if n_r > 0:
		TP = float(TP / float(n_r))
	else:
		TP = 0.0

	datos = {'CPN':CP,'CRN':CR,'CAN':CA, 'TPN': TP, 'CEN': CE, 'DDN': DD}
	return datos







