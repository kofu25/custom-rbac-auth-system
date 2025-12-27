# Этот файл больше не используется, так как аутентификация перенесена 
# в core/authentication.py для корректной работы с DRF.
class CustomAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)