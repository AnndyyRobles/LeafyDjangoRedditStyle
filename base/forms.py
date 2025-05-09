from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Room, User, Cultivation3DModel

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar' ,'name', 'username', 'email', 'bio']

class Cultivation3DModelForm(ModelForm):
    class Meta:
        model = Cultivation3DModel
        fields = ['title', 'description', 'technique', 'width', 'height', 'length', 
                 'location', 'materials_description', 'extra_specifications']
        exclude = ['user', 'cultivation_technique', 'prompt', 'generated_image', 
                  'glb_model', 'status', 'error_message']