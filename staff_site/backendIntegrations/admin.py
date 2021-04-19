from django.contrib import admin
from django.db.models.base import ModelBase
# Register your models here.
from .models import RegisterCard, RegisterLock, RegisterKey
import backendIntegrations.models as integrated_models
for name, var in integrated_models.__dict__.items():
    if type(var) is ModelBase and var not in [RegisterLock, RegisterKey, RegisterCard]:
        admin.site.register(var)


@admin.register(RegisterLock)
class RegisterLockAdmin(admin.ModelAdmin):
    readonly_fields = ["hash_id", "uuid", "linking_code"]


@admin.register(RegisterKey)
class RegisterKeyAdmin(admin.ModelAdmin):
    readonly_fields = ["code_secure", "hash_code"]


@admin.register(RegisterCard)
class RegisterCardAdmin(admin.ModelAdmin):
    readonly_fields = ["hash_id"]