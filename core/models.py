from django.db import models

class User(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)

class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

class BusinessObject(models.Model):
    name = models.CharField(max_length=100, unique=True)

class AccessRule(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    business_object = models.ForeignKey(BusinessObject, on_delete=models.CASCADE)
    can_create = models.BooleanField(default=False)
    can_read_all = models.BooleanField(default=False)
    can_read_own = models.BooleanField(default=False)
    can_update_all = models.BooleanField(default=False)
    can_update_own = models.BooleanField(default=False)
    can_delete_all = models.BooleanField(default=False)
    can_delete_own = models.BooleanField(default=False)