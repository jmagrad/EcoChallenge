from django.contrib import admin
#from Eco.models import *
from Eco.models import Challenge, Submitted_Challenge, UserProfile, User_Challenge_Log_Entry, Leaderboard
import logging

logger = logging.getLogger(__name__)

admin.site.register(UserProfile)
admin.site.register(Challenge)
admin.site.register(User_Challenge_Log_Entry)
admin.site.register(Leaderboard)
# Register your models here.

@admin.register(Submitted_Challenge)
class SubmittedChallengeAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ('title', 'point_value', 'date_submitted', 'approved')  
    
    # Add filtering by approval status
    list_filter = ('approved',)  
    
    # Enable search by title and description
    search_fields = ('title', 'description')  
    
    # Add custom actions for approval, rejection, and challenge creation
    actions = ['approve_selected_challenges', 'reject_selected_challenges', 'create_challenge_from_submission']  

    def approve_selected_challenges(self, request, queryset):
        """Admin action to approve selected challenges."""
        queryset.update(approved=True)

    def reject_selected_challenges(self, request, queryset):
        """Admin action to reject selected challenges."""
        queryset.update(approved=False)

    def create_challenge_from_submission(self, request, queryset):
        """Create a new Challenge from the approved SubmittedChallenges."""
        for submitted_challenge in queryset:
            # Only create challenge if it's approved
            if submitted_challenge.approved:
                Challenge.objects.get_or_create(
                    title=submitted_challenge.title,
                    description=submitted_challenge.description,
                    point_value=submitted_challenge.point_value, 
                    defaults={'likes': 0}
                )

                if created:
                    logger.info(f"Created challenge: {challenge.title}")
                else:
                    logger.info(f"Challenge already exists: {challenge.title}")
                # Optionally, mark the SubmittedChallenge as "converted" or update its status
                submitted_challenge.approved = False  # Or update the status in any way
                submitted_challenge.save()
                
        # Provide feedback message to the admin
        self.message_user(request, "Selected challenges have been converted to real challenges.")
    
    # Short descriptions for the actions
    approve_selected_challenges.short_description = "Approve selected challenges"
    reject_selected_challenges.short_description = "Reject selected challenges"
    create_challenge_from_submission.short_description = "Convert approved submissions to real challenges"