from django.db.models import Count
from .models import Medal, UserMedal, User, Room, PlantGuide, CultivationTechnique

def initialize_medals():
    """
    Inicializa las medallas en la base de datos si no existen.
    """
    medals_data = [
        {
            'medal_type': 'perfil',
            'name': 'Crea un Perfil',
            'description': 'Has creado tu perfil en Leafy',
            'image': 'images/Icons/perfil.png'
        },
        {
            'medal_type': 'likes',
            'name': 'Hojitas',
            'description': 'Uno de tus rooms ha recibido 5 o mas likes',
            'image': 'images/Icons/likes.png'
        },
        {
            'medal_type': 'influencer',
            'name': 'Super Influencer',
            'description': 'Has creado 5 o mas rooms',
            'image': 'images/Icons/influencer.png'
        },
        {
            'medal_type': 'guias',
            'name': 'Creador de Guias',
            'description': 'Has creado una o mas guias de plantas',
            'image': 'images/Icons/guias.png'
        },
        {
            'medal_type': 'tecnicas',
            'name': 'Creador de Tecnicas',
            'description': 'Has creado una o mas tecnicas de cultivo',
            'image': 'images/Icons/tecnicas.png'
        },
    ]
    
    for medal_data in medals_data:
        Medal.objects.get_or_create(
            medal_type=medal_data['medal_type'],
            defaults={
                'name': medal_data['name'],
                'description': medal_data['description'],
                'image': medal_data['image']
            }
        )

def check_and_award_medals(user):
    """
    Verifica si el usuario cumple con los requisitos para obtener medallas
    y las otorga si corresponde.
    """
    # Asegurarse de que las medallas esten inicializadas
    initialize_medals()
    
    # Medalla de perfil - se otorga automaticamente
    medal_perfil = Medal.objects.get(medal_type='perfil')
    UserMedal.objects.get_or_create(user=user, medal=medal_perfil)
    
    # Medalla de likes - si tiene un room con 5 o mas likes
    medal_likes = Medal.objects.get(medal_type='likes')
    popular_rooms = Room.objects.filter(host=user).annotate(like_count=Count('likes')).filter(like_count__gte=5)
    if popular_rooms.exists() and not UserMedal.objects.filter(user=user, medal=medal_likes).exists():
        UserMedal.objects.create(user=user, medal=medal_likes)
    
    # Medalla de influencer - si ha creado 5 o mas rooms
    medal_influencer = Medal.objects.get(medal_type='influencer')
    room_count = Room.objects.filter(host=user).count()
    if room_count >= 5 and not UserMedal.objects.filter(user=user, medal=medal_influencer).exists():
        UserMedal.objects.create(user=user, medal=medal_influencer)
    
    # Medalla de guias - si ha creado al menos una guia
    medal_guias = Medal.objects.get(medal_type='guias')
    guide_count = PlantGuide.objects.filter(author=user).count()
    if guide_count > 0 and not UserMedal.objects.filter(user=user, medal=medal_guias).exists():
        UserMedal.objects.create(user=user, medal=medal_guias)
    
    # Medalla de tecnicas - si ha creado al menos una tecnica
    medal_tecnicas = Medal.objects.get(medal_type='tecnicas')
    technique_count = CultivationTechnique.objects.filter(author=user).count()
    if technique_count > 0 and not UserMedal.objects.filter(user=user, medal=medal_tecnicas).exists():
        UserMedal.objects.create(user=user, medal=medal_tecnicas)
    
    # Retornar las medallas del usuario para mostrarlas en el perfil
    return UserMedal.objects.filter(user=user).select_related('medal')
