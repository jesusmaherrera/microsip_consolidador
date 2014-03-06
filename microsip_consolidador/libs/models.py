#encoding:utf-8
from django.db import models
from django.db import router
from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.sessions.models import Session
from microsip_api.comun.sic_db import next_id, first_or_none
import django.dispatch

articulo_clave_save_signal = django.dispatch.Signal()
from microsip_api.apps.config.models import Usuario
from microsip_api.models_base.comun.articulos import *
from microsip_api.models_base.comun.clientes import *
from microsip_api.models_base.comun.otros import *
from microsip_api.models_base.comun.listas import *
from microsip_api.models_base.configuracion.folios_fiscales import *
from microsip_api.models_base.configuracion.preferencias import *
from microsip_api.models_base.ventas.documentos import *

class Registry(RegistryBase):
    def __unicode__(self):
        return u'%s' % self.nombre
    
    def get_value(self):
        if self.valor == '':
            return None
        return u"%s"%self.valor
    def get_valor_blob(self):
        valor_blob= self.valor_blob
        objects.asd
        return u"%s"%self.valor_blob

class Pais(PaisBase):
    def save(self, *args, **kwargs):    
        using = kwargs.get('using', None)
        using = using or router.db_for_write(self.__class__, instance=self)
        
        if self.id == None:
            self.id = next_id('ID_CATALOGOS', using)  

        if self.es_predet == 'S':
            Pais.objects.using(using).all().exclude(pk=self.id).update(es_predet='N')

        super(self.__class__, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'%s' % self.nombre

class Estado(EstadoBase):
    
    def save(self, *args, **kwargs):
        using = kwargs.get('using', None)
        using = using or router.db_for_write(self.__class__, instance=self)
            
        if self.id == None:
            self.id = next_id('ID_CATALOGOS', using)  
        
        if self.es_predet == 'S':
            Estado.objects.using(using).all().exclude(pk=self.id).update(es_predet='N')

        super(self.__class__, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'%s, %s' % (self.nombre, self.pais)

class Ciudad(CiudadBase):
    def save(self, *args, **kwargs):
        using = kwargs.get('using', None)
        using = using or router.db_for_write(self.__class__, instance=self)
            
        if self.id == None:
            self.id = next_id('ID_CATALOGOS', using)  

        if self.es_predet == 'S':
            Ciudad.objects.using(using).all().exclude(pk=self.id).update(es_predet='N')

        super(self.__class__, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'%s, %s'%(self.nombre, self.estado)

class Moneda(MonedaBase):
    def __unicode__(self):
        return u'%s' % self.nombre

class Almacen(AlmacenBase):
    def __unicode__(self):
        return self.nombre

class PrecioEmpresa(PrecioEmpresaBase):
    def __unicode__(self):
        return u'%s' % self.nombre

class GrupoLineas(GrupoLineasBase):
    def save(self, *args, **kwargs):    
        using = kwargs.get('using', None)
        using = using or router.db_for_write(self.__class__, instance=self)

        if self.id == None:
            self.id = next_id('ID_CATALOGOS', using)  
       
        super(self.__class__, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'%s' % self.nombre

class LineaArticulos(LineaArticulosBase):
    def save(self, *args, **kwargs):    
        using = kwargs.get('using', None)
        using = using or router.db_for_write(self.__class__, instance=self)

        if self.id == None:
            self.id = next_id('ID_CATALOGOS', using)  
        super(self.__class__, self).save(*args, **kwargs)
        
    def __unicode__(self):
        return u'%s' % self.nombre

class Articulo(ArticuloBase):
    def save(self, *args, **kwargs):    
        using = kwargs.get('using', None)
        using = using or router.db_for_write(self.__class__, instance=self)

        if self.id == None:
            self.id = next_id('ID_CATALOGOS', using)  
       
        super(self.__class__, self).save(*args, **kwargs)
        
    def __unicode__( self) :
        return u'%s (%s)' % ( self.nombre, self.unidad_venta )

class ArticuloPrecio(ArticuloPrecioBase):
    def __unicode__(self):
        return u'%s' % self.id

class ArticuloClaveRol(ArticuloClaveRolBase):
    def __unicode__(self):
        return u'%s' % self.nombre

class ArticuloClave(ArticuloClaveBase):
    def save_send_signal(self, *args, **kwargs):
        articulo_clave_save_signal.send(sender=self, *args, **kwargs)

    def save(self, *args, **kwargs):    
        using = kwargs.get('using', None)
        using = using or router.db_for_write(self.__class__, instance=self)
        if self.id == None:
            self.id = next_id('ID_CATALOGOS', using)  
       
        super(self.__class__, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'%s' % self.clave
                
#clientes

class ClienteTipo(ClienteTipoBase):
    def __unicode__( self ):
        return self.nombre

class CondicionPago(CondicionPagoBase):
    def save(self, *args, **kwargs):    
        using = kwargs.get('using', None)
        using = using or router.db_for_write(self.__class__, instance=self)

        if not self.id:
            self.id = next_id('ID_CATALOGOS', using)
        
        if self.es_predet == 'S':
            CondicionPago.objects.using(using).all().exclude(pk=self.id).update(es_predet='N')

        super(self.__class__, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.nombre

class CondicionPagoPlazo(CondicionPagoPlazoBase):
    def save(self, *args, **kwargs):    
        if not self.id:
            using = kwargs.get('using', None)
            using = using or router.db_for_write(self.__class__, instance=self)
            self.id = next_id('ID_CATALOGOS', using)

        super(self.__class__, self).save(*args, **kwargs)

class Cliente(ClienteBase):
    def save(self, *args, **kwargs):    
        using = kwargs.get('using', None)
        using = using or router.db_for_write(self.__class__, instance=self)

        if self.id == None:
            self.id = next_id('ID_CATALOGOS', using)  

        super(self.__class__, self).save(*args, **kwargs)

    def __unicode__( self ):
        return self.nombre

class ClienteClaveRol(ClienteClaveRolBase):
    pass

class ClienteClave(ClienteClaveBase):
    def __unicode__(self):
        return self.clave

class ClienteDireccion(ClienteDireccionBase):
    def save(self, *args, **kwargs):    
        using = kwargs.get('using', None)
        using = using or router.db_for_write(self.__class__, instance=self)

        if self.id == None:
            self.id = next_id('ID_CATALOGOS', using)  
            
        super(self.__class__, self).save(*args, **kwargs)

#listas
class ImpuestoTipo(ImpuestoTipoBase):
    def __unicode__(self):
        return u'%s' % self.nombre

class Impuesto(ImpuestoBase):
    def save(self, *args, **kwargs):    
        using = kwargs.get('using', None)
        using = using or router.db_for_write(self.__class__, instance=self)

        if self.id == None:
            self.id = next_id('ID_CATALOGOS', using)  
        
        if self.es_predet == 'S':
            Impuesto.objects.using(using).all().exclude(pk=self.id).update(es_predet='N')

        super(self.__class__, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.nombre
    
class ImpuestosArticulo(ImpuestoArticuloBase):
    def save(self, *args, **kwargs):    
        using = kwargs.get('using', None)
        using = using or router.db_for_write(self.__class__, instance=self)

        if self.id == None:
            self.id = next_id('ID_CATALOGOS', using)  
       
        super(self.__class__, self).save(*args, **kwargs)
        
    def __unicode__(self):
        return self.impuesto

@receiver(post_save)
def clear_cache(sender, **kwargs):
    if sender != Session:
        cache.clear()

class ConexionDB(models.Model):  
    nombre = models.CharField(max_length=100)
    TIPOS = (('L', 'Local'),('R', 'Remota'),)
    tipo = models.CharField(max_length=1, choices=TIPOS)
    servidor = models.CharField(max_length=250)
    carpeta_datos = models.CharField(max_length=300)
    usuario = models.CharField(max_length=300)
    password = models.CharField(max_length=300)

    def __str__(self):  
          return self.nombre    
          
    class Meta:
        app_label =u'auth' 

class DatabaseSucursal(models.Model):  
    name = models.CharField(max_length=100)
    empresa_conexion = models.CharField(max_length=200)
    sucursal_conexion = models.CharField(max_length=200)
    sucursal_conexion_name = models.CharField(max_length=200)
    
    def __str__(self):  
          return self.name    
          
    class Meta:
        app_label =u'auth'

class AplicationPlugin(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    
    def __unicode__(self):
        return u'%s' % self.nombre

    class Meta:
        app_label =u'auth'
        db_table = u'sic_aplicationplugin'

#####################################################
##
##                         VENTAS
##
##
#####################################################
class Vendedor(VendedorBase):
    def __unicode__(self):
        return self.nombre
        
class ViaEmbarque(ViaEmbarqueBase):
   pass

class FolioVenta(FolioVentaBase):
    def __unicode__(self):
        return u'%s'%self.id
        
class FolioFiscal(ConfiguracionFolioFiscalBase): 
    def __str__(self):  
          return u'%s' % self.id
    def save(self, *args, **kwargs):
        if not self.id:
            using = kwargs.get('using', None)
            using = using or router.db_for_write(self.__class__, instance=self)
            self.id = next_id('ID_DOCTOS', using)

        super(self.__class__, self).save(*args, **kwargs)

class UsoFoliosFiscales(ConfiguracionFolioFiscalUsoBase):
    def __str__(self):  
          return u'%s' % self.id    
          
    def save(self, *args, **kwargs):
        
        if self.id == -1:
            using = kwargs.get('using', None)
            using = using or router.db_for_write(self.__class__, instance=self)
            self.id = next_id('ID_DOCTOS', using)

        super(self.__class__, self).save(*args, **kwargs)

class VentasDocumento(VentasDocumentoBase):

    def __unicode__( self ):
        return u'%s'% self.folio
    
    def next_folio( self, connection_name=None, **kwargs ):
        ''' Funcion para generar el siguiente folio de un documento de ventas '''

        #Parametros opcionales
        serie = kwargs.get('serie', None)
        consecutivos_folios = FolioVenta.objects.using(connection_name).filter(tipo_doc = self.tipo, modalidad_facturacion = self.modalidad_facturacion)
        if serie:
            consecutivos_folios = consecutivos_folios.filter(serie=serie)

        consecutivo_row = first_or_none(consecutivos_folios)
        consecutivo = ''
        if consecutivo_row:
            consecutivo = consecutivo_row.consecutivo 
            serie = consecutivo_row.serie
            if serie == u'@':
                serie = ''

        folio = '%s%s'% (serie,("%09d" % int(consecutivo))[len(serie):]) 

        consecutivo_row.consecutivo = consecutivo_row.consecutivo + 1
        consecutivo_row.save(using=connection_name)

        return folio, consecutivo


    def save(self, *args, **kwargs):
        
        if not self.id:
            using = kwargs.get('using', None)
            using = using or router.db_for_write(self.__class__, instance=self)
            self.id = next_id('ID_DOCTOS', using)
            consecutivo = ''
            #Si no se define folio se asigna uno
            if self.folio == '':
                self.folio, consecutivo = self.next_folio(connection_name=using)

            #si es factura 
            if consecutivo != '' and self.tipo == 'F' and self.modalidad_facturacion == 'CFDI':
                folios_fiscales = first_or_none(FolioFiscal.objects.using(using).filter(modalidad_facturacion=self.modalidad_facturacion))
                if not folios_fiscales:
                    FolioFiscal.objects.using(using).create(
                            serie = '@',
                            folio_ini = 1,
                            folio_fin = 999999999,
                            ultimo_utilizado = 0,
                            num_aprobacion ="1",
                            ano_aprobacion = 1,
                            modalidad_facturacion = self.modalidad_facturacion,
                        )
                    folios_fiscales = first_or_none(FolioFiscal.objects.using(using).filter(modalidad_facturacion=self.modalidad_facturacion))

                if folios_fiscales:
                    UsoFoliosFiscales.objects.using(using).create(
                            id= -1,
                            folios_fiscales = folios_fiscales,
                            folio= consecutivo,
                            fecha = datetime.now(),
                            sistema = self.sistema_origen,
                            documento = self.id,
                            xml = '',
                        )

        super(self.__class__, self).save(*args, **kwargs)

class VentasDocumentoVencimiento(VentasDocumentoVencimientoBase):
    pass

class VentasDocumentoDetalle(VentasDocumentoDetalleBase):
    def __unicode__(self):
        return u'%s(%s)'% (self.id, self.documento_pv)
    
    def save(self, *args, **kwargs):
        
        if not self.id:
            using = kwargs.get('using', None)
            using = using or router.db_for_write(self.__class__, instance=self)
            self.id = next_id('ID_DOCTOS', using)

        super(self.__class__, self).save(*args, **kwargs)