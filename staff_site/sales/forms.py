from django import forms
from backendIntegrations.models import LockPurchaseRequests


class LockPurchaseForm(forms.Form):
    class Meta:
        fields = [
            "status",
            "preferred_type",
            "internal_status",
            "internal_comment",
            "quantity",
            "phone",
            "company",
            "email",
            "fio"
        ]

    STATUS_CHOICES = [
        ('OK', 'Approved'),
        ('FAIL', 'Rejected'),
        ('WAIT', 'Await'),
        ('FINALIZED', 'Finalized'),
        ('CLOSED', 'Closed')
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
        (5, 'SALES_LOCK'),
        (6, 'DELIVERY_LOCK'),
        (7, 'INSTALLED'),
        (8, 'RECALLED'),
        (9, 'STANDBY')

    ]
    TYPE_CHOICES = [
        (1, 'TEST-ONLY'),
        (2, 'CONSUMER-TYPED'),
        (3, 'RETURNED'),
        (4, 'FAULTY')

    ]
    INTERNAL_STATUS = [
        ('IN_PROGRESS', 'In progress - sales'),
        ('HANDED_TO_MAN', 'In progress - transferred to manufacturing'),
        ('ARCHIVE', 'Archived'),
        ('HOLD', 'On hold'),
        ('NEW', 'New')
    ]
    status = forms.ChoiceField(label='Статус', choices=STATUS_CHOICES, required=False,
                                )
    preferred_type = forms.ChoiceField(label='Версия подключения', choices=VERSION_CHOICES, required=False)
    internal_comment = forms.CharField(
        label='Внутренний комментарий для команд Manufacturing и Sales',
        help_text='Комментарий для команды Manufacturing и Sales',
        required=False, max_length=200,
        widget=forms.Textarea(attrs={
            'rows': 2}))
    quantity = forms.IntegerField(
        label='Количество замков',
        max_value=100
    )
    internal_status = forms.ChoiceField(label='Внутренний статус', choices=INTERNAL_STATUS,
                                        required=False,
                                )
    phone = forms.CharField(label='Телефон клиента', max_length=31, required=False)
    company = forms.CharField(label='Компания', max_length=255, required=False)
    email = forms.CharField(label='Email клиента', max_length=255, required=False)
    fio = forms.CharField(label='ФИО Клиента', max_length=255, required=False)
