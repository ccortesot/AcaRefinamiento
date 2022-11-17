from django.urls import path, re_path
from app import views

urlpatterns = [
    # Matches any html file - to be used for gentella
    # Avoid using your .html in your resources.
    # Or create a separate django app.
    re_path(r'^.*\.html', views.gentella_html, name='gentella'),

    # The login page
    path('', views.login, name='login'),
    # The index page
    path('index/', views.index, name='index'),
    path('logout/', views.logout_user, name='logout_user'),
    path('registrar/equipo/', views.registo_equipo, name='registar_equipo'),
    path('upload/', views.cargar_archivo, name='upload')
]
