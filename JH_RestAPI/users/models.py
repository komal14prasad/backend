from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager
from JH_RestAPI import settings
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator


class EmploymentStatus(models.Model):
    value = models.CharField(max_length=20, default='N/A')

    def __str__(self):
        return self.value


class EmploymentAuth(models.Model):
    value = models.CharField(max_length=20, null=False)

    def __str__(self):
        return self.value


class User(AbstractUser):
    objects = UserManager()
    email = models.EmailField(('email address'), unique=True)
    approved = models.BooleanField(default=False, null=False)
    activation_key = models.TextField(null=True, blank=True)
    key_expires = models.DateTimeField(null=True, blank=True)
    forgot_password_key = models.TextField(null=True, blank=True)
    forgot_password_key_expires = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = ('user')
        verbose_name_plural = ('users')
        db_table = 'auth_user'
        swappable = 'AUTH_USER_MODEL'

# Create your models here.


class Profile(models.Model):
    User = get_user_model()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gmail_last_update_time = models.IntegerField(default=0)
    is_gmail_read_ok = models.BooleanField(default=True)
    linkedin_info = models.TextField(null=True, blank=True)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('N', 'None'),
    )
    gender = models.CharField(
        max_length=1, choices=GENDER_CHOICES, default='N')
    dob = models.DateField(blank=True, null=True)
    student_email = models.EmailField(
        ('student email address'), unique=False, blank=True)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(
        validators=[phone_regex], max_length=17, blank=True)  # validators should be a list
    profile_photo = models.CharField(max_length=200, blank=True)
    emp_status = models.ForeignKey(
        EmploymentStatus, on_delete=models.SET_NULL, null=True, blank=True)
    first_login = models.BooleanField(default=True, null=False)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Feedback(models.Model):
    User = get_user_model()
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    star = models.IntegerField(validators=[
        MaxValueValidator(5),
        MinValueValidator(0)
    ], null=True, blank=True)
