#encoding:utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from datetime import datetime
# user autentication
from django.contrib.auth.decorators import login_required
from microsip_consolidador.libs.models import DatabaseSucursal
from microsip_api.comun.sic_db import get_conecctionname, get_existencias_articulo

def get_existencia_sucursales_by_articulo_id(articulo_id, connection_name):
    bases_datos_sucursales = DatabaseSucursal.objects.filter(empresa_conexion=connection_name)
    existencias = {}

    existencias['MATRIZ'] = get_existencias_articulo(
            articulo_id = articulo_id, 
            connection_name = connection_name, 
            fecha_inicio = datetime.now().strftime( "01/01/%Y" ),
            almacen = 'CONSOLIDADO', 
        )

    for base_datos in bases_datos_sucursales:
        existencias[base_datos.name] = get_existencias_articulo(
                articulo_id = articulo_id, 
                connection_name = base_datos.sucursal_conexion, 
                fecha_inicio = datetime.now().strftime( "01/01/%Y" ),
                almacen = 'CONSOLIDADO', 
                )

    return existencias

@login_required( login_url = '/login/' )
def index( request ):
    
    
    return render_to_response( 'main/index.html',{}, context_instance = RequestContext( request ) )
