from django.db import models
from django.dispatch import receiver
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save
from apps.accounts.models import AuthUser

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

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Manga(BaseContent):

    categories = models.ManyToManyField(Category, blank=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta(BaseContent.Meta):
        verbose_name = 'Манга'
        verbose_name_plural = 'Манга'

class Anime(BaseContent):

    categories = models.ManyToManyField(Category, blank=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, blank=True)
    actors = models.ManyToManyField(Actor, blank=True)
    original = models.ForeignKey(Manga, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta(BaseContent.Meta):
        verbose_name = 'Аниме'
        verbose_name_plural = 'Аниме'  

class Profile(BasePerson):
    
    user = models.OneToOneField(AuthUser, on_delete=models.CASCADE, primary_key=True)
    profile_picture = models.ImageField(upload_to='icons/profile', default='icons/default_icons/image_missing.jpg')
    user_manga_favorites = models.ManyToManyField(Manga, blank=True)
    user_anime_favorites = models.ManyToManyField(Anime, blank=True)

    @property
    def full_name(self):
        return self.user.username

    class Meta(BasePerson.Meta):
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

class Comment(BaseAction):

    user = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, null=True, blank=True)
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE, null=True, blank=True)

    @property
    def content(self):
        return self.anime if self.anime is not None else self.manga
    
    def __str__(self):
        return f'Комментарий к {self.content} от {self.user}'

    class Meta(BaseAction.Meta):
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        constraints = [
            models.CheckConstraint(
                check=(
                    Q(anime__isnull=True) &
                    Q(manga__isnull=False)
                ) | (
                    Q(anime__isnull=False) &
                    Q(manga__isnull=True)
                ),
                name='One content required for single comment'
            )
        ]

class Review(BaseAction):

    user = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, blank=True)
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE, blank=True)

    @property
    def content(self):
        return self.anime if self.anime is not None else self.manga
    
    def __str__(self):
        return f'Обзор к {self.content} от {self.user}'

    class Meta(BaseAction.Meta):
        verbose_name = 'Рецензия'
        verbose_name_plural = 'Рецензии'

class News(BaseContent):

    class Meta(BaseContent.Meta):
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

@receiver(post_save, sender=AuthUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, first_name='', last_name='')
    else:
        try:
            instance.profile.save()
        except ObjectDoesNotExist:
            Profile.objects.create(user=instance, first_name='', last_name='')