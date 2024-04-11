from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, Group, Permission
from custum_fields.models import CountryCode, CityModal, CountryModel, StateModal
import random


class MyUserManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, password=None, **extra_fields):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            **extra_fields,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, first_name, last_name, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email, username, first name,
        last name, and password.
        """
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_user', True)

        return self.create_user(email, username, first_name, last_name, password, **extra_fields)


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    username = models.CharField(max_length=250, unique=True)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    Country_code_number = models.ForeignKey(
        "custum_fields.CountryCode", on_delete=models.CASCADE, blank=True, null=True)
    phone_number = models.IntegerField(blank=True, null=True)

    address = models.CharField(max_length=250, blank=True, null=True)
    city = models.ForeignKey(
        "custum_fields.CityModal", on_delete=models.CASCADE, blank=True, null=True)
    state = models.ForeignKey(
        "custum_fields.StateModal", on_delete=models.CASCADE, blank=True, null=True)
    country = models.ForeignKey(
        "custum_fields.CountryModel", on_delete=models.CASCADE, blank=True, null=True)
    zipcode = models.IntegerField(blank=True, null=True)

    profile_photo = models.ImageField(upload_to='user_profile_photo',blank=True)

    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    created_time = models.TimeField(auto_now_add=True)
    updated_time = models.TimeField(auto_now=True)

    verification_code = models.IntegerField(blank=True, null=True)

    date_of_birth = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_user = models.BooleanField(default=True)

    groups = models.ManyToManyField(
        Group, related_name='groups', related_query_name='groups', blank=True)
    user_permissions = models.ManyToManyField(
        Permission, related_name='permissions', related_query_name='permissions', blank=True)
    # -------------------------------test---------------
    forgot = models.IntegerField(blank=True, null=True)
    is_forgot = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "first_name", "last_name"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @ property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def generate_verification(self):
        code = random.randint(100000, 999999)
        self.verification_code = code
        self.save()
        return code

    def generate_forgot(self):
        code_forgot = random.randint(100000, 999999)
        self.forgot = code_forgot
        self.save()
        return code_forgot
