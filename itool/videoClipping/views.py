import datetime
import os
import uuid

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.cache import caches
from django.views import View
from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework.response import Response
from .tasks import *
from .videorestful import VideoClippingStatus, UserSerializer
from rest_framework import status
from django.core.paginator import Paginator, EmptyPage
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, QueryDict
from .models import Books, UploadFile, ToFiles, VideoStatus
from itool import settings
import traceback
import logging

logger = logging.getLogger('videoClipping')
user_cache = caches['users']


# Create your views here.

def index(request):
    if request.method == 'GET':
        # return JsonResponse({'data': 'Hello world'})
        return HttpResponse('heo')


def showbooks(request):
    page_num = request.GET.get('num', 1)
    books = Books.objects.all()
    paginator = Paginator(books, settings.PER_PAGE)
    try:
        page = paginator.page(page_num)
        result = page.object_list
    except EmptyPage:
        result = paginator.page(1).object_list
    except Exception as e:
        print(traceback.format_exc(e))
    result = [i.name for i in result]
    print(result)
    # data = [for i in ]
    return JsonResponse({'data': result}, json_dumps_params={'ensure_ascii': False})


def upload_file(request):
    start_time = time.time()
    if request.method == 'POST':
        file = request.FILES.get('filename', None)
        print(request.FILES)
        print(dir(request.FILES))
        print(file)
        if not file:
            return HttpResponse('not file upload')
        with open(os.path.join("/home/caisheng/", file.name), 'wb+') as f:
            for chunk in file.chunks():
                f.write(chunk)
        print(time.time() - start_time)
        ToFiles.objects.create(file=file.name)
        return HttpResponse('保存成功')
    else:
        return HttpResponseBadRequest('dsa')


def upload_files(request):
    if request.method == 'POST':
        file = request.FILES.get('filename')
        files = UploadFile()
        files.img_file = file
        files.save()
        return HttpResponse('上传成功')


def celery_video(request):
    loop = hello.delay(10)
    print(loop)
    try:
        loop + 'qq'
    except Exception as e:
        logger.error(e)
        logger.info(e)
    return HttpResponse('ok')


class VideoApiClipping(View):
    def get(self, request):
        _id = request.GET.get('task_id', None)
        try:
            video = VideoStatus.objects.filter(task_id=_id) if _id else VideoStatus.objects.all()
            serializer = VideoClippingStatus(video, many=True)
            res = {
                "code": 0,
                "message": "ok",
                "data": serializer.data,
                "reCOde": status.HTTP_200_OK
            }
        except VideoStatus.DoesNotExist:
            res = {
                "code": 1,
                "message": "数据库无此数据",
                "data": "",
                "reCode": status.HTTP_204_NO_CONTENT
            }
        except Exception as e:
            logger.error(e)
            res = {
                "code": 2,
                "message": "操作异常",
                "data": "",
                "reCode": status.HTTP_404_NOT_FOUND
            }

        return JsonResponse(res)

    def post(self, request):
        serializer = VideoClippingStatus(data=request.POST)
        print(request.POST)
        if serializer.is_valid():
            try:
                serializer.save()
                res = {
                    "code": 0,
                    "message": "ok",
                    "data": serializer.data,
                    "reCode": status.HTTP_200_OK
                }
            except Exception as e:
                res = {
                    "code": 0,
                    "message": "ok",
                    "data": serializer.error_messages,
                    "reCode": status.HTTP_406_NOT_ACCEPTABLE
                }
                logger.error(e)
        else:
            print(serializer.data)
            res = {
                "code": 1,
                "message": serializer.error_messages,
                "data": "",
                "reCode": status.HTTP_417_EXPECTATION_FAILED
            }
        return JsonResponse(res)

    def put(self, request):
        params = QueryDict(request.body)
        print(params)
        id = params.get('task_id', None)
        print(id)
        video = VideoStatus.objects.get(task_id=id)
        serializer = VideoClippingStatus(instance=video, data=params)
        print(QueryDict(request.body))
        if serializer.is_valid():
            try:
                serializer.save()
                res = {
                    "code": 0,
                    "message": "ok",
                    "data": serializer.data,
                    "reCode": status.HTTP_200_OK
                }
            except Exception as e:
                res = {
                    "code": 0,
                    "message": "ok",
                    "data": serializer.error_messages,
                    "reCode": status.HTTP_406_NOT_ACCEPTABLE
                }
                logger.error(e)
        else:
            print(serializer.data)
            res = {
                "code": 1,
                "message": serializer.error_messages,
                "data": "",
                "reCode": status.HTTP_417_EXPECTATION_FAILED
            }
        return JsonResponse(res)

    def delete(self, request):
        params = QueryDict(request.body)
        taks_id = params.get('task_id')
        try:
            VideoStatus.object.get(taks_id=taks_id).delete()
            res = {
                "code": 0,
                "message": "删除成功",
                "data": "",
                "reCode": status.HTTP_200_OK
            }
        except Exception as e:
            res = {
                "code": 1,
                "message": "操作异常",
                "data": "",
                "reCode": status.HTTP_403_FORBIDDEN
            }
            logger.error(e)
        return JsonResponse(res)


class LoginRegister(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):

        print(datetime.datetime.now(), ":", request.get_full_path(), request.META['REMOTE_ADDR'])
        username = request.data.get('username', None)
        password = request.data.get('password', None)
        token = request.data.get('token', None)
        try:
            if username and password:
                user = authenticate(username=username, password=password)
                if user:
                    if user_cache.get(token):
                        user_cache.set(token, user.id, 60 * 60 * 2)
                    else:
                        token = uuid.uuid4().hex
                        user_cache.set(token, user.id, 60 * 60 * 2)
                    res = {"code": 0, "message": "ok", "data": token}
                    return Response(res)
                else:
                    res = {"code": 1, "message": "账号或密码错误", "data": ""}
                    return Response(res)
            else:
                res = {"code": 1, "message": "账号或密码错误", "data": ""}
                return Response(res)
        except Exception as e:
            logger.error(e)
            logging.error(traceback.format_exc())
            res = {"code": 1, "message": "操作异常", "data": ""}
            return Response(res)


# class UserAPIView(ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     authentication_classes = [LoginAuthentication]
#
#     def list(self, request, *args, **kwargs):
#         print(request.successful_authenticator)
#         if not request.successful_authenticator:
#             res = {
#                 "code": 1,
#                 "message": "未登录",
#             }
#             return Response(res)
#         queryset = self.filter_queryset(self.get_queryset())
#
#         page = self.paginate_queryset(queryset)
#         if page is not None:
#             serializer = self.get_serializer(page, many=True)
#             return self.get_paginated_response(serializer.data)
#
#         serializer = self.get_serializer(queryset, many=True)
#         return Response(serializer.data)

