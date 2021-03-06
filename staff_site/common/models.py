from django.contrib.auth.models import User
from django.db import models

# this file contains common models for the whole project
# additional models may be added and should be documented


class ActionTypes(models.Model):
	"""
	This model describes types of actions that can be performed.
	Used for logs only.
	WARNING: MUST BE FILLED OUT INITIALLY
	"""
	act_type = models.CharField(max_length=30, primary_key=True)
	description = models.CharField(max_length=150)

	class Meta:
		managed = False


class ResultTypes(models.Model):
	"""
	This model describes types of results that can happen after a
	certain request or action. Used for logs only.
	WARNING: MUST BE FILLED OUT INITIALLY
	"""
	res_type = models.CharField(max_length=30, primary_key=True)
	description = models.CharField(max_length=150)

	class Meta:
		managed = False


class AccountTypes(models.Model):
	"""
	This model defines types of account types used for permissions
	across the app.
	WARNING: MUST BE FILLED OUT INITIALLY
	"""
	acc_type = models.CharField(max_length=50, primary_key=True)

	class Meta:
		managed = False


class PermissionLevels(models.Model):
	p_level = models.PositiveIntegerField(primary_key=True)
	description = models.CharField(max_length=150, null=True, blank=True)

	class Meta:
		managed = False