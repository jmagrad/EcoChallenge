from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

# Create your models here.
    
class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # The additional attributes we wish to include.
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    def __str__(self):
        return self.user.username
    
class Challenge(models.Model):
    TITLE_MAX_LENGTH = 128
    title = models.CharField(max_length=TITLE_MAX_LENGTH)
    description = models.TextField()
    point_value = models.IntegerField()
    users = models.ManyToManyField(User, through='User_Challenge_Log_Entry')
    
    def __str__(self):
        return self.title

class User_Challenge_Log_Entry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    date_logged = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.challenge.title} - {self.date_logged}"

class Submitted_Challenge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    date_submitted = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.challenge.title} - {self.date_submitted}"

class Leaderboard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rank = models.IntegerField()
    date_recorded = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - Rank: {self.rank} - {self.date_recorded}"