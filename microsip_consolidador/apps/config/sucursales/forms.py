#encoding:utf-8
from django import forms

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
import fdb, os
from .models import *
from microsip_consolidador.settings.common import MICROSIP_DATABASES

class DatabaseSucursalForm(forms.ModelForm):    
     class Meta:
        model = DatabaseSucursal
        exclude = ('empresa_conexion','sucursal_conexion_name',)

     def __init__(self,*args,**kwargs):
        bases_de_datos = MICROSIP_DATABASES.keys()
        empresas = []
        for database_conexion in bases_de_datos:
            try:
                database_conexion = u'%s'%database_conexion
            except UnicodeDecodeError:
                pass
            else:
                
                conexion_id, empresa = database_conexion.split('-')
                conexion = ConexionDB.objects.get(pk=int(conexion_id))
                database_conexion_name = "%s-%s"%(conexion.nombre, empresa)

                empresa_option = [database_conexion, database_conexion_name]
                empresas.append(empresa_option)
                    
        super(DatabaseSucursalForm,self).__init__(*args,**kwargs)
        self.fields['sucursal_conexion'] = forms.ChoiceField(choices= empresas)
