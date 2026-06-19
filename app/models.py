from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=30)
    lastname=models.CharField(max_length=30)
    birthdate=models.DateField()
    neighborhood=models.CharField(max_length=30)
    canOffer=models.BooleanField(default=False)
    canWalk=models.BooleanField(default=False)

class DogProfile(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    dogName=models.CharField(max_length=30)
    dogBirthdate=models.DateField()
    breed=models.CharField(max_length=30)
    weightKG=models.DecimalField(max_digits=5, decimal_places=2)
    behaviour=models.CharField(max_length=30)
    meds=models.BooleanField(default=False)

class BoardPost(models.Model):
    dateTimePost=models.DateTimeField()
    dateRequested=models.DateTimeField()
    text=models.TextField()
    recurrent=models.BooleanField(default=False)
    dog=models.ForeignKey(DogProfile,on_delete=models.CASCADE)
    active=models.BooleanField(default=True)
    
