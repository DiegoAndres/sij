from django.conf.urls import patterns,url

urlpatterns = patterns('sij.apps.estampado.views',
	url(r'^estampado/(?P<idcausa>[-\w]+)/pdf$','libro_pdf', name='vista_libro_pdf'),
	url(r'^prueba/(?P<idcausa>[-\w]+)/pdf$','prueba', name='prueba'),
	)