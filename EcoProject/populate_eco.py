import os
import random
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EcoProject.settings')

import django
django.setup()
from Eco.models import User, UserProfile, Challenge, User_Challenge_Log_Entry, Submitted_Challenge, Leaderboard, EducationalLink

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

    # Add eductional links
    # General Sustainability & Green Living
    add_educational_link('Treehugger', 'Covers everything from sustainable living and design to eco-friendly technology and energy.', 'https://www.treehugger.com/' )
    add_educational_link('Earth911', 'Offers recycling guides, sustainability tips, and eco-conscious product recommendations.', 'https://earth911.com/')

    # Zero Waste & Minimalism
    add_educational_link('Going Zero Waste', 'Offers practical tips on living waste-free and reducing your environmental footprint.', 'https://www.goingzerowaste.com/')

    # Eco-Friendly Shopping & Ethical Brands
    add_educational_link('Ethical Consumer', 'A guide to ethical products, brands, and sustainable choices.', 'https://www.ethicalconsumer.org/')
    add_educational_link('Sustainable Jungle', 'Reviews eco-friendly products, sustainable fashion, and ethical brands.', 'https://www.sustainablejungle.com/')

    # Green Energy & Sustainable Homes
    add_educational_link('Energy Sage', 'Helps compare solar panel options and find sustainable energy solutions.', 'https://www.energysage.com/')
    add_educational_link('Green Building Advisor', 'For those interested in sustainable architecture and green home improvements.', 'https://www.greenbuildingadvisor.com/')
    add_educational_link('Mother Earth News', 'A classic resource for homesteading, gardening, and sustainable living.', 'https://www.motherearthnews.com/')

    #Ecofriendly lifestyle 
    add_educational_link('Ecofriendly lifestyle', '20 Steps to Ecofriendly lifestyle', 'https://www.goodenergy.co.uk/blog/the-ultimate-20-step-guide-to-eco-friendly-living/')
    add_educational_link(' Live more sustainably', '20 Ways to live more sustainably', 'https://www.biologicaldiversity.org/programs/population_and_sustainability/sustainability/live_more_sustainably.html')

    #Recycling 
    add_educational_link('Recycling Practises', 'Advantages of Recycling', 'https://www.wastemanaged.co.uk/our-news/recycling/advantages-of-recycling/')
    add_educational_link('Plastic Recycling', 'How does plastic recycling help the environment?', 'https://www.buxtonwater.co.uk/articles/community-and-environment/plastic-recycling')


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

def add_educational_link(title, description, url):
    link, created =  EducationalLink.objects.get_or_create(title=title, description=description, url=url)
    link.save()
    return link

if __name__ == '__main__':
    print('Starting Eco population script...')
    populate()