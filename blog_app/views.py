from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import *
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist

def index(request):
    # Obtiene las publicaciones en la base de datos
    posts = Publicaciones.objects.all().order_by('-creado')
    # Verifica si existen datos de sesion
    if 'usuario' in request.session:
        # Si hay usuario pasa los datos del mismo junto con las publicaciones
        usuario = request.session['usuario']
        return render(request, "blog_app/index.html", {"posts": posts, "usuario": usuario})
    else:
        # Si no hay usuario en la sesion envia solo las publicaciones
        return render(request, "blog_app/index.html", {"posts": posts})


# Pagina de Login
def login_vista(request):
    if 'usuario' in request.session:
        # Si existe usuario en la sesion redirige al index
        return redirect('index')
    else:
        # Si no existe continua normalmente
        return render(request, "blog_app/usuarios/login.html")
# Vista para recibir los datos del login
def login(request):
    if request.method == 'POST':
        nombre = request.POST['nombre'].strip()
        password = request.POST['password'].strip()
        
        try:
            usuario = Usuarios.objects.get(nombre=nombre)  # Intenta obtener el usuario
            # Verifica la contraseña
            if check_password(password, usuario.password):  # Verifica la contraseña cifrada
                id_usuario = usuario.id  # Obtiene el id del usuario
                request.session['usuario'] = {
                    'id': id_usuario,
                    'nombre': nombre,
                }
                return redirect('index')
            else:
                # Si la contraseña es incorrecta
                error = "Nombre de usuario o contraseña incorrectos."
                return render(request, "blog_app/usuarios/login.html", {'error': error})
        except ObjectDoesNotExist:
            # Maneja el caso en que el usuario no existe
            error = "Nombre de usuario o contraseña incorrectos."
            return render(request, "blog_app/usuarios/login.html", {'error': error})
    else:
        return redirect('login_vista')
    
# Pagina de Registro
def register(request):
    if 'usuario' in request.session:
        # Si existe usuario en la sesion redirige al index
        return redirect('index')
    else:
        # Si no existe continua normalmente
        error_usuario = request.GET.get('error_usuario', None)
        return render(request, "blog_app/usuarios/register.html", {'error_usuario': error_usuario})
def recibir_registro(request):
    if request.method == 'POST': # Si el metodo es POST sigue
        nombre = request.POST['nombre'].strip()
        password = request.POST['password'].strip()
        # Verifica si el nombre de usuario existe en la base de datos
        if Usuarios.objects.filter(nombre=nombre).exists():
            # Si existe redirige al formulario con el nombre de usuario que ya existe
            return redirect(f"{reverse('register')}?error_usuario={nombre}")
        else: 
            # Guarda los datos en la DB
            usuario = Usuarios(nombre=nombre, password=password)
            usuario.save()
            
            id_usuario = Usuarios.objects.get(nombre=nombre).id # Solicitamos el id del usuario recien registrado
            request.session['usuario'] = {
                'id': id_usuario,
                'nombre': usuario.nombre,
            }
            return redirect('index')  # Redirige a la página principal tras el registro
    else:
        return redirect('register')  # Si no es POST, redirige al registro
    
    
# Vista para cerrar sesion
def cerrar_sesion(request):
    logout(request) # Para eliminar la sesion
    return redirect('login_vista')


# Pagina para crear posts
def crear_post(request):
    if 'usuario' in request.session:
        # Si existe usuario en la sesion deja continuar normalmente
        usuario = request.session['usuario']
        return render(request, "blog_app/posts/crear_post.html", {"usuario": usuario})
    else:
        # Si no existe usuario no dejara crear posts
        return render(request, "blog_app/posts/crear_post.html")
def recibir_post(request):
    if request.method == 'POST':
        if 'usuario' in request.session:
            # Si existe usuario en la sesion obtiene los datos
            usuario = request.session['usuario']
            # Obtiene los datos de la sesion y el formulario
            id = usuario.get('id')
            nombre = usuario.get('nombre')
            contenido = request.POST['contenido'].strip()
            img = request.FILES.get('img')
            # Si ambos estan vacios redirige al formulario
            if contenido == "" and img is None:
                # Si el contenido y la imagen estan vacios redirige de nuevo al formulario
                return redirect("crear_post")
            else:
                # Obtiene el objeto Usuario correspondiente al id
                try:
                    usuario_creador = Usuarios.objects.get(id=id)
                except Usuarios.DoesNotExist:
                    # Si no existe el usuario, redirige de vuelta o maneja el error
                    return redirect('crear_post')
                # Crea la publicación
                publicacion = Publicaciones(
                    id_usuario_creador=usuario_creador,  # Usa el objeto Usuario en lugar del id
                    nombre_usuario_creador=nombre,
                    contenido=contenido,
                    imagen=img
                )
                publicacion.save()
                # Redirige al index después de crear la publicación
                return redirect('index')
        else:
            # Si no existe usuario redirige a la pagina de login
            return redirect('login_vista')
    else:
        # Si el metodo no es POST redirige al index
        return redirect('index')
    
# Configuracion del usuario
def mi_cuenta_vista(request):
    if 'usuario' in request.session:
        usuario = request.session['usuario']
        return render(request, "blog_app/usuarios/mi_cuenta.html", {"usuario": usuario})
    else: 
        return redirect('index')
    
# Vista para administrar publicaciones
def administrar_posts(request):
    if 'usuario' in request.session:
        usuario = request.session['usuario'] # Datos del usuario en la sesion
        # Obtiene el nombre y el id del usuario guardado en la sesion
        nombre = usuario.get('nombre')
        usuario_id = usuario.get('id')
        # Consulta a para obtener las publicaciones del usuario
        posts = Publicaciones.objects.filter(id_usuario_creador=usuario_id, nombre_usuario_creador=nombre).order_by('-creado')
        return render(request, "blog_app/posts/administrar_posts.html", {"usuario": usuario, "posts": posts})
    else: 
        return redirect('index')
# Vista para editar el post
def editar_post(request, post_id):
    # Obtén el post o devuelve un 404 si no existe
    post = get_object_or_404(Publicaciones, id=post_id)
    if request.method == "POST":
        # Actualiza el contenido si está presente
        if 'contenido' in request.POST:
            post.contenido = request.POST['contenido']
        # Actualiza la imagen si está presente
        if 'img' in request.FILES:
            # Elimina la imagen anterior del sistema de archivos
            if post.imagen and os.path.isfile(post.imagen.path):
                os.remove(post.imagen.path)
            post.imagen = request.FILES['img'] # Asigna la nueva imagen
        post.save()
        return redirect('administrar_posts')
    else:
        print("GET")
        return redirect('administrar_posts')
# Vista para borrar el post
def borrar_post(request, post_id):
    if request.method == "GET":
        post = Publicaciones.objects.get(id=post_id)
        post.delete()
        return redirect("administrar_posts")
    else:
        return redirect("administrar_posts")
# Vista para guardar publicaciones
### def guardar_publicacion(request):
    if request.method == 'POST':
        usuario_id = request.POST.get('usuario_id')
        publicacion_id = request.POST.get('publicacion_id')
        
        # Verificar si la publicación ya está guardada
        guardado, creado = Guardados.objects.get_or_create(
            usuario_id=usuario_id,
            publicacion_id=publicacion_id
        )
        
        # Retornar el estado de guardado
        if creado:
            return JsonResponse({'status': 'guardado'})
        else:
            # Si ya está guardado, eliminar el guardado (función de alternancia)
            guardado.delete()
            return JsonResponse({'status': 'no_guardado'})

    return JsonResponse({'status': 'error'}, status=400)
###
# Vista para cambiar el nombre
def cambiar_nombre(request):
    if request.method == "POST":
        nombre_actual = request.session['usuario']['nombre']
        nombre_nuevo = request.POST['nombre_nuevo'].strip()
        password_actual = request.POST['password'].strip()
        
        if nombre_actual == nombre_nuevo:
            print("Los nombres son iguales")
            return redirect('mi_cuenta_vista')
        else:
            try:
                # Obtiene la fila donde esta el usuario
                usuario = Usuarios.objects.get(nombre=nombre_actual)
                if check_password(password_actual, usuario.password): # Verifica la contraseña
                    # Cambia el nombre de usuario por el nuevo
                    usuario.nombre = nombre_nuevo
                    usuario.save()
                    
                    print("nombre cambiado correctamente.")
                    # Redirige al login para iniciar sesion con el nuevo nombre
                    return redirect('cerrar_sesion')
                else:
                    print("Contraseña incorrecta")
                    return redirect('mi_cuenta_vista')
            except ObjectDoesNotExist:
                return redirect('mi_cuenta_vista')
    else:
        return redirect('mi_cuenta_vista')
# Vista para cambiar la contraseña
def cambiar_password(request):
    if request.method == "POST":
        nombre = request.session['usuario']['nombre'] # Obtiene el nombre almacenado en la sesion
        passwordActual = request.POST['passwordActual'].strip()
        passwordNueva = request.POST['passwordNueva'].strip()
        
        # Verifica que las contraseñas no sean iguales
        if passwordActual == passwordNueva:
            messages.error(request, "Las 2 contraseñas son iguales.")
            return redirect('mi_cuenta_vista')
        else:
            try:
                usuario = Usuarios.objects.get(nombre=nombre)  # Intenta obtener el usuario
                # Verifica la contraseña
                if check_password(passwordActual, usuario.password):  # Verifica la contraseña cifrada
                    # Guarda la contraseña nueva
                    usuario.password = passwordNueva
                    usuario.save()
                    # Mensaje y redireccion
                    messages.success(request, "Contraseña cambiada correctamente.")
                    return redirect('mi_cuenta_vista')
                else:
                    messages.error(request, "La contraseña es incorrecta.")
                    return redirect('mi_cuenta_vista')
            except ObjectDoesNotExist:
                return redirect('mi_cuenta_vista')
    else:
        return redirect('mi_cuenta_vista')