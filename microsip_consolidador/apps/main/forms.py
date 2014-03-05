#encoding:utf-8
from django import forms

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from microsip_consolidador.settings.common import RUTA_PROYECTO
import fdb
from .models import *

class ConexionManageForm(forms.ModelForm):
    password =  forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = ConexionDB

class CustomAuthenticationForm(forms.Form):
    conexion_db = forms.ModelChoiceField(ConexionDB.objects.all(), required= False)
    username = forms.CharField( max_length=150, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Nombre de usuario de microsip'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder': 'Password'} ))
    conexion_db.widget.attrs['class'] = 'form-control'
    
    def clean(self):
        cleaned_data = self.cleaned_data
        conexion_db = cleaned_data.get("conexion_db")
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if conexion_db == None and username != 'SYSDBA':
            raise forms.ValidationError(u'Por favor selecciona una conexion')
        #Si se seleciona una conexion comprueba usuario y password de firebird
        else:
            try:
                db = fdb.connect(host='localhost', user=username ,password=str(password) , database= RUTA_PROYECTO + "data\LOGIN.FDB")
            except fdb.DatabaseError:
               raise forms.ValidationError(u'nombre de usuario o password invalidos')

            if conexion_db:
                try:
                    db = fdb.connect(host=conexion_db.servidor ,user=conexion_db.usuario ,password=conexion_db.password , database="%s\System\CONFIG.FDB"% conexion_db.carpeta_datos)
                except fdb.DatabaseError:
                   raise forms.ValidationError(u'Error en la conexion selecionada')
                
            #Crea o modifica usuario                   
            try:
                usuario = User.objects.get(username__exact=username)
            except ObjectDoesNotExist:
                usuario = User.objects.create_user(username = username, password=str(password))
                if username == 'SYSDBA':
                    User.objects.filter(username = 'SYSDBA').update(is_superuser=True, is_staff=True)
            else:
                usuario.set_password(str(password))
                usuario.save()
            
            #Se crea o se modifica perfil de usuario con conexion                
            # user_profile = UserProfile.objects.filter(usuario = usuario)
            # if conexion_db:
            #     if user_profile.exists():
            #         user_profile.update(conexion_activa = conexion_db, basedatos_activa='')
            #     else:
            #         UserProfile.objects.create(usuario= usuario, basedatos_activa='', conexion_activa= conexion_db)
            # elif usuario.username == 'SYSDBA' and not user_profile.exists():
            #     UserProfile.objects.create(usuario= usuario, basedatos_activa='', conexion_activa=None)


        return cleaned_data

class SelectDBForm(forms.Form):    
     def __init__(self,*args,**kwargs):
        usuario = kwargs.pop('usuario')
        conexion_activa = kwargs.pop('conexion_activa')
        empresas = []
        if conexion_activa != '':
            conexion_activa = ConexionDB.objects.get(pk=conexion_activa)
        else:
            conexion_activa = None

        if conexion_activa:
            acceso_empresas = ''
            try:
                acceso_empresas = Usuario.objects.get(nombre__exact=usuario.username).acceso_empresas
            except ObjectDoesNotExist:
                if usuario.username == 'SYSDBA':
                    acceso_empresas = 'T'            
            consulta = ''

            # T: Acceso total L: Acceso solo a determinadas empresas
            if acceso_empresas == 'T':
                consulta = u"SELECT EMPRESAS.nombre_corto FROM EMPRESAS"
            elif acceso_empresas == 'L':
                consulta = u"SELECT EMPRESAS.nombre_corto FROM EMPRESAS_USUARIOS, EMPRESAS, USUARIOS WHERE USUARIOS.usuario_id = empresas_usuarios.usuario_id AND EMPRESAS.empresa_id = empresas_usuarios.empresa_id AND usuarios.nombre = '%s'"% usuario
            
            db= fdb.connect(host=conexion_activa.servidor, user= conexion_activa.usuario, password=conexion_activa.password, database="%s\System\CONFIG.FDB"%conexion_activa.carpeta_datos)
            cur = db.cursor()
            cur.execute(consulta)
            empresas_rows = cur.fetchall()
            for empresa in empresas_rows:
                try:
                    empresa = u'%s'%empresa[0]
                except UnicodeDecodeError:
                    pass
                else:
                    empresa_option = [empresa, empresa]
                    empresas.append(empresa_option)
                    
        super(SelectDBForm,self).__init__(*args,**kwargs)
        self.fields['conexion'] = forms.ChoiceField(choices= empresas)