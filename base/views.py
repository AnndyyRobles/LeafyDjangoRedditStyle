from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from .models import Room, Topic, Message, User, PlantCategory, PlantGuide, CultivationTechnique
from .forms import RoomForm, UserForm, MyUserCreationForm
# Create your views here.
#rooms = [
#    {'id':1, 'name':'Lets learn python'},
#    {'id':2, 'name':'Design with me'},
#    {'id':3, 'name':'Frontend developers'},
#]
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
    context = {'user' : user, 'rooms' : rooms, 'room_messages' : room_messages, 'topics' : topics}
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


# Cultivation Techniques Views
def techniquesHome(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    techniques = CultivationTechnique.objects.filter(
        Q(name__icontains=q) | 
        Q(title__icontains=q) | 
        Q(description__icontains=q)
    )
    topics = Topic.objects.all()[0:5]
    room_messages = Message.objects.all()[0:3]
    
    context = {
        'techniques': techniques, 
        'topics': topics, 
        'room_messages': room_messages
    }
    return render(request, 'base/techniques.html', context)

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