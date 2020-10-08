from django.contrib.auth.models import User
from django.http import QueryDict
from django.utils.deprecation import MiddlewareMixin
from django.core.cache import caches
from django.http.response import JsonResponse

user_cache = caches['users']


class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path != '/videoClipping/rest/login':
            if request.method == 'GET':
                params = request.GET
            elif request.method == 'POST':
                params = request.POST
            else:
                params = QueryDict(request.body)
            token = params.get('token')
            user_id = user_cache.get(token)
            if user_id:
                user = User.objects.get(pk=user_id)
                user_cache.set(token, user.id, 60 * 60 * 2)
            else:
                res = {
                    "code": 1,
                    "message": "未登录",
                }
                return JsonResponse(res)

