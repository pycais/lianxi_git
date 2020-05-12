# 安装：

- pip install django-bootstrap3
- 在settings.py 的install_apps中加上 'bootstrap3'

## 写模版

导入(文件开头位置)：

​	{% load bootstrap3 %}

使用bootstrap_messages，在文件中的适当位置写上就会显示messages的内容

​	{% bootstrap_messages %}

使用默认表单 bootstrap_form

​	最简单的方式：label和field显示的是上下格式

​	{% bootstrap_form form %}

显示成水平方式：

​	{% bootstrap_form form layout="horizontal" %}

调节label的class： 
​	horizontal_label_class=”xxx” # 只对horizontal模式有效 
​	或 label_class=”xxx” # 都有效
调节field的class： 
​	horizontal_field_class=”yyy” # 只对horizontal模式有效 
​	field_class=”yyy” # 都有效
调节每个input+label外面的div的class，默认是form-group 
​	form_group_class=”xxx”
上面是几种常用的属性，还有很多可以看官方文档django-bootstrap3
省去label：

​	{% bootstrap_form form layout="inline" %}
​	
优点

使用django_bootstrap3的form的优点之一就是，他可以自动的生成错误提示，非常方便

# 使用案例

1 models.py 写入一个 书籍的模型

```
from django.db import models

# Create your models here.
class Book(models.Model):

    name = models.CharField(
        max_length=30,
        verbose_name="书名"
    )
    avater = models.ImageField(
        upload_to="icons",
        verbose_name="书籍封面",
    )
```

2 在app目录下新建forms.py

~~~
from django import forms
from .models import Book
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ("name", "price")
~~~

3 views.py

~~~
from django.http import HttpResponse
from django.shortcuts import render
from .models import *
from .forms import *
from django.contrib import messages

# Create your views here.
def index(request):
    if request.method == "GET":
        form = BookForm()
        return render(request, "index.html", {"form": form})
    else:
        files = request.FILES
        form = BookForm(data=request.POST, files=files)
        if form.is_valid():
            form.save()
            return HttpResponse("ok")
        else:
            messages.add_message(request, messages.ERROR, form.errors.as_text())
            return render(request, "index.html", {"form": form})
~~~

4 index.html的内容如下

~~~
{% load static %}
{#加载bootstrap3#}
{% load bootstrap3 %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
{#    加载样式#}
    {% bootstrap_css %}
{#      加载js#}
    {% bootstrap_javascript %}
{#    加载信息提示#}
    {% bootstrap_messages %}
</head>
<body>
<div class="container">

    <form action="/day06/index" method="post">
{#        使用默认的form表单#}
        {% bootstrap_form form layout="horizontal" %}
        <input type="submit">
        {% csrf_token %}
    </form>
    </div>
</body>
</html>
~~~

5 其他 配置相关的路由 迁移等正常操作