# Create this file in your app directory (e.g., core/context_processor.py)

from .models import Notice

def notification_processor(request):
    """
    Context processor to add notification count to all templates.
    """
    if request.user.is_authenticated:
        try:
            # Get all notices - you may want to filter this based on relevance to the user
            # or add a "read" status field to your Notice model
            notification_count = Notice.objects.count()
        except:
            notification_count = 0
        
        return {
            'notification_count': notification_count
        }
    return {'notification_count': 0}

