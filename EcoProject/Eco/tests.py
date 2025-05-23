from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import timedelta, datetime
from Eco.models import User_Challenge_Log_Entry, User, Challenge, UserProfile, Leaderboard

# Create your tests here.
class UserModelTests(TestCase):
    def test_user_creation(self):
        user = add_user(username="testuser", email="testuser@example.com", password="password", points=5)
        user_profile = UserProfile.objects.get(user=user)
        self.assertEqual(user_profile.user.username, 'testuser')

class ChallengeModelTests(TestCase):
    def test_challenge_creation(self):
        challenge = add_challenge(title='Test Challenge', description='Test Description', point_value=10)
        self.assertEqual(challenge.title, 'Test Challenge')
        self.assertEqual(challenge.point_value, 10)

    def test_challenge_negative_point_value(self):
        with self.assertRaises(ValidationError):
            challenge = Challenge(title='Test Challenge', description='Test Description', point_value=-10)
            challenge.full_clean()  
            challenge.save()

class UserRegistrationTests(TestCase):
    def test_user_registration_invalid_data(self):
        response = self.client.post(reverse('Eco:register'), {
            'username': '',
            'email': 'invalidemail',
            'password1': 'password1',
            'password2': 'password2',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(email='invalidemail').exists())

class ChallengeSearchTests(TestCase):
    def setUp(self):
        self.challenge1 = add_challenge(title='Clean the Beach', description='Beach cleaning activity', point_value=20)
        self.challenge2 = add_challenge(title='Plant a Tree', description='Tree planting activity', point_value=15)

    def test_search_challenges(self):
        response = self.client.get(reverse('Eco:Challenges'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Clean the Beach')
        self.assertContains(response, 'Plant a Tree')

class UserChallengeLogEntryTests(TestCase):
    def setUp(self):
        self.user = add_user(username='testuser', email='test@example.com', password='password123', points=0)
        self.challenge = add_challenge(title='Test Challenge', description='Test Description', point_value=10)

    def test_log_entry_creation(self):
        log_user_challenge(user=self.user, challenge=self.challenge, date_logged=timezone.now())
        log_entry = User_Challenge_Log_Entry.objects.get(user=self.user, challenge=self.challenge)
        self.assertEqual(log_entry.user.username, 'testuser')
        self.assertEqual(log_entry.challenge.title, 'Test Challenge')
        self.assertEqual(log_entry.challenge.point_value, 10)

class LeaderboardViewTests(TestCase):
    def setUp(self):
        self.user1 = add_user(username='user1', email='user1@example.com', password='password123', points=0)
        self.user2 = add_user(username='user2', email='user2@example.com', password='password123', points=0)
        self.challenge = add_challenge(title='Test Challenge', description='Test Description', point_value=10)
        log_user_challenge(user=self.user1, challenge=self.challenge, date_logged=timezone.now() - timedelta(days=500))
        log_user_challenge(user=self.user2, challenge=self.challenge, date_logged=timezone.now() - timedelta(days=40))
        self.client.login(username='user1', password='password123')

    def test_leaderboard_all_time(self):
        response = self.client.get(reverse('Eco:LeaderBoard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user1.username)
        self.assertContains(response, self.user2.username)

    def test_leaderboard_year(self):
        response = self.client.get(reverse('Eco:LeaderBoard') + '?timeframe=year')
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, r"<td>user1</td>\n                <td>0</td")
        self.assertContains(response, self.user2.username)

class LeaderboardTests(TestCase):
    def setUp(self):
        self.user1 = add_user(username='user1', email='user1@example.com', password='password123', points=30)
        self.user2 = add_user(username='user2', email='user2@example.com', password='password123', points=50)
        self.client.login(username='user1', password='password123') 

    def test_leaderboard_ordering(self):
        response = self.client.get(reverse('Eco:LeaderBoard'))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        self.assertTrue(content.index('user2') < content.index('user1'))
        
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