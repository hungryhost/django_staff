import django_filters
from backendIntegrations.models import RegisterLock
from django import forms


class LockFilter(django_filters.FilterSet):
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
	firmware = django_filters.ChoiceFilter(
		choices=FIRMWARE_CHOICES,
		label='Firmware'

	)
	version = django_filters.ChoiceFilter(
		choices=VERSION_CHOICES,
		label='Version'
	)
	is_approved = django_filters.BooleanFilter(
		lookup_expr='iexact'
	)
	current_type = django_filters.ChoiceFilter(
		choices=TYPE_CHOICES
	)
	current_stage = django_filters.ChoiceFilter(
		choices=STAGE_CHOICES
	)
	id = django_filters.NumberFilter(lookup_expr='exact')
	hash_id = django_filters.CharFilter(lookup_expr='exact')
	uuid = django_filters.UUIDFilter(lookup_expr='exact')
	description = django_filters.CharFilter(lookup_expr='icontains')

	class Meta:
		model = RegisterLock
		fields = [
			'description',
			'id',
			'hash_id',
			'uuid',
			'firmware',
			'version',
			'is_approved',
			'current_type',
			'current_stage'
		]