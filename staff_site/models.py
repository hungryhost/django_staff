# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class ActionResultTypes(models.Model):
    res_type = models.CharField(primary_key=True, max_length=30)
    description = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'action_result_types'


class ActionTypes(models.Model):
    act_type = models.CharField(primary_key=True, max_length=30)
    description = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'action_types'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class Bookings(models.Model):
    booked_from = models.DateTimeField()
    booked_until = models.DateTimeField()
    price = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    client_email = models.CharField(max_length=254)
    number_of_clients = models.IntegerField()
    status = models.CharField(max_length=100)
    is_deleted = models.BooleanField()
    booked_by = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    booked_property = models.ForeignKey('Properties', models.DO_NOTHING)
    cancelled_reason = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'bookings'


class CitiesLightCity(models.Model):
    name_ascii = models.CharField(max_length=200)
    slug = models.CharField(max_length=50)
    geoname_id = models.IntegerField(unique=True, blank=True, null=True)
    alternate_names = models.TextField(blank=True, null=True)
    name = models.CharField(max_length=200)
    display_name = models.CharField(max_length=200)
    search_names = models.TextField()
    latitude = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    longitude = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    region = models.ForeignKey('CitiesLightRegion', models.DO_NOTHING, blank=True, null=True)
    country = models.ForeignKey('CitiesLightCountry', models.DO_NOTHING)
    population = models.BigIntegerField(blank=True, null=True)
    feature_code = models.CharField(max_length=10, blank=True, null=True)
    timezone = models.CharField(max_length=40, blank=True, null=True)
    subregion = models.ForeignKey('CitiesLightSubregion', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cities_light_city'
        unique_together = (('region', 'subregion', 'slug'), ('region', 'subregion', 'name'),)


class CitiesLightCountry(models.Model):
    name_ascii = models.CharField(max_length=200)
    slug = models.CharField(max_length=50)
    geoname_id = models.IntegerField(unique=True, blank=True, null=True)
    alternate_names = models.TextField(blank=True, null=True)
    code2 = models.CharField(unique=True, max_length=2, blank=True, null=True)
    code3 = models.CharField(unique=True, max_length=3, blank=True, null=True)
    continent = models.CharField(max_length=2)
    tld = models.CharField(max_length=5)
    phone = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'cities_light_country'


class CitiesLightRegion(models.Model):
    name_ascii = models.CharField(max_length=200)
    geoname_id = models.IntegerField(unique=True, blank=True, null=True)
    alternate_names = models.TextField(blank=True, null=True)
    name = models.CharField(max_length=200)
    display_name = models.CharField(max_length=200)
    geoname_code = models.CharField(max_length=50, blank=True, null=True)
    country = models.ForeignKey(CitiesLightCountry, models.DO_NOTHING)
    slug = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'cities_light_region'
        unique_together = (('country', 'slug'), ('country', 'name'),)


class CitiesLightSubregion(models.Model):
    name = models.CharField(max_length=200)
    name_ascii = models.CharField(max_length=200)
    slug = models.CharField(max_length=50)
    geoname_id = models.IntegerField(unique=True, blank=True, null=True)
    alternate_names = models.TextField(blank=True, null=True)
    display_name = models.CharField(max_length=200)
    geoname_code = models.CharField(max_length=50, blank=True, null=True)
    country = models.ForeignKey(CitiesLightCountry, models.DO_NOTHING)
    region = models.ForeignKey(CitiesLightRegion, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cities_light_subregion'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    action_flag = models.PositiveSmallIntegerField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class LockAccessLogs(models.Model):
    lock = models.IntegerField()
    hash_code = models.CharField(max_length=256)
    try_time = models.DateTimeField()
    result = models.BooleanField()
    is_failed = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'lock_access_logs'


class LockApiKeys(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    prefix = models.CharField(unique=True, max_length=8)
    hashed_key = models.CharField(max_length=100)
    created = models.DateTimeField()
    name = models.CharField(max_length=50)
    revoked = models.BooleanField()
    expiry_date = models.DateTimeField(blank=True, null=True)
    lock = models.ForeignKey('RegisterLock', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'lock_api_keys'


class LockCatalogImages(models.Model):
    image = models.CharField(max_length=100)
    is_main = models.BooleanField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    lock_info = models.ForeignKey('LockCatalogInfo', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'lock_catalog_images'


class LockCatalogInfo(models.Model):
    name = models.CharField(max_length=500)
    description = models.CharField(max_length=3000)
    price = models.FloatField()
    delivery = models.BooleanField()
    installation_included = models.BooleanField()
    is_available = models.BooleanField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'lock_catalog_info'


class LockCatalogStorageAvailability(models.Model):
    quantity = models.IntegerField()
    city = models.ForeignKey('SupportedCities', models.DO_NOTHING)
    lock_info = models.ForeignKey(LockCatalogInfo, models.DO_NOTHING)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'lock_catalog_storage_availability'


class LockPurchaseRequests(models.Model):
    email = models.CharField(max_length=255)
    fio = models.CharField(max_length=255)
    phone = models.CharField(max_length=31)
    comment = models.CharField(max_length=500)
    company = models.CharField(max_length=255)
    quantity = models.IntegerField()
    selected_lock = models.ForeignKey(LockCatalogInfo, models.DO_NOTHING, blank=True, null=True)
    status = models.CharField(max_length=20)
    final_price = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lock_purchase_requests'


class LockPurchaseShippingAddress(models.Model):
    country = models.CharField(max_length=100)
    street = models.CharField(max_length=255)
    building = models.CharField(max_length=20)
    floor = models.CharField(max_length=20)
    number = models.CharField(max_length=30)
    zip_code = models.CharField(max_length=10)
    directions_description = models.CharField(max_length=500)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    city = models.ForeignKey('SupportedCities', models.DO_NOTHING)
    shipping_ticket = models.OneToOneField(LockPurchaseRequests, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lock_purchase_shipping_address'


class LrUserAddressTypes(models.Model):
    addr_type = models.CharField(primary_key=True, max_length=40)
    description = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lr_user_address_types'


class LrUserDocumentTypes(models.Model):
    doc_type = models.CharField(primary_key=True, max_length=40)
    description = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lr_user_document_types'


class LrUserPhoneTypes(models.Model):
    phone_type = models.CharField(primary_key=True, max_length=20)
    description = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lr_user_phone_types'


class OrganisationAddresses(models.Model):
    country = models.CharField(max_length=2)
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    building = models.CharField(max_length=20)
    floor = models.CharField(max_length=20)
    number = models.CharField(max_length=30)
    zip_code = models.CharField(max_length=10)
    crm_region = models.CharField(db_column='CRM_REGION', max_length=3)  # Field name made lowercase.
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    organisation = models.OneToOneField('Organisations', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'organisation_addresses'


class OrganisationApiKeys(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    prefix = models.CharField(unique=True, max_length=8)
    hashed_key = models.CharField(max_length=100)
    created = models.DateTimeField()
    name = models.CharField(max_length=50)
    revoked = models.BooleanField()
    expiry_date = models.DateTimeField(blank=True, null=True)
    organisation = models.ForeignKey('Organisations', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'organisation_api_keys'


class OrganisationInviteCodes(models.Model):
    secret_code = models.TextField()
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    created_by_member = models.ForeignKey('OrganisationMembers', models.DO_NOTHING)
    organisation = models.ForeignKey('Organisations', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'organisation_invite_codes'


class OrganisationInviteLinks(models.Model):
    secret_link = models.TextField()
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    created_by_member = models.ForeignKey('OrganisationMembers', models.DO_NOTHING)
    organisation = models.ForeignKey('Organisations', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'organisation_invite_links'


class OrganisationMembers(models.Model):
    is_creator = models.BooleanField()
    can_add_properties = models.BooleanField()
    can_delete_properties = models.BooleanField()
    can_book_properties = models.BooleanField()
    recursive_ownership = models.BooleanField()
    can_add_members = models.BooleanField()
    can_remove_members = models.BooleanField()
    can_manage_members = models.BooleanField()
    joined_with_code = models.BooleanField()
    joined_with_link = models.BooleanField()
    added_by_user_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    organisation = models.ForeignKey('Organisations', models.DO_NOTHING)
    user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'organisation_members'
        unique_together = (('organisation', 'user'),)


class OrganisationProperties(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    added_by = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    organisation = models.ForeignKey('Organisations', models.DO_NOTHING)
    premises = models.ForeignKey('Properties', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'organisation_properties'
        unique_together = (('premises', 'organisation'),)


class Organisations(models.Model):
    name = models.CharField(max_length=255)
    website = models.CharField(max_length=255)
    description = models.CharField(max_length=500)
    is_confirmed = models.BooleanField()
    active = models.BooleanField()
    lr_crm_id = models.TextField(db_column='LR_CRM_ID')  # Field name made lowercase.
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'organisations'


class Properties(models.Model):
    title = models.CharField(max_length=50)
    body = models.TextField()
    price = models.PositiveIntegerField(blank=True, null=True)
    active = models.BooleanField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    client_greeting_message = models.CharField(max_length=500)
    requires_additional_confirmation = models.BooleanField()
    booking_type = models.IntegerField()
    property_type = models.ForeignKey('PropertyTypes', models.DO_NOTHING)
    visibility = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'properties'


class PropertiesPropertylog(models.Model):
    action = models.CharField(max_length=300)
    act_time = models.DateTimeField()
    result = models.BooleanField()
    listed_prop = models.ForeignKey(Properties, models.DO_NOTHING)
    user = models.ForeignKey('Users', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'properties_propertylog'


class PropertyAddress(models.Model):
    country = models.CharField(max_length=100)
    street = models.CharField(max_length=255)
    building = models.CharField(max_length=20)
    floor = models.CharField(max_length=20)
    number = models.CharField(max_length=30)
    zip_code = models.CharField(max_length=10)
    directions_description = models.CharField(max_length=500)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    city = models.ForeignKey('SupportedCities', models.DO_NOTHING)
    premises = models.OneToOneField(Properties, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'property_address'


class PropertyAvailability(models.Model):
    open_days = models.CharField(max_length=7)
    booking_interval = models.IntegerField()
    maximum_number_of_clients = models.IntegerField()
    available_from = models.TimeField(blank=True, null=True)
    available_until = models.TimeField(blank=True, null=True)
    available_hours = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    premises = models.OneToOneField(Properties, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'property_availability'


class PropertyAvailabilityExceptions(models.Model):
    exception_datetime_start = models.DateTimeField()
    exception_datetime_end = models.DateTimeField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    parent_availability = models.ForeignKey(PropertyAvailability, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'property_availability_exceptions'


class PropertyGroupMembers(models.Model):
    is_creator = models.BooleanField()
    can_add_properties = models.BooleanField()
    can_delete_properties = models.BooleanField()
    can_book_properties = models.BooleanField()
    recursive_ownership = models.BooleanField()
    can_add_members = models.BooleanField()
    can_remove_members = models.BooleanField()
    can_manage_members = models.BooleanField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    group = models.ForeignKey('PropertyGroups', models.DO_NOTHING)
    user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    added_by_owner_id = models.IntegerField(blank=True, null=True)
    added_by_user_id = models.IntegerField(blank=True, null=True)
    joined_with_code = models.BooleanField()
    joined_with_link = models.BooleanField()
    can_delete_group = models.BooleanField()
    can_update_info = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'property_group_members'
        unique_together = (('user', 'group'),)


class PropertyGroupProperties(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    group = models.ForeignKey('PropertyGroups', models.DO_NOTHING)
    premises = models.ForeignKey(Properties, models.DO_NOTHING)
    added_by = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'property_group_properties'


class PropertyGroups(models.Model):
    description = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    title = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'property_groups'


class PropertyImages(models.Model):
    image = models.CharField(max_length=100, blank=True, null=True)
    uploaded_at = models.DateTimeField()
    is_main = models.BooleanField()
    premises = models.ForeignKey(Properties, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'property_images'


class PropertyLocks(models.Model):
    description = models.CharField(max_length=200)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    lock = models.ForeignKey('RegisterLock', models.DO_NOTHING)
    property = models.ForeignKey(Properties, models.DO_NOTHING)
    added_by = models.ForeignKey('Users', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'property_locks'


class PropertyOwnership(models.Model):
    visibility = models.IntegerField()
    is_creator = models.BooleanField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    permission_level = models.ForeignKey('PropertyPermissionLevels', models.DO_NOTHING)
    premises = models.ForeignKey(Properties, models.DO_NOTHING)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    can_add_bookings = models.BooleanField()
    can_add_locks = models.BooleanField()
    can_add_owners = models.BooleanField()
    can_add_to_group = models.BooleanField()
    can_add_to_organisation = models.BooleanField()
    can_delete = models.BooleanField()
    can_delete_locks = models.BooleanField()
    can_delete_owners = models.BooleanField()
    can_edit = models.BooleanField()
    can_manage_bookings = models.BooleanField()
    can_manage_locks = models.BooleanField()
    can_manage_owners = models.BooleanField()
    can_add_images = models.BooleanField()
    can_delete_images = models.BooleanField()
    is_super_owner = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'property_ownership'


class PropertyPermissionLevels(models.Model):
    p_level = models.PositiveIntegerField(primary_key=True)
    description = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'property_permission_levels'


class PropertyTypes(models.Model):
    property_type = models.AutoField(primary_key=True)
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'property_types'


class RegisterCard(models.Model):
    card_id = models.CharField(max_length=66, blank=True, null=True)
    is_master = models.BooleanField()
    lock = models.ForeignKey('RegisterLock', models.DO_NOTHING)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    field_card_data = models.BinaryField(db_column='_card_data')  # Field renamed because it started with '_'.
    hash_id = models.CharField(max_length=256)

    class Meta:
        managed = False
        db_table = 'register_card'


class RegisterKey(models.Model):
    hash_code = models.CharField(max_length=256)
    access_start = models.DateTimeField()
    access_stop = models.DateTimeField()
    lock = models.ForeignKey('RegisterLock', models.DO_NOTHING)
    code_secure = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    created_manually = models.BooleanField()
    field_code_data = models.BinaryField(db_column='_code_data')  # Field renamed because it started with '_'.
    code = models.CharField(max_length=66, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'register_key'


class RegisterLock(models.Model):
    uuid = models.CharField(unique=True, max_length=32)
    description = models.TextField()
    is_on = models.BooleanField()
    is_approved = models.BooleanField()
    last_echo = models.DateTimeField()
    firmware = models.IntegerField()
    linking_code = models.TextField(unique=True, blank=True, null=True)
    version = models.IntegerField()
    hash_id = models.CharField(unique=True, max_length=256)

    class Meta:
        managed = False
        db_table = 'register_lock'


class RegisterLockIpAddresses(models.Model):
    private_ip = models.CharField(max_length=255)
    lock = models.ForeignKey(RegisterLock, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'register_lock_ip_addresses'


class RestFrameworkApiKeyApikey(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    created = models.DateTimeField()
    name = models.CharField(max_length=50)
    revoked = models.BooleanField()
    expiry_date = models.DateTimeField(blank=True, null=True)
    hashed_key = models.CharField(max_length=100)
    prefix = models.CharField(unique=True, max_length=8)

    class Meta:
        managed = False
        db_table = 'rest_framework_api_key_apikey'


class SupportMessages(models.Model):
    title = models.CharField(max_length=255)
    message = models.CharField(max_length=1000)
    user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'support_messages'


class SupportedCities(models.Model):
    name = models.CharField(primary_key=True, max_length=255)
    city = models.ForeignKey(CitiesLightCity, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'supported_cities'


class TokenBlacklistBlacklistedtoken(models.Model):
    blacklisted_at = models.DateTimeField()
    token = models.OneToOneField('TokenBlacklistOutstandingtoken', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'token_blacklist_blacklistedtoken'


class TokenBlacklistOutstandingtoken(models.Model):
    token = models.TextField()
    created_at = models.DateTimeField(blank=True, null=True)
    expires_at = models.DateTimeField()
    jti = models.CharField(unique=True, max_length=255)
    user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'token_blacklist_outstandingtoken'


class UserAvailablePlans(models.Model):
    code = models.CharField(primary_key=True, max_length=255)
    description = models.CharField(max_length=500)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'user_available_plans'


class UserAvatars(models.Model):
    image = models.CharField(max_length=100, blank=True, null=True)
    is_deleted = models.BooleanField()
    uploaded_at = models.DateTimeField()
    account = models.ForeignKey('Users', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'user_avatars'


class UserBillingAddresses(models.Model):
    addr_country = models.CharField(max_length=100, blank=True, null=True)
    addr_city = models.CharField(max_length=100, blank=True, null=True)
    addr_street_1 = models.CharField(max_length=100, blank=True, null=True)
    addr_street_2 = models.CharField(max_length=100, blank=True, null=True)
    addr_building = models.CharField(max_length=20, blank=True, null=True)
    addr_floor = models.CharField(max_length=20, blank=True, null=True)
    addr_number = models.CharField(max_length=30, blank=True, null=True)
    zip_code = models.CharField(max_length=10)
    addr_is_active = models.BooleanField()
    account = models.ForeignKey('Users', models.DO_NOTHING)
    addr_type = models.ForeignKey(LrUserAddressTypes, models.DO_NOTHING)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'user_billing_addresses'


class UserDocuments(models.Model):
    doc_serial = models.PositiveIntegerField(unique=True, blank=True, null=True)
    doc_number = models.PositiveIntegerField(unique=True, blank=True, null=True)
    doc_issued_at = models.DateField(blank=True, null=True)
    doc_issued_by = models.CharField(max_length=100, blank=True, null=True)
    doc_is_confirmed = models.BooleanField()
    account = models.ForeignKey('Users', models.DO_NOTHING)
    doc_type = models.ForeignKey(LrUserDocumentTypes, models.DO_NOTHING)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'user_documents'


class UserFavoredProperties(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    property = models.ForeignKey(Properties, models.DO_NOTHING)
    user = models.ForeignKey('Users', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'user_favored_properties'


class UserKycInfo(models.Model):
    kys_status = models.CharField(max_length=10)
    kyc_last_performed = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_kyc_info'


class UserPhones(models.Model):
    phone_number = models.CharField(max_length=13)
    is_deleted = models.BooleanField()
    account = models.ForeignKey('Users', models.DO_NOTHING)
    phone_type = models.ForeignKey(LrUserPhoneTypes, models.DO_NOTHING)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'user_phones'


class UserPlanRequests(models.Model):
    status_changed_by = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    client = models.ForeignKey('Users', models.DO_NOTHING)
    requested_plan = models.ForeignKey(UserAvailablePlans, models.DO_NOTHING, blank=True, null=True)
    status_changed_reason = models.CharField(max_length=255)
    status = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'user_plan_requests'


class UserPlans(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    plan = models.ForeignKey(UserAvailablePlans, models.DO_NOTHING)
    client = models.ForeignKey('Users', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'user_plans'


class UserTripMembers(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    trip = models.ForeignKey('UserTrips', models.DO_NOTHING)
    user = models.ForeignKey('Users', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'user_trip_members'


class UserTripProperties(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    property = models.ForeignKey(Properties, models.DO_NOTHING)
    trip = models.ForeignKey('UserTrips', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'user_trip_properties'


class UserTrips(models.Model):
    title = models.CharField(max_length=50)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'user_trips'


class Users(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    email = models.CharField(unique=True, max_length=64)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    bio = models.CharField(max_length=500)
    dob = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1)
    timezone = models.CharField(max_length=63)
    is_active = models.BooleanField()
    is_staff = models.BooleanField()
    is_admin = models.BooleanField()
    two_factor_auth = models.BooleanField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    email_confirmed = models.BooleanField()
    additional_info = models.CharField(max_length=1024)
    client_rating = models.CharField(max_length=15)
    is_banned = models.BooleanField()
    last_password_update = models.DateTimeField()
    phone_confirmed = models.BooleanField()
    tos_version = models.CharField(max_length=20, blank=True, null=True)
    phone = models.CharField(max_length=31)
    use_work_email_incbookings = models.BooleanField()
    use_work_email_outbookings = models.BooleanField()
    work_email = models.CharField(unique=True, max_length=64, blank=True, null=True)
    show_main_email_in_contact_info = models.BooleanField()
    show_work_email_in_contact_info = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'users'


class UsersBannedInfo(models.Model):
    reason = models.CharField(max_length=500)
    employee_id = models.IntegerField()
    expiration = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    banned_user = models.ForeignKey(Users, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users_banned_info'


class UsersGroups(models.Model):
    customuser = models.ForeignKey(Users, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'users_groups'
        unique_together = (('customuser', 'group'),)


class UsersUserPermissions(models.Model):
    customuser = models.ForeignKey(Users, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'users_user_permissions'
        unique_together = (('customuser', 'permission'),)
