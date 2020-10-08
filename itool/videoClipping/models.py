from django.db import models


# Create your models here.
class Books(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=True)
    create_time = models.DateTimeField(auto_now_add=True)


class UploadFile(models.Model):
    img_file = models.ImageField(upload_to='icons')
    video_file = models.FileField(upload_to='videos')
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'uploadfiles'


class ToFiles(models.Model):
    file = models.FileField(upload_to='videos')
    ctreate_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tofiles'


class VideoStatus(models.Model):
    video_name = models.CharField(max_length=500)
    video_name2 = models.CharField(max_length=50, verbose_name='视频别名', null=True)
    file_path = models.CharField(max_length=100, verbose_name='视频存储路径')
    file_path2 = models.CharField(max_length=100, verbose_name='视频剪裁后路径', null=True)
    task_id = models.CharField(max_length=50, verbose_name='异步剪裁ID', null=True)
    status = models.CharField(max_length=50, verbose_name='视频剪裁状态', null=True)
    result = models.CharField(max_length=500, verbose_name='异步剪裁结果', null=True)
    runtime = models.FloatField(verbose_name='异步任务运行时间', max_length=10, null=True)
    traceback = models.CharField(max_length=1000, verbose_name='报错', null=True)
    children = models.CharField(max_length=500, verbose_name='字段保留', null=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='存储时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'videostatus'
