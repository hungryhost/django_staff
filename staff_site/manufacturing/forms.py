from django import forms
from backendIntegrations.models import LockManuals, RegisterLock, RegisterKey


class LockCreateForm(forms.Form):
    VERSION_CHOICES = [
        (1, 'Ethernet'),
        (2, 'Wi-Fi'),
    ]
    FIRMWARE_CHOICES = [
        (1, '1'),
    ]

    STAGE_CHOICES = [
        (1, 'TEST_IN_PROGRESS'),
        (2, 'TEST_OK'),
        (3, 'TEST_FAIL'),
        (4, 'STORAGE'),
        (9, 'STANDBY')

    ]
    TYPE_CHOICES = [
        (1, 'TEST-ONLY'),
        (2, 'CONSUMER-TYPED'),
    ]
    description = forms.CharField(label='Описание замка', max_length=200,
                                  widget = forms.Textarea(attrs={
                                        'rows': 2}))
    manual = forms.ModelChoiceField(label='Инструкция к замку', queryset=LockManuals.objects.all())
    version = forms.ChoiceField(label='Версия подключения', choices=VERSION_CHOICES)
    firmware = forms.ChoiceField(label='Версия ПО', choices=FIRMWARE_CHOICES)
    type = forms.ChoiceField(label='Внутренний тип замка', choices=TYPE_CHOICES)
    stage = forms.ChoiceField(label='Индикатор готовности замка', choices=STAGE_CHOICES)


class LockUpdateManufacturingForm(forms.ModelForm):
    class Meta:
        model = RegisterLock
        fields = [
            'description',
            'current_stage',
            'current_type',
            #'version',
            #'firmware',
            'is_approved'

        ]
    VERSION_CHOICES = [
        (1, 'Ethernet'),
        (2, 'Wi-Fi'),
    ]
    FIRMWARE_CHOICES = [
        (1, '1'),
    ]

    STAGE_CHOICES = [
        (1, 'TEST_IN_PROGRESS'),
        (2, 'TEST_OK'),
        (3, 'TEST_FAIL'),
        (4, 'STORAGE'),
        (9, 'STANDBY')

    ]
    TYPE_CHOICES = [
        (1, 'TEST-ONLY'),
        (2, 'CONSUMER-TYPED'),
        (3, 'RETURNED'),
        (4, 'FAULTY')

    ]
    description = forms.CharField(label='Описание замка', max_length=200,
                                  widget = forms.Textarea(attrs={
                                        'rows': 2}))
    manual = forms.ModelChoiceField(label='Инструкция к замку', queryset=LockManuals.objects.all())

    #version = forms.ChoiceField(label='Версия подключения', choices=VERSION_CHOICES)
    #firmware = forms.ChoiceField(label='Версия ПО', choices=FIRMWARE_CHOICES)
    current_type = forms.ChoiceField(label='Внутренний тип замка', choices=TYPE_CHOICES)
    current_stage = forms.ChoiceField(label='Индикатор готовности замка', choices=STAGE_CHOICES)


class MasterKeyUpdateManufacturingForm(forms.ModelForm):
    class Meta:
        model = RegisterKey
        fields = [
            '_code_data'
        ]