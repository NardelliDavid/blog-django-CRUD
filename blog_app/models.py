from django.db import models
from django.contrib.auth.hashers import make_password
import os

class Usuarios(models.Model):
    nombre = models.CharField(max_length=50)
    password = models.CharField(max_length=128)

    def save(self, *args, **kwargs):
        # Cifrar la contraseña antes de guardar
        if self.password:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

class Publicaciones(models.Model):
    id_usuario_creador = models.ForeignKey(Usuarios, on_delete=models.CASCADE, related_name='publicaciones')
    nombre_usuario_creador = models.CharField(max_length=50, null=True)
    contenido = models.TextField()
    imagen = models.ImageField(upload_to='imagenesPublicaciones', blank=True, null=True)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    def delete(self, *args, **kwargs):
        if self.imagen:
            # Elimina la imagen del sistema de archivos
            if os.path.isfile(self.imagen.path):
                os.remove(self.imagen.path)
        super().delete(*args, **kwargs)

class Guardados(models.Model):
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE, related_name='guardados')
    publicacion = models.ForeignKey(Publicaciones, on_delete=models.CASCADE, related_name='guardados')
    fecha_guardado = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'publicacion')  # Evita guardar la misma publicación más de una vez