from django.dispatch import Signal

confirmation_sms_sent = Signal(providing_args=['phone_number'])
