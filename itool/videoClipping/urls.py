from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('index', index, name='index'),
    path('books', showbooks, name='books'),
    path('upload', upload_file, name='upload'),
    path('uploads', upload_files, name='uploads'),
    path('celery', celery_video, name='celery'),
    path('rest/video', VideoApiClipping.as_view()),
    path('rest/login', LoginRegister.as_view()),
    # path('rest/auth', UserAPIView.as_view())

]
