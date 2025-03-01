import os
import random
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EcoProject.settings')

import django
django.setup()
from Eco.models import User, UserProfile, Challenge, User_Challenge_Log_Entry, Submitted_Challenge, Leaderboard

def populate():
    # Create users
    user1 = add_user('user1', 'user1@example.com', 'password123', 30)
    user2 = add_user('user2', 'user2@example.com', 'password123', 50)

    # Create challenges
    commute_challenge = add_challenge('Commute', 'Walk or take public transit to work today.', 5)
    food_waste_challenge = add_challenge('Food Waste', 'Compost all of your food this week.', 15)

    # Log user challenges
    log_user_challenge(user1, commute_challenge)
    log_user_challenge(user1, food_waste_challenge)
    log_user_challenge(user2, commute_challenge)
    log_user_challenge(user2, food_waste_challenge)

    # Create leaderboard entries
    add_leaderboard_entry(user1, 30)
    add_leaderboard_entry(user2, 50)

    # Print out the users and their points
    for user in User.objects.all():
        try:
            user_profile = user.userprofile
        except UserProfile.DoesNotExist:
            user_profile = UserProfile.objects.create(user=user, points=0)
        print(f'- {user.username}: {user_profile.points} points')

def add_user(username, email, password, points):
    user, created = User.objects.get_or_create(username=username, email=email)
    if created:
        user.set_password(password)
        user.save()
    try:
        user_profile = user.userprofile
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=user, points=points)
    user_profile.points = points
    user_profile.save()
    return user

def add_challenge(title, description, point_value):
    challenge = Challenge.objects.get_or_create(title=title, description=description, point_value=point_value)[0]
    challenge.save()
    return challenge

def log_user_challenge(user, challenge):
    log_entry = User_Challenge_Log_Entry.objects.get_or_create(user=user, challenge=challenge)[0]
    log_entry.save()

def add_leaderboard_entry(user, points):
    leaderboard_entry = Leaderboard.objects.get_or_create(user=user, rank=points)[0]
    leaderboard_entry.save()

if __name__ == '__main__':
    print('Starting Eco population script...')
    populate()
