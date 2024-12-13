from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.http import HttpResponsePermanentRedirect

# SSL_ENABLED = getattr(settings, 'SSL_ENABLED', False)

class SecurityMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['Content-Security-Policy'] = "default-src 'self'"
        return response
