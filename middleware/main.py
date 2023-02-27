from datetime import datetime
from user_auth.models import UserLog


class UserLogMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def log_request(self, method, url, user):
        try:
            log_entry = UserLog.objects.get(method=method, url=url, user=user)
            log_entry.count += 1
            log_entry.updated_at = datetime.now()
            log_entry.save()
        except UserLog.DoesNotExist:
            UserLog.objects.create(method=method, url=url, user=user)

    def __call__(self, request):
        # Call the next middleware or view
        response = self.get_response(request)
        # If the user is authenticated, log the request
        if request.user.is_authenticated:
            self.log_request(request.method, request.path, request.user)
        return response
