from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from phone_confirmation.models import PhoneConfirmation


class ConfirmationSerializer(serializers.ModelSerializer):

    class Meta:
        model = PhoneConfirmation
        fields = ('phone_number',)


class ActivationKeySerializer(serializers.ModelSerializer):

    class Meta:
        model = PhoneConfirmation
        fields = ('phone_number', 'code', 'activation_key')
        extra_kwargs = {
            'phone_number': {'write_only': True},
            'code': {'write_only': True},
            'activation_key': {'read_only': True}
        }

    def is_valid(self, raise_exception=False):
        is_valid = super(ActivationKeySerializer, self).is_valid(raise_exception=raise_exception)
        self.instance = self.Meta.model.objects.get_confirmation_code(phone_number=self.validated_data['phone_number'],
                                                                      code=self.validated_data['code'])
        self.Meta.model.objects.clear_phone_number_confirmations(phone_number=self.validated_data['phone_number'])

        if is_valid and not self.instance:
            raise serializers.ValidationError({"error": _("The code or phone number are invalid.")})
        return is_valid
