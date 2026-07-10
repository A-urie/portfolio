from django.db import models

# Create your models here.
from django.db import models
from django.urls import reverse


class Project(models.Model):
    CATEGORY_CHOICES = [
        ('mobile', 'Mobile'),
        ('web', 'Web'),
        ('erp', 'ERP'),
    ]

    title = models.CharField('Titre', max_length=100)
    slug = models.SlugField('Slug', unique=True, help_text="Utilisé dans l'URL, ex: agriscore")
    category = models.CharField('Catégorie', max_length=20, choices=CATEGORY_CHOICES)
    short_description = models.CharField('Description courte', max_length=200)
    description = models.TextField('Description complète')
    thumbnail = models.ImageField('Image (carte)', upload_to='portfolio/', blank=True, null=True)
    cover_image = models.ImageField('Image (détail)', upload_to='portfolio/', blank=True, null=True)
    tech_stack = models.CharField('Technologies', max_length=200, help_text="Ex: Flutter, Dart, Provider")
    github_url = models.URLField('Lien GitHub', blank=True)
    demo_url = models.URLField('Lien démo', blank=True)
    client = models.CharField('Client / Contexte', max_length=100, blank=True, help_text="Ex: Projet académique L2")
    project_date = models.DateField('Date du projet', blank=True, null=True)
    order = models.PositiveIntegerField("Ordre d'affichage", default=0)
    featured = models.BooleanField('Mettre en avant', default=True)

    class Meta:
        ordering = ['order', '-project_date']
        verbose_name = 'Projet'
        verbose_name_plural = 'Projets'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('portfolio:project_detail', kwargs={'slug': self.slug})