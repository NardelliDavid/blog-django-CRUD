from django.contrib import admin
from blog_app.models import *

class UsuariosAdmin(admin.ModelAdmin):
    list_display=("id", "nombre", "password")
admin.site.register(Usuarios, UsuariosAdmin)

class PublicacionesAdmin(admin.ModelAdmin):
    list_display=("id", "id_usuario_creador", "nombre_usuario_creador", "contenido", "imagen", "creado", "actualizado")
admin.site.register(Publicaciones, PublicacionesAdmin)

class GuardadosAdmin(admin.ModelAdmin):
    list_display=("id", "usuario", "publicacion", "fecha_guardado")
admin.site.register(Guardados, GuardadosAdmin)