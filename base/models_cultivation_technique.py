# Modelo para técnicas de cultivo

class CultivationTechnique(models.Model):
    TECHNIQUE_CHOICES = (
        ('Vertical', 'Cultivo Vertical'),
        ('Pared', 'Cultivo en Pared'),
        ('Hidroponía', 'Hidroponía'),
        ('Materiales Reciclados', 'Materiales Reciclados'),
        ('Acuaponía', 'Acuaponía'),
    )
    
    name = models.CharField(max_length=50, choices=TECHNIQUE_CHOICES, unique=True)
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
    step_images = models.ImageField(upload_to='technique_steps/', blank=True, null=True, help_text='Additional images showing setup steps')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Cultivation Technique'
        verbose_name_plural = 'Cultivation Techniques'
