# Generated by Django 5.2 on 2025-05-06 20:47

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_message_depth_message_parent'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cultivationtechnique',
            options={'ordering': ['-created'], 'verbose_name': 'Cultivation Technique', 'verbose_name_plural': 'Cultivation Techniques'},
        ),
        migrations.RemoveField(
            model_name='cultivationtechnique',
            name='step_images',
        ),
        migrations.AddField(
            model_name='cultivationtechnique',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='techniques', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='cultivationtechnique',
            name='image_fourth',
            field=models.ImageField(blank=True, help_text='Fourth image of the technique', null=True, upload_to='technique_images/'),
        ),
        migrations.AddField(
            model_name='cultivationtechnique',
            name='image_second',
            field=models.ImageField(blank=True, help_text='Second image of the technique', null=True, upload_to='technique_images/'),
        ),
        migrations.AddField(
            model_name='cultivationtechnique',
            name='image_third',
            field=models.ImageField(blank=True, help_text='Third image of the technique', null=True, upload_to='technique_images/'),
        ),
        migrations.AddField(
            model_name='cultivationtechnique',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='technique_likes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='cultivationtechnique',
            name='participants',
            field=models.ManyToManyField(blank=True, related_name='technique_participants', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='cultivationtechnique',
            name='title',
            field=models.CharField(blank=True, default='Mi Técnica de Cultivo', help_text='A descriptive title for your technique', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='cultivationtechnique',
            name='name',
            field=models.CharField(choices=[('Vertical', 'Vertical'), ('Wall-mounted', 'Wall-mounted'), ('Hydroponics', 'Hydroponics'), ('Recycled Materials', 'Recycled Materials'), ('Aquaponics', 'Aquaponics'), ('Other', 'Other')], max_length=50),
        ),
    ]
