from django.http import HttpResponseForbidden

class RolesMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            if request.user.role == 'admin':
                request.is_admin = True
            else:
                request.is_admin = False
        else:
            request.is_admin = False

        response = self.get_response(request)

        return response
