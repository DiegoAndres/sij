import ho.pisa as pisa
import cStringIO as StringIO
import cgi
from django.template import RequestContext
from django.template.loader import render_to_string
from django.http import HttpResponse
from sij.apps.causas.models import Causa, ResultadoDiligencia, FotoDiligencia
from django.shortcuts import render_to_response
from django.core.mail import EmailMessage

import os
from django.conf import settings

def fetch_resources(uri, rel):
	if uri.startswith(settings.MEDIA_URL):
		path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
	elif uri.startswith(settings.STATIC_URL):
		path = os.path.join(settings.STATIC_ROOT, uri.replace(settings.STATIC_URL, ""))
	else:
		path = uri
		
	return path

def generar_pdf(request, html, causa):
	result = StringIO.StringIO()
	pdf = pisa.pisaDocument(StringIO.StringIO(html.encode('UTF-8')), result, link_callback= fetch_resources)
	if not pdf.err:
		title = 'Estampado causa rol '+causa.ncausa
		body = 'Se adjunta el estampado para la causa '+ causa.ncausa
		email = EmailMessage(title, body, 'no-reply@sij.cl', [causa.receptor.user.email])
		email.attach('estampado.pdf', result.getvalue(), 'application/pdf')
		email.send()
		return HttpResponse('0')
		# return HttpResponse(result.getvalue(), mimetype='application/pdf')
	else:
		return HttpResponse('Error al generar el PDF: %s' % cgi.escape(html))

def libro_pdf(request, idcausa):
	causa = Causa.objects.get(id=idcausa)
	resultado = ResultadoDiligencia.objects.get(causa = causa)
	fotos = FotoDiligencia.objects.filter(resultadodiligencia = resultado)
	ctx = {'causa': causa, 'resultado': resultado, 'fotos': fotos}

	html = render_to_string('estampado/libro_pdf.html', ctx, context_instance=RequestContext(request))
	# return render_to_response('estampado/libro_pdf.html', ctx, context_instance=RequestContext(request))
	return generar_pdf(request, html, causa)

def prueba(request, idcausa):
	causa = Causa.objects.get(id=idcausa)
	resultado = ResultadoDiligencia.objects.get(causa = causa)
	fotos = FotoDiligencia.objects.filter(resultadodiligencia = resultado)
	ctx = {'causa': causa, 'resultado': resultado, 'fotos': fotos}
	return render_to_response('estampado/libro_pdf.html', ctx, context_instance=RequestContext(request))