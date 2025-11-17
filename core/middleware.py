from django.utils import timezone


class SessionTrackingMiddleware:
    """
    Middleware to track user visits and session activity
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Track visit count in session
        if 'visit_count' not in request.session:
            request.session['visit_count'] = 0
        request.session['visit_count'] += 1
        
        # Track last visit time
        request.session['last_visit'] = timezone.now().isoformat()
        
        # Track pages visited
        if 'pages_visited' not in request.session:
            request.session['pages_visited'] = []
        
        current_path = request.path
        if current_path not in request.session['pages_visited']:
            request.session['pages_visited'].append(current_path)
        
        # Ensure session is saved
        request.session.modified = True
        
        response = self.get_response(request)
        return response

