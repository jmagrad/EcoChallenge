from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone
from django.core.validators import MinValueValidator

# Create your models here.

class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # The additional attributes we wish to include
    picture = models.ImageField(upload_to='profile_images', blank=True)
    points = models.IntegerField(default=0)  # Add this line to include points field

    def __str__(self):
        return self.user.username
    
    def points_within_timeframe(self, days):
        end_date = timezone.now()
        start_date = end_date - timedelta(days=days)
        log_entries = User_Challenge_Log_Entry.objects.filter(user=self.user, date_logged__range=(start_date, end_date))
        return sum(entry.challenge.point_value for entry in log_entries)

class Challenge(models.Model):
    TITLE_MAX_LENGTH = 128
    DESCRIPTION_MAX_LENGTH = 750
    title = models.CharField(max_length=TITLE_MAX_LENGTH)
    description = models.TextField(max_length=DESCRIPTION_MAX_LENGTH)
    point_value = models.IntegerField([MinValueValidator(0)])

    likes = models.IntegerField(default=0)
    users = models.ManyToManyField(User, through='User_Challenge_Log_Entry')
    
    def __str__(self):
        return self.title

class User_Challenge_Log_Entry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    date_logged = models.DateTimeField()  # Remove auto_now_add=True
    
    def __str__(self):
        return f"{self.user.username} - {self.challenge.title} - {self.date_logged}"

class Submitted_Challenge(models.Model):
    title = models.CharField(max_length=Challenge.TITLE_MAX_LENGTH, default="No title provided.")
    #challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE) Deleted because this is a new challenge
    #   not an existing one. This was trying to link the submitted challenge to an existing one.
    description = models.TextField(max_length=Challenge.DESCRIPTION_MAX_LENGTH, default="No description provided.")
    point_value = models.IntegerField(default=0)
    date_submitted = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    #challenge = models.ForeignKey('Challenge', on_delete=models.SET_NULL, null=True, blank=True) See comment immediately above
    
    def __str__(self):
        return f"{self.title} - {self.date_submitted}"
    
    def approve(self):
        # This is my attempt at trying to automatically create a new challenge, when approved by the 
        #   administrator in the submitted challenges seciton of /admin
        if self.approved:
            add_challenge(self.title, self.description, self.point_value)
        # Considered having logic to delete the approved challenge from submitted challenges, but the 
        # /admin interface has a helpful filter function already, so you can easily find what you need

class Leaderboard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_recorded = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.date_recorded}"
    
class EducationalLink(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    url = models.URLField()

    def __str__(self):
        return self.title
