from django.db import models
from dateutil.relativedelta import relativedelta
from datetime import date, datetime

"""
This is module with base classes
It's not supposed to use them without inheritance
"""

class BasePerson(models.Model):

    """
    Base class for all person-related models in database
    """

    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    date_of_birth = models.DateField(blank=True, null=True)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}' if '' not in (self.first_name, self.last_name) else 'MissingName'

    def __str__(self):
        return self.full_name

    @property
    def age(self):
        return relativedelta(date.today(), self.date_of_birth).years

    class Meta():
        abstract = True


class BaseContent(models.Model):

    """
    Base class for all content in database
    """

    name = models.CharField(max_length=250, unique=True)
    description = models.TextField(blank=True, null=True)
    created = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return self.name

    class Meta:
        abstract = True

class BaseAction(models.Model):
    
    """
    Base class for all user actions in database
    """

    text = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, blank=True)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)

    class Meta:
        abstract = True
        ordering = ['-created']