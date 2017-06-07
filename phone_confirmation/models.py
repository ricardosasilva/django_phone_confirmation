from __future__ import unicode_literals

import random
from datetime import timedelta

from django.conf import settings
from django.core import signing
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

from sendsms import api

phone_settings = getattr(settings, 'PHONE_CONFIRMATION', {})

SALT = getattr(phone_settings, 'SALT', 'phonenumber')
ACTIVATION_MINUTES = getattr(phone_settings, 'ACTIVATION_MINUTES', 15)
SMS_TEMPLATE = getattr(phone_settings, 'SMS_TEMPLATE', 'phone_confirmation/message.txt')
FROM_NUMBER = getattr(phone_settings, 'FROM_NUMBER', '')
MAX_CONFIRMATIONS = getattr(phone_settings, 'MAX_CONFIRMATIONS', 10)


def random_confirmation_code():
    return '{0:04d}'.format(random.SystemRandom().randint(1, 9999))


class PhoneConfirmationManager(models.Manager):
    """Manager for PhoneConfirmation model."""

    def validate_key(self, activation_key):
        """
        Check if the activation_key is valid and not expired.

        Return phone number if it is valid or None otherwise.
        """
        try:
            phone_number = signing.loads(
                activation_key,
                salt=SALT,
                max_age=ACTIVATION_MINUTES * 60
            )
            return phone_number.get('phone_number')
        except signing.BadSignature:
            return None

    def get_confirmation_code(self, phone_number, code):
        """Get the PhoneConfirmation for the phone number and code."""
        time_threshold = timezone.now() - timedelta(minutes=ACTIVATION_MINUTES)
        return self.get_queryset().filter(created_at__gte=time_threshold,
                                          phone_number=phone_number,
                                          code=code).order_by('-created_at').first()

    def clear_phone_number_confirmations(self, phone_number):
        """Remove all confirmations for the phone number."""
        self.get_queryset().filter(phone_number=phone_number).delete()


class PhoneConfirmation(models.Model):
    """Store confirmation codes for phone number."""

    created_at = models.DateTimeField(auto_now_add=True)
    phone_number = PhoneNumberField(db_index=True)
    code = models.CharField(max_length=6, default=random_confirmation_code)
    objects = PhoneConfirmationManager()

    class Meta:
        index_together = (('created_at', 'phone_number', 'code'), ('phone_number', 'code'))

    @property
    def activation_key(self):
        return self._get_activation_key(self.phone_number)

    def __str__(self):
        return str(self.phone_number)

    @staticmethod
    def _get_activation_key(phone_number):
        return signing.dumps(
            obj={'phone_number': str(phone_number)},
            salt=SALT
        )

    def send_sms(self, request=None):
        message = render_to_string(template_name=SMS_TEMPLATE,
                                   context={"code": self.code},
                                   request=request)
        api.send_sms(body=message,
                     from_phone=FROM_NUMBER,
                     to=[str(self.phone_number)])


@receiver(post_save, sender=PhoneConfirmation)
def post_save_person_receiver(sender, instance, created, **kwargs):
    if created:
        if PhoneConfirmation.objects.filter(phone_number=instance.phone_number).count() > MAX_CONFIRMATIONS:
            PhoneConfirmation.objects.filter(phone_number=instance.phone_number).order_by('created_at').first().delete()
        instance.send_sms()
