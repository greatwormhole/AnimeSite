from django.db import models
from django.contrib.auth.models import User

from .base_models import BaseContent, BasePerson, BaseAction

class Company(BaseContent):

    class Meta(BaseContent.Meta):
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'

class Actor(BasePerson):

    class Meta(BasePerson.Meta):
        verbose_name = 'Актер'
        verbose_name_plural = 'Актеры'

class Author(BasePerson):

    class Meta(BasePerson.Meta):
        verbose_name = 'Автор'
        verbose_name_plural = 'Автор'

class Category(models.Model):
    name=models.CharField(max_length=250)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Manga(BaseContent):

    category = models.ManyToManyField(Category, blank=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta(BaseContent.Meta):
        verbose_name = 'Манга'
        verbose_name_plural = 'Манга'

class Anime(BaseContent):

    category = models.ManyToManyField(Category, blank=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, blank=True)
    actors = models.ManyToManyField(Actor)
    original = models.ForeignKey(Manga, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta(BaseContent.Meta):
        verbose_name = 'Аниме'
        verbose_name_plural = 'Аниме'  

class Profile(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    profile_picture = models.ImageField(upload_to='icons/profile', default='../default_icons/image_missing.png')
    user_manga_favorites = models.ManyToManyField(Manga, blank=True)
    user_anime_favorites = models.ManyToManyField(Anime, blank=True)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

class Comment(BaseAction):

    user = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, blank=True)
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE, blank=True)

    class Meta(BaseAction.Meta):
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

class Review(BaseAction):

    user = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, blank=True)
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE, blank=True)

    class Meta(BaseAction.Meta):
        verbose_name = 'Рецензия'
        verbose_name_plural = 'Рецензии'
