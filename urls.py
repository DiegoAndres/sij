from django.conf.urls import patterns, include, url
import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include('sij.apps.home.urls')),
    url(r'^', include('sij.apps.causas.urls')),
    url(r'^', include('sij.apps.estadistica.urls')),
    url(r'^', include('sij.apps.estampado.urls')),
	url(r'^cuentas/contrasena/recuperar/$', 'django.contrib.auth.views.password_reset', 
		{'post_reset_redirect' : '/cuentas/contrasena/reset/exito/'}, name="vista_recuperar_contrasena"),
	url(r'^cuentas/contrasena/reset/exito/$', 'django.contrib.auth.views.password_reset_done'),
	url(r'^cuentas/contasena/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', 
		{'post_reset_redirect' : '/cuentas/contrasena/exito/'}, name="auth_password_reset_confirm"),

	url(r'^cuentas/contrasena/exito/$', 'django.contrib.auth.views.password_reset_complete'),

	url(r'^cuentas/contrasena/cambiar/$', 'django.contrib.auth.views.password_change', name="password_change_form"),
	url(r'^cuentas/contrasena/cambiar/exito$', 'django.contrib.auth.views.password_change_done', name="password_change_done"),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT})
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
