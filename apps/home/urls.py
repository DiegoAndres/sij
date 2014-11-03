from django.conf.urls import patterns,url

urlpatterns = patterns('sij.apps.home.views',
	url(r'^$','login_view', name='vista_login'),
	url(r'^logout/$', 'logout_view', name='vista_logout'),
	url(r'^inicio/$', 'redireccion', name='redirect_usuario'),
	url(r'^registro/$', 'registro_view', name='vista_registro'),
	url(r'^registro/exito/$', 'registro_exito_view', name='vista_registro_exito'),
	url(r'^registro/pendiente/$', 'registro_pendiente_view', name='vista_registro_pendiente'), 
	# url(r'^registro/receptor/(?P<username>[-\w]+)$', 'registro_receptor_view', name='vista_registro_receptor'),
	url(r'^registro/receptor/(?P<username>[-\w]+)/terminar/$', 'terminar_registro_receptor_view', name='vista_terminar_registro_receptor'),
	url(r'^datos/editar', 'editar_datos_view', name='editar_datos'),

	url(r'^receptor/tribunales/$', 'listado_tribunales_receptor_view', name='listado_tribunales_receptor'),
	url(r'^receptor/tribunales/tabla$', 'tribunales_receptor', name='listado_tribunales_receptor_tabla'),
	url(r'^receptor/tribunales/eliminar/(?P<tribunal>[-\w]+)$', 'eliminar_empleado', name="eliminar_empleado"),

	url(r'^spinner/$','spinner_view', name='vista_spinner'),

	url(r'^cuentas/contrasena/$', 'password_view', name="vista_password"),

	# url(r'^cosaqueregistrareceptores/$','registrar_receptores_view', name='vista_registrar_receptores'),
	)