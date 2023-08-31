from django.db import models

from functools import reduce

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

    image = models.ImageField(upload_to='images/content/manga   ', default='images/default_images/image_missing.jpg')
    categories = models.ManyToManyField(Category, blank=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, blank=True)
    
    @property
    def rating(self):
        reviews = self.reviews.values_list('rate', flat=True)
        return reduce(lambda i, j: i + j, reviews, 0) / len(reviews)

    class Meta(BaseContent.Meta):
        verbose_name = 'Манга'
        verbose_name_plural = 'Манга'

class Anime(BaseContent):

    image = models.ImageField(upload_to='images/content/anime', default='images/default_images/image_missing.jpg')
    categories = models.ManyToManyField(Category, blank=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, blank=True)
    actors = models.ManyToManyField(Actor, blank=True)
    original = models.ForeignKey(Manga, on_delete=models.SET_NULL, null=True, blank=True)
    
    @property
    def rating(self):
        reviews = self.reviews.values_list('rate', flat=True)
        return reduce(lambda i, j: i + j, reviews, 0) / len(reviews)

    class Meta(BaseContent.Meta):
        verbose_name = 'Аниме'
        verbose_name_plural = 'Аниме'  

class Profile(BasePerson):
    
    first_name = models.CharField(max_length=120, default='')
    last_name = models.CharField(max_length=120, default='')
    user = models.OneToOneField(AuthUser, on_delete=models.CASCADE, primary_key=True)
    profile_picture = models.ImageField(upload_to='images/profile', default='images/default_icons/image_missing.jpg')
    user_manga_favorites = models.ManyToManyField(Manga, blank=True, related_name='manga_favorites')
    user_anime_favorites = models.ManyToManyField(Anime, blank=True, related_name='anime_favorites')
    user_manga_reviews = models.ManyToManyField(Manga, through='MangaReview', blank=True, related_name='manga_reviews')
    user_anime_reviews = models.ManyToManyField(Anime, through='AnimeReview', blank=True, related_name='anime_reviews')

    @property
    def full_name(self):
        return self.user.username

    class Meta(BasePerson.Meta):
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

class AnimeComment(BaseAction):

    user = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'Комментарий к аниме от {self.user}'

    class Meta(BaseAction.Meta):
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        
class MangaComment(BaseAction):

    user = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'Комментарий к манге от {self.user}'

    class Meta(BaseAction.Meta):
        verbose_name = 'Комментарий к манге'
        verbose_name_plural = 'Комментарии к манге'

class AnimeReview(BaseAction):

    user = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, related_name='reviews')
    rate = models.PositiveSmallIntegerField()
    
    def __str__(self):
        return f'Обзор к аниме от {self.user}'

    class Meta(BaseAction.Meta):
        verbose_name = 'Рецензия к аниме'
        verbose_name_plural = 'Рецензии к аниме'
        
class MangaReview(BaseAction):

    user = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE, related_name='reviews')
    rate = models.PositiveSmallIntegerField()
    
    def __str__(self):
        return f'Обзор к манге {self.manga} от {self.user}'

    class Meta(BaseAction.Meta):
        verbose_name = 'Рецензия к манге'
        verbose_name_plural = 'Рецензии к манге'
        constraints = [
            models.CheckConstraint(
                check=models.Q(rate__gte=0) & models.Q(rate__lte=10),
                name='Оценка должна быть от 0 до 10',
            ),
        ]

class News(BaseContent):

    class Meta(BaseContent.Meta):
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
