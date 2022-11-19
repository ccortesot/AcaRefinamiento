# AcaRefinamiento

### Funcionalidad

-	Hasta la fecha, la aplicación registra los equipos soportados por netmiko, próximas actualizaciones se agrega las demás funcionalidades descritas en trabajo anteriores
-	Registra usuarios desde la interface web, los administradores desde la consola de python3.11 comando (python3.11 manage.py createsuperuser) y seguir los pasos indicados
-	Ingreso a la aplicación, separando las funcionalidades del cliente, las de administrador 


Clonar repositorio
-------------
git clone https://github.com/ccortesot/AcaRefinamiento.git

###Linux

cd gentelella/

###Windows

dir gentelella/

Instalar entorno virtual
-------------
Abren la terminal en linux o cmd en windows desde la ruta del proyecto .

python -m venv env 

Activar entorno virtual
-------------

###Linux
source env/bin/activate

###Windows
env\Scripts\activate.bat

Instalar módulos en el entorno virtual
-------------

pip install -r  requeriments.txt 

Ejecutar servidor Django
-------------

python manage.py runserver 0.0.0.0:8000


Ejecutar migración  base de datos
-------------
python manage.py makemigrations app
python manage.py  migrate app

Crear usuario administración
-------------
python manage.py createsuperuser



###End
