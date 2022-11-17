from django.shortcuts import render, redirect
from django.template import loader
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login, authenticate, logout
from django.http import HttpResponse
from .models import Equipo, Tipo, ClienteRegistraEquipo, ClienteGeneraScript
from netmiko import ConnectHandler


def index(request):
    context = {}
    template = loader.get_template('app/index.html')

    return render(request, 'app/index.html', context)


# ingreso
def login(request):
    if request.method == 'GET':
        return render(request, 'app/login.html')
    else:
        print(request.POST)
        if 'passwd_2' in request.POST:

            if request.POST['passwd_1'] != request.POST['passwd_2']:
                return render(request, 'app/login.html', {
                    'Error': 'Las contraseñas no coinciden'
                })
            else:
                try:
                    user = User.objects.create_user(
                        username=request.POST['Usuario'],
                        email=request.POST['Email'],
                        password=request.POST['passwd_1']
                    )
                    user.save()
                    auth_login(request, user)
                    return redirect('login')
                except Exception as ex:
                    return render(request, 'app/login.html', {
                        'Error': 'El usuario ya existe',

                    })
        else:
            print(request.POST)
            user_auth = authenticate(request,
                                     username=request.POST['Usuario'],
                                     password=request.POST['passwd_1']
                                     )
            if user_auth is None:
                return render(request, 'app/login.html', {
                    'Error_login': 'Usuario o Contraseña incorrectos'
                })
            else:
                print(user_auth)
                auth_login(request, user_auth)
                return redirect('index')


def logout_user(request):
    logout(request)
    print(request)
    return redirect('login')


# gestion de configuraciones
def registo_equipo(request):
    if request.method == 'GET':
        return render(request, 'app/form_wizards.html', {
            'confirm_equipo': True
        })
    else:
        if 'Serial' in request.POST:
            try:
                print(request.POST)

                equipo = Equipo.objects.create(
                    serial_equipo=request.POST['Serial'],
                    modelo=request.POST['Modelo'],
                    marca=request.POST['Marca'],
                    tipo=Tipo.objects.get(id=int(request.POST['Tipo'])),
                    area=request.POST['Area'],
                    piso=request.POST['Piso']

                )
                equipo.save()
                equipo_enviar = Equipo.objects.filter(serial_equipo=request.POST['Serial']).values()
                user_client = User.objects.filter(username=request.user).values()
                tipo_equipo = Tipo.objects.filter(id=int(request.POST['Tipo'])).values()

                print(user_client)

                cliente_registra_equipo = ClienteRegistraEquipo.objects.create(
                    Equipo=Equipo.objects.get(serial_equipo=request.POST['Serial']),
                    user=User.objects.get(id=int(user_client[0]['id']))

                )
                cliente_registra_equipo.save()

                return render(request, 'app/form_wizards.html', {
                    'modelo': equipo_enviar[0]['modelo'],
                    'marca': equipo_enviar[0]['marca'],
                    'tipo': tipo_equipo[0]['nombre'],
                    'area': equipo_enviar[0]['area'],
                    'piso': equipo_enviar[0]['piso'],
                    'equipo_serial': request.POST['Serial'],
                    'confirm_equipo': True
                })
            except Exception as ex:
                return render(request, 'app/form_wizards.html', {
                    'error_registro': 'Error!! serial ya esta registrado en el sistema',
                    'confirm_equipo': None
                })

        else:
            try:
                print(1)
                print(request.POST)
                equipo_enviar = Equipo.objects.filter(serial_equipo=request.POST['eq_serial']).values()
                print(equipo_enviar)
                tipo_equipo = Tipo.objects.filter(id=int(equipo_enviar[0]['tipo_id'])).values()
                device = {
                    'device_type': equipo_enviar[0]['marca'],
                    'ip': request.POST['ip'],
                    'username': request.POST['Usuario'],
                    'password': request.POST['passwd'],
                }
                conn = ConnectHandler(**device)
                output = conn.send_command('show version | i uptime')
                print(output)
                return render(request, 'app/form_upload.html', {
                    'confirm_equipo': True,
                    'verifcar_equipo': True,
                    'equipo_serial': request.POST['eq_serial'],
                })
            except Exception as ex:
                print(ex)
                return render(request, 'app/form_wizards.html', {
                    'error_validar': ex,
                    'confirm_equipo': True,
                    'verifcar_equipo': None,
                    'modelo': equipo_enviar[0]['modelo'],
                    'marca': equipo_enviar[0]['marca'],
                    'tipo': tipo_equipo[0]['nombre'],
                    'area': equipo_enviar[0]['area'],
                    'piso': equipo_enviar[0]['piso'],
                    'equipo_serial': equipo_enviar[0]['serial_equipo'],
                })

def cargar_archivo(request):
    print(request.FILE['file'])
    return render(request, 'app/form_upload.html')


def gentella_html(request):
    context = {}
    # The template to be loaded as per gentelella.
    # All resource paths for gentelella end in .html.

    # Pick out the html file name from the url. And load that template.
    load_template = request.path.split('/')[-1]
    template = loader.get_template('app/' + load_template)
    return HttpResponse(template.render(context, request))
