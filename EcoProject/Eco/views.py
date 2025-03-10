# Create your views here.
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout

from django.shortcuts import render
#forms imports
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.urls import reverse
from Eco.forms import UserForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from Eco.models import Challenge
from django.utils import timezone
from datetime import timedelta
from Eco.models import UserProfile
from django.http import JsonResponse
from django.db.models import Q
from .models import Challenge, User_Challenge_Log_Entry
from django.views.decorators.csrf import csrf_exempt


def index(request):
    # Create context dictionary
    context_dict = {
        'boldmessage': 'This will be text for the landing page',
    }

    # Render the response and send it back!
    return render(request, 'Eco/index.html', context=context_dict)

def register(request):
    # A boolean value for telling the template
    # whether the registration was successful.
    # Set to False initially. Code changes value to
    # True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves,
            # we set commit=False. This delays saving the model
            # until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and
            #put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to indicate that the template
            # registration was successful.
            registered = True
        else:
            # Invalid form or forms - mistakes or something else?
            # Print problems to the terminal.
            print(user_form.errors, profile_form.errors)
    else:
        # Not a HTTP POST, so we render our form using two ModelForm instances.
        # These forms will be blank, ready for user input.
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(request,'Eco/register.html',
                  context = {'user_form': user_form,
                             'profile_form': profile_form,
                             'registered': registered})

def user_login(request):
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        # We use request.POST.get('<variable>') as opposed
        # to request.POST['<variable>'], because the
        # request.POST.get('<variable>') returns None if the
        # value does not exist, while request.POST['<variable>']
        # will raise a KeyError exception.
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)
        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return redirect(reverse('Eco:index'))
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Eco account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
        # The request is not a HTTP POST, so display the login form.
        # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'Eco/login.html')

@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")

# Use the login_required() decorator to ensure only those logged in can
# access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return redirect(reverse('Eco:index'))

def challenges(request):
    query = request.GET.get('q')
    if query:
        challenges_list = Challenge.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) 
        )
    else:
        challenges_list = Challenge.objects.all()
    
    context_dict = {
        'challenges': challenges_list,
    }
    
    return render(request, 'Eco/challenges.html', context=context_dict)

def educational_links(request):
    return render(request, 'Eco/EducationalLinks.html')

@login_required
def log_challenge(request, challenge_id):
        challenge = get_object_or_404(Challenge, id=challenge_id)
        User_Challenge_Log_Entry.objects.create(user=request.user, challenge=challenge)
        user_profile = UserProfile.objects.get(user=request.user)
        user_profile.points += challenge.point_value
        user_profile.save()
        return redirect('Eco:Challenges')


@login_required
def leaderboard(request):
    timeframe = request.GET.get('timeframe', 'all')
    if timeframe == 'month':
        days = 30
    elif timeframe == 'year':
        days = 365
    else:
        days = None

    if days:
        users = UserProfile.objects.all()
        users = sorted(users, key=lambda u: u.points_within_timeframe(days), reverse=True)
    else:
        users = UserProfile.objects.all().order_by('-points')

    context_dict = {
        'users': users,
        'timeframe': timeframe,
    }
    return render(request, 'Eco/leaderboard.html', context=context_dict)


@login_required
def account_page(request):
    user_profile = UserProfile.objects.get(user=request.user)
    points_all_time = user_profile.points
    points_year = user_profile.points_within_timeframe(365)
    points_month = user_profile.points_within_timeframe(30)
    points_week = user_profile.points_within_timeframe(7)
    user_challenge_log_entries = User_Challenge_Log_Entry.objects.filter(user=request.user)
    
    context_dict = {
        'user': request.user,
        'user_profile': user_profile,
        'points_all_time': points_all_time,
        'points_year': points_year,
        'points_month': points_month,
        'points_week': points_week,
        'user_challenge_log_entries': user_challenge_log_entries,
    }
    return render(request, 'Eco/AccountPage.html', context=context_dict)

@login_required
@require_POST
def update_email(request):
    new_email = request.POST.get('email')
    if new_email:
        request.user.email = new_email
        request.user.save()
        return JsonResponse({'message': 'Email updated successfully.'})
    else:
        return JsonResponse({'error': 'Invalid email.'}, status=400)

@login_required
@require_POST
def update_picture(request):
    if 'picture' in request.FILES:
        user_profile = UserProfile.objects.get(user=request.user)
        user_profile.picture = request.FILES['picture']
        user_profile.save()
        return JsonResponse({'message': 'Profile picture updated successfully.'})
    else:
        return JsonResponse({'error': 'No picture uploaded.'}, status=400)