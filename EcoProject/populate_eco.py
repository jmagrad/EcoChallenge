import os
import random
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EcoProject.settings')

import django
django.setup()
from Eco.models import User, UserProfile, Challenge, User_Challenge_Log_Entry, Submitted_Challenge, Leaderboard

def populate():
    # Clear existing user points and user challenge log entries
    User_Challenge_Log_Entry.objects.all().delete()
    for user in User.objects.all():
        try:
            user_profile = user.userprofile
        except UserProfile.DoesNotExist:
            user_profile = UserProfile.objects.create(user=user, points=0)
        user_profile.points = 0
        user_profile.save()

    # Create users
    user1 = add_user('user1', 'user1@example.com', 'password123', 0)
    user2 = add_user('user2', 'user2@example.com', 'password123', 0)
    user3 = add_user('user3', 'user3@example.com', 'password123', 0)

    # Create challenges
    commute_challenge = add_challenge('Commute', 'Walk or take public transit to work today.', 5)
    food_waste_challenge = add_challenge('Food Waste', 'Compost all of your food this week.', 15)
    litter_pickup_challenge = add_challenge('Litter Pickup', 'Spend 30 minutes picking up litter in a public space', 10)
    meatless_week_challenge = add_challenge('Meatless Week', 'Go a week without eating meat.', 15)
    
    # Log user challenges
    log_user_challenge(user1, commute_challenge,datetime.now() - timedelta(days=14))
    log_user_challenge(user1, food_waste_challenge,datetime.now() - timedelta(days=14))
    log_user_challenge(user2, commute_challenge,datetime.now() - timedelta(days=60))
    log_user_challenge(user2, food_waste_challenge,datetime.now() - timedelta(days=60))
    log_user_challenge(user3, litter_pickup_challenge,datetime.now() - timedelta(days=2*365))
    log_user_challenge(user2, meatless_week_challenge,datetime.now() - timedelta(days=60))

    # Add 3 new food waste challenge logs to user3 from 2 years ago
    two_years_ago = datetime.now() - timedelta(days=2*365)
    for _ in range(3):
        log_user_challenge(user3, food_waste_challenge, date_logged=two_years_ago)

    # Update user points
    update_user_points(user1)
    update_user_points(user2)
    update_user_points(user3)

    # Create leaderboard entries
    add_leaderboard_entry(user1)
    add_leaderboard_entry(user2)
    add_leaderboard_entry(user3)

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
    challenge = Challenge.objects.get_or_create(title=title, description=description, point_value=point_value, defaults={'likes': 0})[0]
    challenge.save()
    return challenge

def log_user_challenge(user, challenge, date_logged=None):
    if date_logged is None:
        date_logged = datetime.now()
    log_entry, created = User_Challenge_Log_Entry.objects.get_or_create(user=user, challenge=challenge, defaults={'date_logged': date_logged})
    if not created:
        log_entry.date_logged = date_logged
        log_entry.save()

def add_leaderboard_entry(user):
    # Ensure only one leaderboard entry per user
    Leaderboard.objects.filter(user=user).delete()
    leaderboard_entry = Leaderboard.objects.create(user=user)
    leaderboard_entry.save()

def update_user_points(user):
    user_profile = user.userprofile
    user_profile.points = User_Challenge_Log_Entry.objects.filter(user=user).count() * 15  # Assuming each challenge is worth 15 points
    user_profile.save()

if __name__ == '__main__':
    print('Starting Eco population script...')
    populate()
