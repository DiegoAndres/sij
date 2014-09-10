from django.conf.urls import patterns,url

urlpatterns = patterns('sij.apps.estadistica.views',
	url(r'^juez/$','juez_view', name='vista_juez'),
	url(r'^juez/receptores/jurisdiccion/(?P<jurisdiccion>[-\w]+)/$', 'juez_receptores_jurisdiccion_view', name='vista_juez_receptores_jurisdiccion'),
	# url(r'^juez/receptores/region/(?P<region>[-\w]+)/$', 'juez_receptores_region_view', name='vista_juez_receptores_region'),
	# url(r'^juez/receptores/provincia/(?P<provincia>[-\w]+)/$', 'juez_receptores_provincia_view', name='vista_juez_receptores_provincia'),
	# url(r'^juez/receptores/comuna/(?P<comuna>[-\w]+)/$', 'juez_receptores_comuna_view', name='vista_juez_receptores_comuna'),
	url(r'^juez/receptores/tribunal/(?P<tribunal>[-\w]+)/$', 'juez_receptores_tribunal_view', name='vista_juez_receptores_tribunal'),
	#url(r'^juez/grafico/region/(?P<region>[-\w]+)/$', 'grafico_region_view', name='vista_grafico_region'),
	#url(r'^juez/grafico/provincia/(?P<provincia>[-\w]+)/$', 'grafico_provincia_view', name='vista_grafico_provincia'),
	#url(r'^juez/grafico/comuna/(?P<comuna>[-\w]+)/$', 'grafico_comuna_view', name='vista_comuna_region'),
	#url(r'^juez/grafico/tribunal/(?P<tribunal>[-\w]+)/$', 'causas_view', name='vista_causas'),
	url(r'^juez/causas/$', 'causas_view', name='vista_causas'),
	)