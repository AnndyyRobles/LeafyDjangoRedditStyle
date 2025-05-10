from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.contrib.auth import authenticate, login, logout
from .models import Room, Topic, Message, User, PlantCategory, PlantGuide, CultivationTechnique, Friendship, Medal, UserMedal
from .medals import check_and_award_medals
from .forms import RoomForm, UserForm, MyUserCreationForm

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        
        try:
            # Debug: Imprimir usuarios con este email
            users = User.objects.filter(email=email)
            print(f'Found {users.count()} users with email {email}')
            for user in users:
                print(f'User ID: {user.id}, Username: {user.username}, Email: {user.email}')
            
            # Verificamos si el usuario existe
            if not users.exists():
                messages.error(request, 'Email does not exist')
                context = {'page': page}
                return render(request, 'base/login_register.html', context)
            
            # Intenta autenticar al usuario
            user = authenticate(request, username=email, password=password)
            
            # Si falla con username=email, intenta con email=email
            if user is None:
                user = authenticate(request, email=email, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                print(f'Authentication failed for {email}')
                messages.error(request, 'Invalid password - Please make sure you are using the right credentials')
                
        except Exception as e:
            print(f'Login error: {str(e)}')
            messages.error(request, f'An error occurred: {str(e)}')
    
    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            # Mostrar errores de validación detallados en mensajes
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    return render(request, 'base/login_register.html', {'form' : form, 'page': 'register'})

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(Q(topic__name__icontains = q) | Q(name__icontains = q)| Q(description__icontains = q))
    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages = Message.objects.all().filter(Q(room__topic__name__icontains = q))

    context = {'rooms' : rooms, 'topics' : topics, 'room_count' : room_count, 'room_messages' : room_messages}
    return render(request, 'base/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    # Obtener solo los mensajes principales (sin padres)
    room_messages = room.message_set.filter(parent=None).select_related('user').prefetch_related('replies', 'replies__user', 'replies__replies', 'replies__replies__user')
    participants = room.participants.all()

    if request.method == 'POST':
        parent_id = request.POST.get('parent_id')
        depth = 0
        parent = None
        
        # Si es una respuesta a otro mensaje
        if parent_id:
            try:
                parent = Message.objects.get(id=parent_id)
                # Limitar la profundidad a 2 niveles (0, 1, 2)
                depth = min(parent.depth + 1, 2)
            except Message.DoesNotExist:
                # Si el mensaje padre no existe, crear un mensaje normal
                pass
            
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body'),
            parent=parent,
            depth=depth
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {
        'room': room, 
        'room_messages': room_messages, 
        'participants': participants
    }
    return render(request, 'base/room.html', context)

def send_message_ajax(request, pk):
    """Vista para enviar mensajes mediante AJAX sin recargar la página"""
    from django.http import JsonResponse
    
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            room = Room.objects.get(id=pk)
            body = request.POST.get('body')
            parent_id = request.POST.get('parent_id')
            
            if not body or body.strip() == '':
                return JsonResponse({
                    'status': 'error',
                    'message': 'El mensaje no puede estar vacío'
                }, status=400)
            
            depth = 0
            parent = None
            
            # Si es una respuesta a otro mensaje
            if parent_id:
                try:
                    parent = Message.objects.get(id=parent_id)
                    # Limitar la profundidad a 2 niveles (0, 1, 2)
                    depth = min(parent.depth + 1, 2)
                except Message.DoesNotExist:
                    return JsonResponse({
                        'status': 'error',
                        'message': 'El mensaje al que intentas responder no existe'
                    }, status=404)
            
            # Crear el mensaje
            message = Message.objects.create(
                user=request.user,
                room=room,
                body=body,
                parent=parent,
                depth=depth
            )
            
            room.participants.add(request.user)
            
            # Devolver una respuesta JSON con información detallada
            return JsonResponse({
                'status': 'success',
                'message': {
                    'id': message.id,
                    'body': message.body,
                    'user_id': message.user.id,
                    'user_name': message.user.username,
                    'parent_id': parent_id if parent_id else None,
                    'depth': depth,
                    'created': message.created.strftime('%Y-%m-%d %H:%M:%S')
                }
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'Error al procesar la solicitud: {str(e)}'
            }, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=400)

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    
    # Obtener amigos del usuario
    friends = user.get_friends()
    
    # Verificar si el usuario actual es amigo del perfil que está viendo
    is_friend = False
    friendship = None
    if request.user.is_authenticated and request.user.id != user.id:
        is_friend = request.user.is_friend(user)
        # Buscar si existe una solicitud de amistad pendiente
        friendship = Friendship.objects.filter(
            (Q(from_user=request.user) & Q(to_user=user)) |
            (Q(from_user=user) & Q(to_user=request.user))
        ).first()
    
    # Verificar y otorgar medallas al usuario
    user_medals = check_and_award_medals(user)
    
    context = {
        'user': user, 
        'rooms': rooms, 
        'room_messages': room_messages, 
        'topics': topics,
        'friends': friends,
        'is_friend': is_friend,
        'friendship': friendship,
        'user_medals': user_medals
    }
    return render(request, 'base/profile.html', context)

@login_required(login_url = 'login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all().order_by('name')
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
            image=request.FILES.get('image'),
        )
        return redirect('home')
    context = {'form':form, 'topics' : topics}
    return render(request, 'base/room_form.html', context)

@login_required(login_url = 'login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all().order_by('name')

    if request.user != room.host:
        return HttpResponse('You are not the owner of this room')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        if request.FILES.get('image'):
            room.image = request.FILES.get('image')
        room.save()
        return redirect('home')
    context = {'form' : form, 'topics' : topics, 'room' : room}
    return render(request, 'base/room_form.html', context)

@login_required(login_url = 'login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('You are not the owner of this room')

    if  request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':room})

@login_required(login_url = 'login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You are not the owner of this message')

    if  request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':message})

@login_required(login_url = 'login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    return render(request, 'base/update-user.html', {'form' : form})

def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html', {'topics' : topics})

def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, 'base/activity.html', {'room_messages' : room_messages})


# Plant Guides Views
def guidesHome(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    categories = PlantCategory.objects.all().order_by('name')
    
    if q:
        plant_guides = PlantGuide.objects.filter(
            Q(categories__name__icontains=q) |
            Q(common_name__icontains=q) |
            Q(scientific_name__icontains=q) |
            Q(description__icontains=q)
        ).distinct()
    else:
        plant_guides = PlantGuide.objects.all()
        
    context = {
        'categories': categories,
        'plant_guides': plant_guides,
        'plant_count': plant_guides.count(),
    }
    return render(request, 'base/guides.html', context)


def guideDetail(request, pk):
    plant_guide = get_object_or_404(PlantGuide, id=pk)
    categories = plant_guide.categories.all()
    
    context = {
        'guide': plant_guide,
        'categories': categories,
    }
    return render(request, 'base/guide_detail.html', context)


@login_required(login_url='login')
def createGuide(request):
    categories = PlantCategory.objects.all().order_by('name')
    
    if request.method == 'POST':
        # Get category from form (with new input format)
        category_name = request.POST.get('category')
        
        # Obtener o crear la categoría según el nombre
        if category_name:
            category, created = PlantCategory.objects.get_or_create(name=category_name)
            selected_categories = [category]
        else:
            selected_categories = []
        
        # Create plant guide
        plant_guide = PlantGuide(
            author=request.user,
            common_name=request.POST.get('common_name'),
            scientific_name=request.POST.get('scientific_name'),
            description=request.POST.get('description'),
            germination=request.POST.get('germination'),
            transplanting=request.POST.get('transplanting'),
            harvest=request.POST.get('harvest'),
            watering=request.POST.get('watering'),
            sunlight=request.POST.get('sunlight'),
            extra_care=request.POST.get('extra_care'),
            difficulty=request.POST.get('difficulty'),
            growing_season=request.POST.get('growing_season'),
            days_to_harvest=request.POST.get('days_to_harvest'),
        )
        
        if request.FILES.get('guide_picture'):
            plant_guide.guide_picture = request.FILES.get('guide_picture')
            
        plant_guide.save()
        
        # Add categories to plant guide
        plant_guide.categories.set(selected_categories)
        
        return redirect('guides')
    
    context = {'categories': categories}
    return render(request, 'base/guide_form.html', context)


@login_required(login_url='login')
def updateGuide(request, pk):
    plant_guide = get_object_or_404(PlantGuide, id=pk)
    categories = PlantCategory.objects.all().order_by('name')
    
    # Check if user is author
    if request.user != plant_guide.author:
        return HttpResponse('You are not authorized to edit this guide')
    
    if request.method == 'POST':
        # Get category from form (with new input format)
        category_name = request.POST.get('category')
        
        # Obtener o crear la categoru00eda segu00fan el nombre
        if category_name:
            category, created = PlantCategory.objects.get_or_create(name=category_name)
            selected_categories = [category]
        else:
            selected_categories = []
        
        # Update plant guide
        plant_guide.common_name = request.POST.get('common_name')
        plant_guide.scientific_name = request.POST.get('scientific_name')
        plant_guide.description = request.POST.get('description')
        plant_guide.germination = request.POST.get('germination')
        plant_guide.transplanting = request.POST.get('transplanting')
        plant_guide.harvest = request.POST.get('harvest')
        plant_guide.watering = request.POST.get('watering')
        plant_guide.sunlight = request.POST.get('sunlight')
        plant_guide.extra_care = request.POST.get('extra_care')
        plant_guide.difficulty = request.POST.get('difficulty')
        plant_guide.growing_season = request.POST.get('growing_season')
        plant_guide.days_to_harvest = request.POST.get('days_to_harvest')
        
        if request.FILES.get('guide_picture'):
            plant_guide.guide_picture = request.FILES.get('guide_picture')
            
        plant_guide.save()
        
        # Update categories
        plant_guide.categories.set(selected_categories)
        
        return redirect('guide', pk=plant_guide.id)
    
    context = {
        'guide': plant_guide, 
        'categories': categories,
        'selected_categories': plant_guide.categories.all()
    }
    return render(request, 'base/guide_form.html', context)


@login_required(login_url='login')
def deleteGuide(request, pk):
    plant_guide = get_object_or_404(PlantGuide, id=pk)
    
    # Check if user is author
    if request.user != plant_guide.author:
        return HttpResponse('You are not authorized to delete this guide')
    
    if request.method == 'POST':
        plant_guide.delete()
        return redirect('guides')
    
    return render(request, 'base/delete.html', {'obj': plant_guide})

# Likes (hojitas) views
from django.views.decorators.csrf import csrf_exempt

@login_required(login_url='login')
def likeRoom(request, pk):
    room = get_object_or_404(Room, id=pk)
    
    # Alternar el estado del like
    if request.user in room.likes.all():
        room.likes.remove(request.user)
    else:
        room.likes.add(request.user)
    
    # Redirigir a la página anterior
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    return redirect('home')

@login_required(login_url='login')
def likeMessage(request, pk):
    message = get_object_or_404(Message, id=pk)
    
    # Alternar el estado del like
    if request.user in message.likes.all():
        message.likes.remove(request.user)
    else:
        message.likes.add(request.user)
    
    # Redirigir a la página anterior
    referer = request.META.get('HTTP_REFERER')
    return redirect('room', pk=message.room.id)


@login_required(login_url='login')
def likeTechnique(request, pk):
    technique = CultivationTechnique.objects.get(id=pk)
    if request.user.is_authenticated:
        if request.user in technique.likes.all():
            technique.likes.remove(request.user)
        else:
            technique.likes.add(request.user)
    return redirect('technique-detail', pk=technique.id)


@login_required(login_url='login')
def send_friend_request(request, pk):
    """Agregar amigo inmediatamente"""
    to_user = User.objects.get(id=pk)
    from_user = request.user
    
    # Verificar que no se agregue a sí mismo
    if to_user == from_user:
        messages.error(request, 'No puedes agregarte a ti mismo como amigo')
        return redirect('user-profile', pk=to_user.id)
    
    # Verificar si ya existe una relación de amistad
    friendship = Friendship.objects.filter(
        (Q(from_user=from_user) & Q(to_user=to_user)) |
        (Q(from_user=to_user) & Q(to_user=from_user))
    ).first()
    
    if friendship:
        # Si ya son amigos
        if friendship.status == 'accepted':
            messages.info(request, 'Ya son amigos')
        # Si hay alguna relación previa, actualizarla a aceptada
        else:
            friendship.status = 'accepted'
            friendship.save()
            messages.success(request, f'Has agregado a {to_user.username} como amigo')
    else:
        # Crear nueva relación de amistad (aceptada inmediatamente)
        Friendship.objects.create(
            from_user=from_user, 
            to_user=to_user, 
            status='accepted'
        )
        messages.success(request, f'Has agregado a {to_user.username} como amigo')
    
    # Usar referer para volver a la página anterior si existe
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    return redirect('user-profile', pk=to_user.id)


@login_required(login_url='login')
def accept_friend_request(request, pk):
    """Aceptar solicitud de amistad"""
    friendship = Friendship.objects.get(id=pk)
    
    # Verificar que el usuario sea el destinatario de la solicitud
    if request.user != friendship.to_user:
        messages.error(request, 'No tienes permiso para aceptar esta solicitud')
        return redirect('home')
    
    friendship.status = 'accepted'
    friendship.save()
    messages.success(request, f'Ahora eres amigo de {friendship.from_user.username}')
    
    return redirect('user-profile', pk=friendship.from_user.id)


@login_required(login_url='login')
def reject_friend_request(request, pk):
    """Rechazar solicitud de amistad"""
    friendship = Friendship.objects.get(id=pk)
    
    # Verificar que el usuario sea el destinatario de la solicitud
    if request.user != friendship.to_user:
        messages.error(request, 'No tienes permiso para rechazar esta solicitud')
        return redirect('home')
    
    friendship.status = 'rejected'
    friendship.save()
    messages.info(request, f'Has rechazado la solicitud de amistad de {friendship.from_user.username}')
    
    return redirect('user-profile', pk=friendship.from_user.id)


@login_required(login_url='login')
def remove_friend(request, pk):
    """Eliminar amigo"""
    friend = User.objects.get(id=pk)
    
    # Buscar la relación de amistad
    friendship = Friendship.objects.filter(
        (Q(from_user=request.user) & Q(to_user=friend) & Q(status='accepted')) |
        (Q(from_user=friend) & Q(to_user=request.user) & Q(status='accepted'))
    ).first()
    
    if friendship:
        friendship.delete()
        messages.success(request, f'Has eliminado a {friend.username} de tus amigos')
    else:
        messages.error(request, 'No existe una relación de amistad con este usuario')
    
    # Usar referer para volver a la página anterior si existe
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    return redirect('user-profile', pk=friend.id)


# Cultivation Techniques Views
def techniquesHome(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    techniques = CultivationTechnique.objects.filter(
        Q(name__icontains=q) | 
        Q(title__icontains=q) | 
        Q(description__icontains=q)
    )
    topics = Topic.objects.all()[0:5]
    
    # Técnicas principales para mostrar en la columna derecha
    main_techniques = [
        {'name': 'Vertical', 'display_name': 'Cultivo Vertical', 'url_name': 'vertical-technique'},
        {'name': 'Wall-mounted', 'display_name': 'Cultivo en Pared', 'url_name': 'wall-mounted-technique'},
        {'name': 'Hydroponics', 'display_name': 'Hidroponía', 'url_name': 'hydroponics-technique'},
        {'name': 'Recycled Materials', 'display_name': 'Materiales Reciclados', 'url_name': 'recycled-materials-technique'},
        {'name': 'Aquaponics', 'display_name': 'Acuaponía', 'url_name': 'aquaponics-technique'}
    ]
    
    context = {
        'techniques': techniques, 
        'topics': topics, 
        'main_techniques': main_techniques
    }
    return render(request, 'base/techniques.html', context)

# Vistas para las técnicas principales
def verticalTechniqueInfo(request):
    context = {
        'title': 'Sistema de Cultivo Vertical para Espacios Reducidos',
        'difficulty': 'Intermedio',
        'cost': '$100-150',
        'space': '1m² x 2m',
        'setup_time': '3-4 horas',
        'description': 'Este sistema de cultivo vertical aprovecha el espacio vertical para cultivar una variedad de plantas sin suelo. Utiliza un sistema de bombeo que hace circular agua rica en nutrientes a través de tubos PVC dispuestos en forma vertical, permitiendo cultivar hasta 36 plantas en apenas 1 metro cuadrado de espacio.',
        'setup_instructions': ['Corta los tubos PVC de 4 pulgadas en secciones de 1 metro.', 'Perfora agujeros de 2 pulgadas de diámetro a lo largo de los tubos, espaciados cada 20 cm.', 'Monta la estructura de soporte usando madera tratada o metal.', 'Instala la bomba de agua en el depósito inferior.', 'Conecta los tubos al sistema de bombeo usando mangueras de 1/2 pulgada.', 'Instala el temporizador para controlar los ciclos de riego.'],
        'maintenance_tips': ['Revisa el pH del agua cada 3 días, manteniéndolo entre 5.8 y 6.2.', 'Cambia la solución nutritiva completamente cada 2 semanas.', 'Limpia los filtros de la bomba semanalmente para evitar obstrucciones.', 'Verifica que no haya fugas en las conexiones de las mangueras.', 'Durante el verano, añade un sistema de enfriamiento para mantener la temperatura del agua por debajo de 24°C.'],
        'recommended_plants': ['Lechugas (todas las variedades)', 'Espinacas', 'Albahaca y otras hierbas aromáticas', 'Fresas', 'Pimientos pequeños', 'Tomates cherry (con soporte adicional)'],
        'space_requirements': ['Un área de 1m² en la base', 'Altura mínima de 2 metros', 'Acceso a electricidad para la bomba', 'Ubicación con al menos 6 horas de luz solar directa', 'Protección contra vientos fuertes si se instala en exterior'],
        'materials': ['4 tubos PVC de 4 pulgadas x 1 metro', '1 depósito de agua de 50 litros', '1 bomba de agua sumergible (400-600 L/h)', '5 metros de manguera de 1/2 pulgada', '36 canastillas para hidroponía', '1 temporizador digital', 'Estructura de soporte (madera tratada o metal)', 'Kit de medición de pH y EC', 'Solución nutritiva para hidroponía'],
        'benefits': ['Aprovechamiento óptimo del espacio vertical', 'Ahorro de agua (hasta 90% menos que cultivo tradicional)', 'Mayor velocidad de crecimiento', 'Reducción de plagas y enfermedades', 'No requiere deshierbe', 'Producción durante todo el año'],
        'limitations': ['Dependencia de electricidad para la bomba', 'Requiere monitoreo constante de pH y nutrientes', 'Inversión inicial moderada', 'No es adecuado para plantas de raíz grande', 'Requiere conocimientos básicos de hidroponía'],
        'technique_type': 'Vertical',
        # Imagen principal en la parte superior
        'main_image': 'https://i.pinimg.com/736x/3d/05/2b/3d052bd7c472a79693e280808d1cf764.jpg',
        # Imágenes adicionales para los recuadros inferiores
        'image_fifth': 'https://i.pinimg.com/736x/e5/a2/01/e5a201457333ddec0dea3a2089ae1280.jpg',
        'image_sixth': 'https://i.pinimg.com/736x/c9/f2/0b/c9f20b76fd722326687663f63f16d0c4.jpg'
    }
    return render(request, 'base/main_technique.html', context)

def wallMountedTechniqueInfo(request):
    context = {
        'title': 'Sistema de Cultivo en Pared para Decoración y Producción',
        'difficulty': 'Principiante',
        'cost': '$50-120',
        'space': '2m² de pared',
        'setup_time': '2-3 horas',
        'description': 'El sistema de cultivo en pared permite aprovechar superficies verticales para crear jardines funcionales y decorativos. Ideal para balcones, terrazas y espacios interiores con buena iluminación, combina estética y productividad en un mismo espacio.',
        'setup_instructions': ['Selecciona una pared con buena iluminación (natural o artificial).', 'Instala un sistema de soporte resistente al peso y la humedad.', 'Coloca una barrera impermeable para proteger la pared.', 'Monta los contenedores o bolsillos de cultivo en el soporte.', 'Instala un sistema de riego por goteo (opcional pero recomendado).', 'Llena los contenedores con sustrato ligero y bien drenado.'],
        'maintenance_tips': ['Riega con moderación, evitando encharcamientos.', 'Fertiliza cada 2-3 semanas con fertilizante líquido diluido.', 'Rota las plantas según la temporada y su desarrollo.', 'Revisa regularmente el estado de los soportes y la impermeabilización.', 'Poda las plantas para mantener un tamaño adecuado al espacio.'],
        'recommended_plants': ['Hierbas aromáticas (albahaca, tomillo, romero, menta)', 'Plantas de hoja verde (lechuga, rúcula, espinaca)', 'Fresas', 'Suculentas y cactus (para zonas con poca agua)', 'Flores comestibles (pensamientos, capuçhinas)', 'Plantas ornamentales de poco desarrollo radicular'],
        'space_requirements': ['Una pared con buena iluminación', 'Capacidad para soportar el peso del sistema (aproximadamente 10-15 kg/m²)', 'Acceso para mantenimiento y riego', 'Protección contra vientos fuertes si está en exterior', 'Drenaje adecuado para el agua sobrante'],
        'materials': ['Estructura de soporte (madera tratada, metal o plástico resistente)', 'Barrera impermeable (lámina plástica o geotextil)', 'Contenedores o bolsillos de cultivo', 'Sustrato ligero (mezcla de fibra de coco, perlita y compost)', 'Sistema de riego por goteo (opcional)', 'Herramientas básicas de jardinería', 'Tornillería y anclajes para pared'],
        'benefits': ['Aprovechamiento de espacios infrautilizados', 'Efecto decorativo y bienestar psicológico', 'Mejora de la calidad del aire interior', 'Aislamiento térmico y acústico', 'Fácil acceso para personas con movilidad reducida', 'Posibilidad de cultivar sin agacharse'],
        'limitations': ['Limitación en el tamaño de las plantas', 'Necesidad de riego frecuente', 'Posibles problemas de humedad en la pared si no se impermeabiliza correctamente', 'Peso limitado que puede soportar la estructura', 'Menor volumen de sustrato disponible para las raíces'],
        'technique_type': 'Wall-mounted',
        # Imagen principal en la parte superior
        'main_image': 'https://i.pinimg.com/736x/a2/d0/af/a2d0af1269df63d430b4372eafe08420.jpg',
        # Imágenes adicionales para los recuadros inferiores
        'image_fifth': 'https://i.pinimg.com/736x/6e/8f/1e/6e8f1ec3a17694d238590881111c4322.jpg',
        'image_sixth': 'https://i.pinimg.com/736x/7a/18/fb/7a18fb04e07f110b2a68856b216678dd.jpg'
    }
    return render(request, 'base/main_technique.html', context)

def hydroponicsTechniqueInfo(request):
    context = {
        'title': 'Sistema Hidropónico NFT para Producción Intensiva',
        'difficulty': 'Intermedio',
        'cost': '$150-300',
        'space': '2m²',
        'setup_time': '4-6 horas',
        'description': 'La hidroponía NFT (Nutrient Film Technique) es un sistema de cultivo sin suelo donde las raíces de las plantas están en contacto con una fina película de solución nutritiva que circula constantemente. Este método permite una producción intensiva con un uso mínimo de agua y nutrientes.',
        'setup_instructions': ['Construye la estructura de soporte con la inclinación adecuada (1-3%).', 'Instala los canales de cultivo (tubos de PVC o canaletas) sobre la estructura.', 'Coloca el tanque de reserva en la parte inferior del sistema.', 'Instala la bomba de agua y conecta las tuberías.', 'Prepara la solución nutritiva según las necesidades de tus cultivos.', 'Coloca las plantas en los agujeros de los canales usando canastillas hidropónicas.'],
        'maintenance_tips': ['Monitorea diariamente el pH (5.5-6.5) y la conductividad eléctrica (EC).', 'Mantiene la temperatura de la solución entre 18-24°C.', 'Cambia la solución nutritiva completamente cada 7-14 días.', 'Limpia regularmente los filtros y tuberías para evitar obstrucciones.', 'Verifica que la bomba funcione correctamente las 24 horas.', 'Controla la aparición de algas cubriendo el sistema de la luz directa.'],
        'recommended_plants': ['Lechugas y verduras de hoja', 'Hierbas aromáticas', 'Fresas', 'Tomates cherry (con soporte adicional)', 'Pimientos', 'Pepinos pequeños'],
        'space_requirements': ['Área de 2m² mínimo', 'Altura variable según diseño (generalmente 1-1.5m)', 'Acceso a electricidad 24/7', 'Protección contra temperaturas extremas', 'Buena ventilación', 'Iluminación adecuada (natural o artificial)'],
        'materials': ['Tubos de PVC de 3-4 pulgadas o canaletas', 'Tanque de reserva (50-100 litros)', 'Bomba de agua sumergible (400-800 L/h)', 'Tuberías y conexiones', 'Timer (opcional para ciclos de riego)', 'Kit de medición de pH y EC', 'Nutrientes hidropónicos (macro y micronutrientes)', 'Canastillas hidropónicas', 'Sustrato inerte para germinación (espuma, lana de roca)'],
        'benefits': ['Ahorro de agua (hasta 90% menos que cultivo tradicional)', 'Mayor control sobre la nutrición de las plantas', 'Crecimiento más rápido y mayor productividad', 'Ausencia de malezas', 'Menor incidencia de plagas y enfermedades del suelo', 'Posibilidad de automatización completa'],
        'limitations': ['Dependencia total de electricidad', 'Requiere conocimientos técnicos sobre nutrición vegetal', 'Inversión inicial moderada-alta', 'Necesidad de monitoreo constante', 'Riesgo de pérdida total en caso de fallo eléctrico prolongado', 'Curva de aprendizaje pronunciada'],
        'technique_type': 'Hydroponics',
        # Imagen principal en la parte superior
        'main_image': 'https://i.pinimg.com/736x/0e/8c/7a/0e8c7ab74b99a8fefb028ad80a56aae7.jpg',
        # Imágenes adicionales para los recuadros inferiores
        'image_fifth': 'https://i.pinimg.com/736x/17/c3/29/17c3298bf1cee84040bbaa1d2e5000c5.jpg',
        'image_sixth': 'https://i.pinimg.com/736x/e4/24/58/e42458b67e062b787f70a51055b36067.jpg'
    }
    return render(request, 'base/main_technique.html', context)

def recycledMaterialsTechniqueInfo(request):
    context = {
        'title': 'Sistema de Cultivo con Materiales Reciclados',
        'difficulty': 'Principiante',
        'cost': '$20-80',
        'space': 'Variable',
        'setup_time': '2-4 horas',
        'description': 'El cultivo con materiales reciclados transforma objetos cotidianos en espacios productivos, reduciendo residuos y costos. Esta técnica versátil permite crear jardines en botellas plásticas, pallets, neumáticos y otros materiales reutilizados, adaptándose a cualquier espacio disponible.',
        'setup_instructions': ['Selecciona materiales reciclados en buen estado (botellas, pallets, neumáticos, etc.).', 'Limpia y desinfecta todos los materiales a fondo.', 'Realiza los agujeros necesarios para drenaje y ventilación.', 'Aplica pintura o sellador no tóxico si es necesario.', 'Prepara un sustrato adecuado mezclando tierra, compost y material drenante.', 'Instala el sistema de riego apropiado para cada tipo de contenedor.'],
        'maintenance_tips': ['Adapta la frecuencia de riego al tipo de contenedor (los materiales reciclados pueden secarse más rápido).', 'Fertiliza regularmente, ya que muchos materiales reciclados no retienen nutrientes.', 'Monitorea la degradación de los materiales y reemplázalos cuando sea necesario.', 'Rota los cultivos para evitar el agotamiento del sustrato.', 'Protege los materiales sensibles a la intemperie durante condiciones climáticas extremas.'],
        'recommended_plants': ['Hierbas aromáticas', 'Verduras de hoja verde', 'Plantas ornamentales resistentes', 'Raíces y tubérculos pequeños', 'Fresas y berries', 'Flores comestibles'],
        'space_requirements': ['Adaptable a cualquier espacio disponible', 'Buena exposición solar (mínimo 4-6 horas diarias)', 'Superficie estable para contenedores pesados', 'Protección contra vientos fuertes para estructuras ligeras', 'Acceso para mantenimiento regular'],
        'materials': ['Materiales reciclados (botellas plásticas, pallets, neumáticos, latas, etc.)', 'Herramientas básicas (tijeras, cuchillo, taladro)', 'Sustrato de calidad', 'Pintura o sellador no tóxico (opcional)', 'Material para drenaje (piedras, trozos de cerámica)', 'Compost o fertilizante orgánico', 'Cuerdas, alambres o soportes para estructuras verticales'],
        'benefits': ['Costo mínimo de implementación', 'Reducción de residuos y huella ecológica', 'Alta adaptabilidad a diferentes espacios', 'Valor educativo y creativo', 'Posibilidad de cultivar sin necesidad de terreno', 'Facilidad para principiantes'],
        'limitations': ['Durabilidad limitada de algunos materiales', 'Capacidad restringida para plantas grandes', 'Posible lixiviación de sustancias desde ciertos materiales', 'Estética variable (puede no ser adecuada para todos los espacios)', 'Mayor frecuencia de riego en contenedores pequeños', 'Posible sobrecalentamiento en contenedores oscuros'],
        'technique_type': 'Recycled Materials',
        # Imagen principal en la parte superior
        'main_image': 'https://i.pinimg.com/736x/ab/e3/5e/abe35ef08501b43a5381fd456bc8c844.jpg',
        # Imágenes adicionales para los recuadros inferiores
        'image_fifth': 'https://i.pinimg.com/736x/4d/a8/5b/4da85bf3c6309f7dcc87f24742ed1406.jpg',
        'image_sixth': 'https://i.pinimg.com/736x/98/58/20/9858205f56fc856b0ad6299a333dd7e6.jpg'
    }
    return render(request, 'base/main_technique.html', context)

def aquaponicsTechniqueInfo(request):
    context = {
        'title': 'Sistema Acuapónico Integrado para Producción Sostenible',
        'difficulty': 'Avanzado',
        'cost': '$300-600',
        'space': '3-4m²',
        'setup_time': '8-12 horas',
        'description': 'La acuaponía es un sistema de producción que integra la acuicultura (cría de peces) con la hidroponía (cultivo de plantas sin suelo) en un ecosistema simbiótico. Los desechos de los peces proporcionan nutrientes para las plantas, mientras que éstas filtran el agua para los peces, creando un ciclo sostenible y altamente productivo.',
        'setup_instructions': ['Instala el tanque para peces con capacidad adecuada (mínimo 200 litros).', 'Monta el sistema de filtración (filtro mecánico y biofiltro).', 'Construye las camas de cultivo sobre el tanque o a un lado.', 'Instala la bomba de agua y el sistema de tuberías.', 'Prepara el sustrato para las plantas (arcilla expandida, grava o similar).', 'Cicla el sistema durante 3-4 semanas antes de introducir peces.', 'Introduce gradualmente los peces una vez establecidas las bacterias nitrificantes.'],
        'maintenance_tips': ['Monitorea diariamente los parámetros del agua (pH, amoníaco, nitritos, nitratos).', 'Alimenta a los peces con la cantidad adecuada (3-5% de su peso corporal).', 'Mantiene la temperatura del agua entre 18-26°C según la especie de pez.', 'Limpia regularmente los filtros y elimina los sólidos acumulados.', 'Controla el nivel del agua y repone la evaporada.', 'Equilibra la densidad de peces con la superficie de cultivo (1kg de pez por 10-20 plantas).', 'Realiza pruebas de calidad del agua semanalmente.'],
        'recommended_plants': ['Verduras de hoja verde (lechuga, espinaca, acelga)', 'Hierbas aromáticas', 'Tomates cherry y pimientos pequeños', 'Pepinos', 'Fresas', 'Plantas de raíz poco profunda'],
        'space_requirements': ['Área mínima de 3-4m²', 'Superficie resistente que soporte el peso del sistema (400-600kg)', 'Ubicación con buena luz natural o iluminación artificial', 'Protección contra temperaturas extremas', 'Acceso a electricidad 24/7', 'Ventilación adecuada'],
        'materials': ['Tanque para peces (200-500 litros)', 'Camas de cultivo o sistemas NFT/DWC', 'Bomba de agua sumergible (1500-3000 L/h)', 'Bomba de aire y piedras difusoras', 'Sistema de filtración (filtro mecánico y biofiltro)', 'Tuberías y conexiones', 'Sustrato para plantas (arcilla expandida, grava)', 'Kit de prueba de agua completo', 'Bacterias nitrificantes para el arranque', 'Peces apropiados (tilapia, carpa, etc.)'],
        'benefits': ['Sistema cerrado con mínimo consumo de agua', 'Doble producción (vegetales y proteína animal)', 'No requiere fertilizantes químicos', 'Alta productividad en espacio reducido', 'Menor incidencia de plagas y enfermedades', 'Sostenibilidad y bajo impacto ambiental'],
        'limitations': ['Inversión inicial alta', 'Complejidad técnica y curva de aprendizaje pronunciada', 'Dependencia total de electricidad', 'Equilibrio delicado entre subsistemas', 'Requiere monitoreo constante', 'Limitaciones en tipos de cultivos (no adecuado para plantas que requieren muchos nutrientes)'],
        'technique_type': 'Aquaponics',
        # Imagen principal en la parte superior
        'main_image': 'https://i.pinimg.com/736x/49/cc/5d/49cc5d3ef0d1c520ba39f255d3cce76e.jpg',
        # Imágenes adicionales para los recuadros inferiores
        'image_fifth': 'https://i.pinimg.com/736x/53/bb/63/53bb63b40728d608f2eddeb2a49ca61c.jpg',
        'image_sixth': 'https://i.pinimg.com/736x/a2/5e/d4/a25ed4749814a6ae05c83742c8604915.jpg'
    }
    return render(request, 'base/main_technique.html', context)

def techniqueDetail(request, pk):
    technique = get_object_or_404(CultivationTechnique, id=pk)
    context = {'technique': technique}
    return render(request, 'base/technique_detail.html', context)

@login_required(login_url='login')
def createTechnique(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        title = request.POST.get('title')
        description = request.POST.get('description')
        setup_instructions = request.POST.get('setup_instructions')
        maintenance_tips = request.POST.get('maintenance_tips')
        recommended_plants = request.POST.get('recommended_plants')
        space_requirements = request.POST.get('space_requirements')
        difficulty_level = request.POST.get('difficulty_level')
        estimated_cost = request.POST.get('estimated_cost')
        materials_needed = request.POST.get('materials_needed')
        benefits = request.POST.get('benefits')
        limitations = request.POST.get('limitations')
        
        technique = CultivationTechnique.objects.create(
            author=request.user,
            name=name,
            title=title,
            description=description,
            setup_instructions=setup_instructions,
            maintenance_tips=maintenance_tips,
            recommended_plants=recommended_plants,
            space_requirements=space_requirements,
            difficulty_level=difficulty_level,
            estimated_cost=estimated_cost,
            materials_needed=materials_needed,
            benefits=benefits,
            limitations=limitations
        )
        
        if request.FILES.get('main_image'):
            technique.main_image = request.FILES.get('main_image')
        if request.FILES.get('image_second'):
            technique.image_second = request.FILES.get('image_second')
        if request.FILES.get('image_third'):
            technique.image_third = request.FILES.get('image_third')
        if request.FILES.get('image_fourth'):
            technique.image_fourth = request.FILES.get('image_fourth')
            
        technique.save()
        technique.participants.add(request.user)
        return redirect('techniques')
    
    return render(request, 'base/technique_form.html', {
        'difficulty_choices': CultivationTechnique.TECHNIQUE_CHOICES,
        'difficulty_levels': PlantGuide.DIFFICULTY_CHOICES
    })

@login_required(login_url='login')
def updateTechnique(request, pk):
    technique = get_object_or_404(CultivationTechnique, id=pk)
    
    if request.user != technique.author and not request.user.is_staff:
        return HttpResponse('No estás autorizado para editar esta técnica')
    
    if request.method == 'POST':
        technique.name = request.POST.get('name')
        technique.title = request.POST.get('title')
        technique.description = request.POST.get('description')
        technique.setup_instructions = request.POST.get('setup_instructions')
        technique.maintenance_tips = request.POST.get('maintenance_tips')
        technique.recommended_plants = request.POST.get('recommended_plants')
        technique.space_requirements = request.POST.get('space_requirements')
        technique.difficulty_level = request.POST.get('difficulty_level')
        technique.estimated_cost = request.POST.get('estimated_cost')
        technique.materials_needed = request.POST.get('materials_needed')
        technique.benefits = request.POST.get('benefits')
        technique.limitations = request.POST.get('limitations')
        
        if request.FILES.get('main_image'):
            technique.main_image = request.FILES.get('main_image')
        if request.FILES.get('image_second'):
            technique.image_second = request.FILES.get('image_second')
        if request.FILES.get('image_third'):
            technique.image_third = request.FILES.get('image_third')
        if request.FILES.get('image_fourth'):
            technique.image_fourth = request.FILES.get('image_fourth')
            
        technique.save()
        return redirect('technique', pk=technique.id)
    
    return render(request, 'base/technique_form.html', {
        'technique': technique,
        'difficulty_choices': CultivationTechnique.TECHNIQUE_CHOICES,
        'difficulty_levels': PlantGuide.DIFFICULTY_CHOICES
    })

@login_required(login_url='login')
def deleteTechnique(request, pk):
    technique = get_object_or_404(CultivationTechnique, id=pk)
    
    if request.user != technique.author and not request.user.is_staff:
        return HttpResponse('No estás autorizado para eliminar esta técnica')
    
    if request.method == 'POST':
        technique.delete()
        return redirect('techniques')
    
    return render(request, 'base/delete.html', {'obj': technique})

@login_required(login_url='login')
def likeTechnique(request, pk):
    technique = get_object_or_404(CultivationTechnique, id=pk)
    user = request.user
    
    if user in technique.likes.all():
        technique.likes.remove(user)
        liked = False
    else:
        technique.likes.add(user)
        liked = True
    
    return JsonResponse({'liked': liked, 'count': technique.likes.count()})


import os
import replicate
import requests
from django.conf import settings
from django.core.files.base import ContentFile
from .models import Cultivation3DModel
from .forms import Cultivation3DModelForm
from .utils import generate_prompt

@login_required(login_url='login')
def cultivation3d_home(request):
    """Vista principal para mostrar todos los modelos 3D"""
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    
    if q:
        models = Cultivation3DModel.objects.filter(
            Q(title__icontains=q) |
            Q(description__icontains=q) |
            Q(technique__icontains=q)
        )
    else:
        models = Cultivation3DModel.objects.all()
    
    # Filtrar por usuario si se solicita
    user_id = request.GET.get('user')
    if user_id:
        models = models.filter(user_id=user_id)
    
    # Filtrar por técnica si se solicita
    technique = request.GET.get('technique')
    if technique:
        models = models.filter(technique=technique)
    
    context = {
        'models': models,
        'model_count': models.count(),
        'techniques': Cultivation3DModel.TECHNIQUE_CHOICES,
    }
    return render(request, 'base/cultivation3d_home.html', context)

@login_required(login_url='login')
def create_3d_model(request):
    """Vista para crear un nuevo modelo 3D"""
    if request.method == 'POST':
        form = Cultivation3DModelForm(request.POST)
        if form.is_valid():
            model = form.save(commit=False)
            model.user = request.user
            model.status = 'pending'
            
            # Generar el prompt basado en los datos del formulario
            model.prompt = generate_prompt(model)
            model.save()
            
            # Iniciar la tarea asíncrona
            from .tasks import generate_3d_model
            generate_3d_model.delay(model.id)
            
            messages.success(request, 'Your 3D model is being generated. You will be notified when it is ready.')
            return redirect('cultivation3d_detail', pk=model.id)
    else:
        form = Cultivation3DModelForm()
    
    context = {'form': form}
    return render(request, 'base/cultivation3d_form.html', context)

@login_required(login_url='login')
def cultivation3d_detail(request, pk):
    """Vista para mostrar el detalle de un modelo 3D"""
    model = get_object_or_404(Cultivation3DModel, id=pk)
    context = {'model': model}
    return render(request, 'base/cultivation3d_detail.html', context)

@login_required(login_url='login')
def check_model_status(request, pk):
    """API para verificar el estado de un modelo 3D"""
    model = get_object_or_404(Cultivation3DModel, id=pk, user=request.user)
    
    return JsonResponse({
        'status': model.status,
        'completed': model.status == 'completed',
        'error': model.status == 'error',
        'error_message': model.error_message,
        'has_image': bool(model.generated_image),
        'has_model': bool(model.glb_model),
        'image_url': model.generated_image.url if model.generated_image else None,
        'model_url': model.glb_model.url if model.glb_model else None,
    })

@login_required(login_url='login')
def delete_3d_model(request, pk):
    """Vista para eliminar un modelo 3D"""
    model = get_object_or_404(Cultivation3DModel, id=pk)
    
    if request.user != model.user and not request.user.is_staff:
        return HttpResponse('You are not authorized to delete this model')
    
    if request.method == 'POST':
        model.delete()
        return redirect('cultivation3d_home')
    
    return render(request, 'base/delete.html', {'obj': model})