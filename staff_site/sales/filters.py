import django_filters
from backendIntegrations.models import LockPurchaseRequests
from django import forms


class RequestFilter(django_filters.FilterSet):
	INTERNAL_STATUS = [
		('IN_PROGRESS', 'In progress - sales'),
		('HANDED_TO_MAN', 'In progress - manufacturing'),
		('ARCHIVE', 'Archived'),
		('HOLD', 'On hold'),
		('NEW', 'New')
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
	CHOICES = [
		('OK', 'Approved'),
		('FAIL', 'Rejected'),
		('WAIT', 'Await'),
		('FINALIZED', 'Finalized'),
		('CLOSED', 'Closed')
	]
	internal_status = django_filters.ChoiceFilter(
		choices=INTERNAL_STATUS,
		label='Internal Status'
		#lookup_expr='iexact'
	)
	preferred_type = django_filters.ChoiceFilter(
		choices=VERSION_CHOICES,
		label='Preferred Type'
		#lookup_expr='iexact'
	)
	fio = django_filters.CharFilter(lookup_expr='icontains')
	phone = django_filters.CharFilter(lookup_expr='icontains')
	email = django_filters.CharFilter(lookup_expr='icontains')
	company = django_filters.CharFilter(lookup_expr='icontains')

	status = django_filters.ChoiceFilter(
		choices=CHOICES,
		label='External status'
		#lookup_expr='iexact'
	)

	class Meta:
		model = LockPurchaseRequests
		fields = [
			'internal_status',
			'status',
			'preferred_type',
			'fio',
			'phone',
			'email',
			'company'
		]