from django import forms
from django.contrib.auth.models import User
from Eco.models import UserProfile, Challenge, User_Challenge_Log_Entry, Submitted_Challenge, Leaderboard

        
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password',)
        
        
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture',)

class ChallengeForm(forms.ModelForm):
    class Meta:
        model = Challenge
        fields = ('title', 'description','point_value',)

class UserChallengeLogEntryForm(forms.ModelForm):
    class Meta:
        model = User_Challenge_Log_Entry
        fields = ('user', 'challenge', )

class SubmittedChallengeForm(forms.ModelForm):
    class Meta:
        model = Submitted_Challenge
        fields = ('user', 'challenge',)

class LeaderboardForm(forms.ModelForm):
    class Meta:
        model = Leaderboard
        fields = ('user', 'rank',)