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
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
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
        ('Vertical', 'Vertical'),
        ('Wall-mounted', 'Wall-mounted'),
        ('Hydroponics', 'Hydroponics'),
        ('Recycled Materials', 'Recycled Materials'),
        ('Aquaponics', 'Aquaponics'),
        ('Other', 'Other'),
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
