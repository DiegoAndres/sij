from django.conf.urls import patterns, url
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = patterns('sij.apps.causas.views',
	url(r'^abogado/$','abogado_view', name='vista_abogado'),
	url(r'^nuevacausa/$','nueva_causa_view', name='vista_nueva_causa'),
	url(r'^nuevacausa/(?P<tribunal>[-\w]+)/$','asignar_receptor_view', name='vista_asignar_receptor'),
	url(r'^notificaciones/nuevas/$','notificaciones_view', name='vista_notificaciones'),
	url(r'^notificaciones/leidas/$','notificaciones_leidas_view', name='vista_notificaciones_leidas'),
	url(r'^notificaciones/page/(?P<pagina>.*)/$','notificaciones_todas_view', name='vista_notificaciones_todas'),
	url(r'^notificaciones/icono/$','icono_notificaciones', name='vista_icono_notificaciones'),

	url(r'^receptor/$','receptor_view', name='vista_receptor'),
	url(r'^causas/panel/$', 'panel_causas_view', name='panel_causas'),
	url(r'^causas/tabla/$', 'tabla_causas_view', name='tabla_causas'),
	url(r'^causa/(?P<idcausa>[-\w]+)/detalle/$', 'detalle_causa_view', name='detalle_causa'),
	url(r'^causa/(?P<idcausa>[-\w]+)/detalle/diligencia$', 'detalle_diligencia_causa_view', name='detalle_diligencia_causa'),
	url(r'^causa/(?P<idcausa>[-\w]+)/opciones/receptor$', 'opciones_receptor_causa_view', name='opciones_receptor_causa'),
	url(r'^causa/(?P<idcausa>[-\w]+)/opciones/abogado$', 'opciones_abogado_causa_view', name='opciones_abogado_causa'),
	url(r'^causa/(?P<idcausa>[-\w]+)/aceptar/$', 'aceptar_causa_view', name='aceptar_causa'),
	url(r'^causa/(?P<idcausa>[-\w]+)/aceptar/deshacer/$', 'deshacer_aceptar_causa_view', name='deshacer_aceptar_causa'),
	url(r'^causa/(?P<idcausa>[-\w]+)/rechazar/$', 'rechazar_causa_view', name='rechazar_aceptar_causa'),
	url(r'^causa/(?P<idcausa>[-\w]+)/eliminar/$', 'eliminar_causa_view', name='eliminar_aceptar_causa'),
	url(r'^causa/(?P<idcausa>[-\w]+)/reasignar/$', 'reasignar_causa_view', name='reasignar_causa'),
	url(r'^causa/(?P<idcausa>[-\w]+)/reasignar/registrar/$', 'registro_reasignar_causa_view', name='registro_reasignar_causa'),
	url(r'^causa/(?P<idcausa>[-\w]+)/diligenciar/$', 'diligenciar_causa_view', name='diligenciar_causa'),
	url(r'^causa/(?P<idcausa>[-\w]+)/diligenciar/opciones/$', 'opciones_diligenciar_causa_view', name='opciones_diligenciar_causa'),
	url(r'^causa/(?P<idcausa>[-\w]+)/diligenciar/registrar/$', 'registrar_diligenciar_causa_view', name='registrar_diligenciar_causa'),
	url(r'^causa/(?P<idcausa>[-\w]+)/diligenciar/foto/$', 'foto_diligenciar_causa_view', name='foto_diligenciar_causa'),
	url(r'^causa/(?P<idcausa>[-\w]+)/diligenciar/foto/opciones/$', 'opciones_foto_diligenciar_causa_view', name='opciones_foto_diligenciar_causa'),
	url(r'^causa/(?P<idcausa>[-\w]+)/diligenciar/foto/registrar/$', 'registrar_foto_diligenciar_causa_view', name='registrar_foto_diligenciar_causa'),

	url(r'^diligencia/(?P<diligencia>[-\w]+)/respuesta/$', 'diligencias', name='diligencias'),
	url(r'^jurisdiccion/(?P<jurisdiccion>[-\w]+)/tribunales/$', 'tribunales_jurisdiccion', name='tribunales_jurisdiccion'),
	url(r'^region/(?P<region>[-\w]+)/provincias/$', 'provincias', name='provincias'),
	url(r'^provincia/(?P<provincia>[-\w]+)/comunas/$', 'comunas', name='comunas'),
	url(r'^comuna/(?P<comuna>[-\w]+)/tribunales/$', 'tribunales', name='tribunales'),

	url(r'^imagen/(?P<id_imagen>[-\w]+)/rotar/$', 'rotar_imagen_view', name='rotar_imagen')

	)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)