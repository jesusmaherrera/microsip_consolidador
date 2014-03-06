#encoding:utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from datetime import datetime
# user autentication
from django.contrib.auth.decorators import login_required
from microsip_consolidador.libs.models import DatabaseSucursal, Articulo, ArticuloClave
from microsip_api.comun.sic_db import get_conecctionname, get_existencias_articulo, first_or_none

def get_existencia_sucursales_by_articulo_id(clave, connection_name):
    bases_datos_sucursales = DatabaseSucursal.objects.filter(empresa_conexion=connection_name)
    existencias = {}
    articulo_clave = first_or_none(ArticuloClave.objects.filter(clave=clave))
    articulo_nombre = ''
    if articulo_clave:
        articulo = articulo_clave.articulo
        articulo_nombre = articulo.nombre
        existencias['MATRIZ'] = get_existencias_articulo(
                articulo_id = articulo.id, 
                connection_name = connection_name, 
                fecha_inicio = datetime.now().strftime( "01/01/%Y" ),
                almacen = 'CONSOLIDADO', 
            )

    
    for base_datos in bases_datos_sucursales:
        articulo_clave = first_or_none(ArticuloClave.objects.using(base_datos.sucursal_conexion).filter(clave=clave))
        if articulo_clave:
            articulo = articulo_clave.articulo
            if not articulo_nombre:
                articulo_nombre = articulo.nombre
            existencias[base_datos.name] = get_existencias_articulo(
                    articulo_id = articulo.id, 
                    connection_name = base_datos.sucursal_conexion, 
                    fecha_inicio = datetime.now().strftime( "01/01/%Y" ),
                    almacen = 'CONSOLIDADO', 
                    )

    return {'existencias':existencias,'articulo_nombre':articulo_nombre,}

@login_required( login_url = '/login/' )
def articulo_consolidado_view( request, clave, template_name='common/articulos/articulo_consoliado.html'):
    connection_name = get_conecctionname(request.session)
    resultado_existencias  = get_existencia_sucursales_by_articulo_id(clave, connection_name)


    c= { 'existencias':resultado_existencias['existencias'], 'articulo_nombre':resultado_existencias['articulo_nombre'], }
    
    return render_to_response( template_name, c, context_instance = RequestContext( request ) )
