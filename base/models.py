from django.db import models
from django.contrib.auth.models import AbstractUser 

class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)
    avatar = models.ImageField(null=True, default="blue.jpg")
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def get_friends(self):
        """Retorna todos los amigos del usuario"""
        friend_users = []
        for friendship in self.friendships.filter(status='accepted'):
            friend_users.append(friendship.to_user)
        for friendship in self.friend_requests.filter(status='accepted'):
            friend_users.append(friendship.from_user)
        return friend_users
    
    def get_friend_count(self):
        """Retorna el número de amigos del usuario"""
        return len(self.get_friends())
    
    def is_friend(self, user):
        """Verifica si un usuario es amigo"""
        return user in self.get_friends()

class Topic(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic =  models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    image = models.ImageField(null=True, blank=True, upload_to='room_images/')
    likes = models.ManyToManyField(User, related_name='room_likes', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']
        
    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    depth = models.IntegerField(default=0)  # 0 para mensajes principales, 1-2 para respuestas
    likes = models.ManyToManyField(User, related_name='message_likes', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']
        
    def __str__(self):
        return self.body[0:50]


class PlantCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Plant Categories'


class PlantGuide(models.Model):
    DIFFICULTY_CHOICES = (
        ('Easy', 'Fácil'),
        ('Medium', 'Intermedio'),
        ('Hard', 'Difícil'),
    )
    
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    categories = models.ManyToManyField(PlantCategory, related_name='plant_guides')
    common_name = models.CharField(max_length=100)
    scientific_name = models.CharField(max_length=100)
    guide_picture = models.ImageField(upload_to='plant_guides/')
    description = models.TextField()
    germination = models.TextField()
    transplanting = models.TextField()
    harvest = models.TextField()
    watering = models.TextField()
    sunlight = models.TextField()
    extra_care = models.TextField()
    difficulty = models.CharField(max_length=50, choices=DIFFICULTY_CHOICES)
    growing_season = models.CharField(max_length=100)
    days_to_harvest = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.common_name
    
    class Meta:
        ordering = ['-updated', '-created']


class CultivationTechnique(models.Model):
    TECHNIQUE_CHOICES = (
        ('Vertical', 'Cultivo Vertical'),
        ('Pared', 'Cultivo en Pared'),
        ('Hidroponía', 'Hidroponía'),
        ('Materiales Reciclados', 'Materiales Reciclados'),
        ('Acuaponía', 'Acuaponía'),
        ('Otro', 'Otro'),
    )
    
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='techniques')
    name = models.CharField(max_length=50, choices=TECHNIQUE_CHOICES)
    title = models.CharField(max_length=100, help_text='A descriptive title for your technique', null=True, blank=True, default='Mi Técnica de Cultivo')
    description = models.TextField(help_text='General description of the cultivation technique')
    setup_instructions = models.TextField(help_text='Step-by-step instructions on how to set up this cultivation system')
    maintenance_tips = models.TextField(help_text='Tips for maintaining the cultivation system')
    recommended_plants = models.TextField(help_text='Types of plants that work well with this technique')
    space_requirements = models.TextField(help_text='Space requirements and ideal locations for this technique')
    difficulty_level = models.CharField(max_length=20, choices=PlantGuide.DIFFICULTY_CHOICES)
    estimated_cost = models.CharField(max_length=100, help_text='Estimated cost range for setting up this system')
    materials_needed = models.TextField(help_text='List of materials needed for this cultivation technique')
    benefits = models.TextField(help_text='Benefits of using this cultivation technique')
    limitations = models.TextField(help_text='Limitations or challenges of this technique')
    main_image = models.ImageField(upload_to='technique_images/', help_text='Main image showing the cultivation technique')
    image_second = models.ImageField(upload_to='technique_images/', blank=True, null=True, help_text='Second image of the technique')
    image_third = models.ImageField(upload_to='technique_images/', blank=True, null=True, help_text='Third image of the technique')
    image_fourth = models.ImageField(upload_to='technique_images/', blank=True, null=True, help_text='Fourth image of the technique')
    likes = models.ManyToManyField(User, related_name='technique_likes', blank=True)
    participants = models.ManyToManyField(User, related_name='technique_participants', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Cultivation Technique'
        verbose_name_plural = 'Cultivation Techniques'
        ordering = ['-created']


class Friendship(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )
    
    from_user = models.ForeignKey(User, related_name='friendships', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='friend_requests', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('from_user', 'to_user')
        ordering = ['-updated']
    
    def __str__(self):
        return f'{self.from_user.username} -> {self.to_user.username} ({self.status})'


class Cultivation3DModel(models.Model):
    TECHNIQUE_CHOICES = [
        ('vertical', 'Cultivo Vertical'),
        ('pared', 'Cultivo en Pared'),
        ('hidroponia', 'Hidroponía'),
        ('reciclados', 'Materiales Reciclados'),
        ('acuaponia', 'Acuaponía'),
    ]
    
    LOCATION_CHOICES = [
        ('interior', 'Interior'),
        ('exterior', 'Exterior'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('generating_image', 'Generando Imagen'),
        ('generating_model', 'Generando Modelo 3D'),
        ('completed', 'Completado'),
        ('error', 'Error'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='models_3d')
    cultivation_technique = models.ForeignKey(CultivationTechnique, on_delete=models.SET_NULL, null=True, blank=True, related_name='models_3d')
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    # Specific fields for 3D modeling
    technique = models.CharField(max_length=20, choices=TECHNIQUE_CHOICES)
    width = models.IntegerField(help_text="Width in centimeters")
    height = models.IntegerField(help_text="Height in centimeters")
    length = models.IntegerField(help_text="Length in centimeters")
    location = models.CharField(max_length=10, choices=LOCATION_CHOICES)
    materials_description = models.TextField()
    extra_specifications = models.TextField(blank=True)
    
    # Fields to store results
    prompt = models.TextField(blank=True)
    generated_image = models.ImageField(upload_to='models3d/images/', blank=True, null=True)
    glb_model = models.FileField(upload_to='models3d/glb/', blank=True, null=True)
    
    # Process status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    error_message = models.TextField(blank=True)
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = '3D Cultivation Model'
        verbose_name_plural = '3D Cultivation Models'
        ordering = ['-created']


class Medal(models.Model):
    """Modelo para las medallas que pueden ganar los usuarios."""
    MEDAL_TYPES = [
        ('perfil', 'Perfil'),
        ('likes', 'Likes'),
        ('influencer', 'Influencer'),
        ('guias', 'Guías'),
        ('tecnicas', 'Técnicas'),
    ]
    
    name = models.CharField(max_length=50)
    medal_type = models.CharField(max_length=20, choices=MEDAL_TYPES, unique=True)
    description = models.TextField()
    image = models.CharField(max_length=100)  # Ruta relativa a la imagen de la medalla
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Medalla'
        verbose_name_plural = 'Medallas'


class UserMedal(models.Model):
    """Modelo para la relación entre usuarios y medallas."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='medals')
    medal = models.ForeignKey(Medal, on_delete=models.CASCADE, related_name='users')
    earned_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'medal')
        verbose_name = 'Medalla de Usuario'
        verbose_name_plural = 'Medallas de Usuarios'
        
    def __str__(self):
        return f"{self.user.username} - {self.medal.name}"