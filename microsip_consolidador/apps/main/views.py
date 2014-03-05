
 #encoding:utf-8
from django.shortcuts import render_to_response, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext

# user autentication
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, AdminPasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.core import management
from .forms import *

@login_required( login_url = '/login/' )
def conexiones_View( request, template_name = 'main/conexiones/conexiones.html' ):
    """ Lista de conexiones a carpetas ( Microsip Datos ). """

    c = { 'conexiones' : ConexionDB.objects.all() }
    return render_to_response( template_name, c, context_instance = RequestContext( request ) )

@login_required(login_url='/login/')
def conexion_manageView( request, id = None, template_name = 'main/conexiones/conexion.html' ):
    """ Lista de conexiones """

    message = ''
    initial_form = None
    if id:
        conexion = get_object_or_404( ConexionDB, pk = id)
    else:
        conexion =  ConexionDB()
        initial_form = {
        'nombre':'local',
        'tipo':'L',
        'servidor':'localhost',
        'carpeta_datos':'C:\Microsip datos',
        'usuario':'SYSDBA'
        }

    form = ConexionManageForm( request.POST or None, instance=conexion, initial=initial_form)
    
    if form.is_valid():
        grupo = form.save()
        return HttpResponseRedirect( '/conexiones/' )

    c = { 'form' : form, }
    return render_to_response( template_name, c, context_instance = RequestContext( request ) )
    

@login_required( login_url = '/login/' )
def index( request ):
    return render_to_response( 'main/index.html',{}, context_instance = RequestContext( request ) )

@login_required(login_url='/login/')
def select_db(request, template_name='main/select_db.html'):
    ''' Para seleccionar base de datos con la que se desea trabjar '''

    form = SelectDBForm(request.POST or None, usuario= request.user, conexion_activa = request.session['conexion_activa'])
    message = ''
    conexion_activa = request.session['conexion_activa']
    
    if form.is_valid():
        conexion = form.cleaned_data['conexion'].replace(' ','_')
        request.session['selected_database'] = conexion

        return HttpResponseRedirect('/')
        call_command('runserver')
    else:
        request.session['selected_database'] = ''
    
    c =  {'form':form, 'message':message,}
    return render_to_response(template_name, c, context_instance=RequestContext(request))

def ingresar(request):
    ''' logea un usuario '''

    message = ''
    formulario = CustomAuthenticationForm(request.POST or None)
    
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')

    if formulario.is_valid():
        usuario = authenticate(username=request.POST['username'], password=request.POST['password'])
        
        if usuario.is_active:
            login(request, usuario)
            conexion_db = request.POST['conexion_db']
            request.session['conexion_activa'] = ''
            if conexion_db != '':
                request.session['conexion_activa'] = int(conexion_db)

            return HttpResponseRedirect('/select_db/')
        else:
            return render_to_response('noactivo.html', context_instance=RequestContext(request))

    return render_to_response('main/login.html',{'form':formulario, 'message':message,}, context_instance=RequestContext(request))

def logoutUser(request):
    ''' Deslogea un usuario '''
    
    try:
        del request.session['selected_database']
        del request.session['conexion_activa']
    except KeyError:
        pass
    
    logout(request)
    return HttpResponseRedirect('/')
