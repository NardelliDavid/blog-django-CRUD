"""
URL configuration for blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from blog_app import views
# Para imagenes
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"), # Inicio
    # URLS de inicio de sesion
    path('login_vista/', views.login_vista, name="login_vista"),
    path('login/', views.login, name="login"),
    # URLS de registro de usuario
    path('register/', views.register, name="register"), # Pagina de registro de usuario
    path('recibir_registro/', views.recibir_registro, name="recibir_registro"),
    # URL para cerrar sesion
    path('cerrar_sesion/', views.cerrar_sesion, name="cerrar_sesion"),
    # URLS de los posts
    path('crear_post/', views.crear_post, name="crear_post"), # Pagina con el formulario para crear publicaciones
    path('recibir_post/', views.recibir_post, name="recibir_post"), # Recibe los datos del formulario para crear el post
    # URL de la config de la cuenta
    path('mi_cuenta_vista/', views.mi_cuenta_vista, name="mi_cuenta_vista"),
    path('administrar_posts/', views.administrar_posts, name="administrar_posts"), # Muestra las publicaciones del usuario
    path('editar_post/<int:post_id>/', views.editar_post, name="editar_post"),
    path('borrar_post/<int:post_id>/', views.borrar_post, name="borrar_post"),
    path('guardar_publicacion/<int:post_id>/', views.guardar_publicacion, name="guardar_publicacion"),# URL para guardar una publicacion
    path('cambiar_password/', views.cambiar_password, name="cambiar_password"), # URL para cambiar la contraseña
    path('cambiar_nombre/', views.cambiar_nombre, name="cambiar_nombre"), # URL para cambiar el nombre
    path('mis_guardados/', views.mis_guardados, name="mis_guardados"), # Pagina de guardados
    path('borrar_cuenta/', views.borrar_cuenta, name="borrar_cuenta"),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)