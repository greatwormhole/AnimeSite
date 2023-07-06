from django.db import models
from dateutil.relativedelta import relativedelta
from datetime import date, datetime

"""
This is module with base classes
It's not supposed to use them without inheritance
"""

class BasePerson(models.Model):

    """
    Base class for all persons in database
    """

    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    date_of_birth = models.DateField()

    @property
    def age(self):
        return relativedelta(date.today(), self.date_of_birth).years

    class Meta():
        abstract = True


class BaseContent(models.Model):

    """
    Base class for all content in database
    """

    image = models.ImageField(upload_to='icons', default='../default_icons/image_missing.jpg')
    name = models.CharField(max_length=250)
    description = models.TextField()
    created = models.DateField()
    rating = models.PositiveSmallIntegerField()

    class Meta:
        abstract = True

class BaseAction(models.Model):
    
    """
    Base class for all user actions in database
    """

    text = models.TextField()
    created = models.DateTimeField(default=datetime.now(), primary_key=True)
    updated = models.DateTimeField(blank=True)
    likes = models.PositiveIntegerField()
    dislikes = models.PositiveIntegerField()

    class Meta:
        abstract = True
        ordering = ['-created']