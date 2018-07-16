# Based on https://github.com/bjldigital/django-randompinfield/blob/master/randompinfield/fields.py
from random import randint

from django.db import models


class RandomPinField(models.CharField):
    """
    Generates a random digit pin
    By default sets length=6
    """
    def __init__(self, length, *args, **kwargs):
        kwargs['blank'] = True
        kwargs['max_length'] = length
        self.length = length
        super(RandomPinField, self).__init__(*args, **kwargs)

    def generate_pin(self):
        """
        Returns a random pin.
        """
        range_start = 10**(self.max_length - 1)
        range_end = (10**self.max_length) - 1

        return str(randint(range_start, range_end))

    def pre_save(self, instance, add):
        value = getattr(instance, self.attname)
        if not value:
            value = self.generate_pin()
            setattr(instance, self.attname, value)
        return value

    def deconstruct(self):
        name, path, args, kwargs = super(RandomPinField, self).deconstruct()
        kwargs['length'] = self.length
        return name, path, args, kwargs
