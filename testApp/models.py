from django.db import models
from django.contrib.auth.models import User
# Create your models here.


"""
Email required in registration Model settings
"""
User._meta.get_field('email')._unique = True
User._meta.get_field('email').blank = False
User._meta.get_field('email').null = False