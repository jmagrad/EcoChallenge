from django.shortcuts import render
from .models import User

def leaderboard(request):
    timeframe = request.GET.get('timeframe', 'all')
    days = 0
    if timeframe == 'week':
        days = 7
    elif timeframe == 'month':
        days = 30
    elif timeframe == 'year':
        days = 365

    ranked_users = User.objects.all()  # Adjust this query to get ranked users based on your logic

    context = {
        'ranked_users': ranked_users,
        'timeframe': timeframe,
        'days': days,
    }
    return render(request, 'Eco/LeaderBoard.html', context)