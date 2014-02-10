# -*- encoding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout_then_login

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('academicos.core.views',
    # Examples:
    # url(r'^$', 'academicos.views.home', name='home'),
    # url(r'^academicos/', include('academicos.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'homepage', name="homepage"),
    url(r'^register/$', 'register', name="register"),
    url(r'^register/(\d+)/$', 'detail', name="detail"),
    url(r'^detail/$', 'detail', name="detail"),
    url(r'^student_register/$','student_register', name = 'student_register'),
    #url(r'^bemvindo/$', 'bemvindo', name = 'bemvindo'),Tirei vamos usar a / no lugar de /bemvindo. Acho que fica mais organizado Deixar tudo em inglês... kkkkk
    url(r'^login/',login,{"template_name":"login.html"}),#Agora na versão 1.5.1 tenho que usar o import do caminho para chamá-lo pelo atalho no caso login. Logo login== django.contrib.auth.login    
    url(r'^logout/',logout_then_login,{"login_url":"/login/"}),#Mesma coisa da de cima
    url(r'^teacher_register/$', 'teacher_register', name='teacher_register'),
    url(r'^class_register/$', 'class_register', name='class_register'),
    url(r'^grade_register/$', 'grade_register', name='grade_register'),
    url(r'^matriculation_register/$', 'matriculation_register', name='matriculation_register'),
    url(r'^disciplina_register/$','disciplina_register',name='disciplina_register'),
    url(r'^lista_disciplina_aluno/$','lista_disciplina_aluno', name='lista_disciplina_aluno'),
    url(r'^menu_aluno/$','menu_aluno',name='menu_aluno'),
    url(r'^disciplina/(\d+)/$','disciplina',name='disciplina'),    
    url(r'^menu_professor/$','menu_professor',name='menu_professor'),
    url(r'^lista_disciplina_professor/$','lista_disciplina_professor',name='lista_disciplina_professor'),
    url(r'^disciplina_alterar/(\d+)/$','disciplina_alterar',name='disciplina_alterar'),
)

from django.conf import settings
urlpatterns += patterns('django.views.static',
url(r'^static/(?P<path>.*)$', 'serve',
{'document_root': settings.STATIC_ROOT}),
)
