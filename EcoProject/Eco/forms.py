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
        fields = ('picture',)

class ChallengeForm(forms.ModelForm):
    class Meta:
        model = Challenge
        fields = ('title', 'description','point_value',)

class UserChallengeLogEntryForm(forms.ModelForm):
    class Meta:
        model = User_Challenge_Log_Entry
        fields = ('user', 'challenge',)

class SubmittedChallengeForm(forms.ModelForm):
    POINT_CHOICES = [
        (5, '5 points'),
        (10, '10 points'),
        (15, '15 points'),
        (20, '20 points'),
        (25, '25 points or more')
    ]

    point_value = forms.ChoiceField(choices=POINT_CHOICES, widget=forms.RadioSelect)
    
    class Meta:
        model = Submitted_Challenge
        fields = ('title', 'description', 'point_value')
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
        }

class LeaderboardForm(forms.ModelForm):
    class Meta:
        model = Leaderboard
        fields = ('user',)