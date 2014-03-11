from microsip_api.models import ConexionDB
from django.db import models

class DatabaseSucursal(models.Model):  
    name = models.CharField(max_length=100)
    empresa_conexion = models.CharField(max_length=200)
    sucursal_conexion = models.CharField(max_length=200)
    sucursal_conexion_name = models.CharField(max_length=200)
    
    def __str__(self):  
          return self.name    
          
    class Meta:
        app_label =u'auth'