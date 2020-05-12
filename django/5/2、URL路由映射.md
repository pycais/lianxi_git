# URL路由映射

## 一、概要

>路由映射模块，主要完成url与views视图函数的映射。当一个url请求到来时，会按照这个模块中的url地址从上到下进行匹配，如果匹配成功，将执行映射试图中的函数；反之将返回404错误'
>
>当用户请求一个页面时，Django根据下面的逻辑执行操作：
>
>1. 决定要使用的根URLconf模块。通常，这是ROOT_URLCONF设置的值，但是如果传入的HttpRequest对象具有urlconf属性（由中间件设置），则其值将被用于代替ROOT_URLCONF设置。通俗的讲，就是你可以自定义项目入口url是哪个文件！
>2. 加载该模块并寻找可用的urlpatterns。 它是django.conf.urls.url()实例的一个列表。
>3. 依次匹配每个URL模式，在与请求的URL相匹配的第一个模式停下来。也就是说，url匹配是从上往下的短路操作，所以url在列表中的位置非常关键。
>
>导入并调用匹配行中给定的视图，该视图是一个简单的Python函数（被称为视图函数）,或基于类的视图。 视图将获得如下参数:
>一个HttpRequest 实例。
>如果匹配的正则表达式返回了没有命名的组，那么正则表达式匹配的内容将作为位置参数提供给视图。
>关键字参数由正则表达式匹配的命名组组成，但是可以被django.conf.urls.url()的可选参数kwargs覆盖。
>如果没有匹配到正则表达式，或者过程中抛出异常，将调用一个适当的错误处理视图

## 二、基本介绍

### 1、基本语法

1. Django 1.7.x以下版本

   ```python
   from django.conf.urls import patterns, include, url
   from django.contrib import admin
   urlpatterns = patterns(
       url(正则表达式, 'view函数',参数,别名), 
       url(r'^admin/', include(admin.site.urls)),
   )
   ```

2. Django 1.8.x - Django 2.0 版本

   ```python
   from django.conf.urls import url
   from django.contrib import admin
   from views import home
   urlpatterns = [
       url(正则表达式,view函数,参数,别名),
       url(r'^admin/'c, admin.site.urls),
       url(r'^index/', home.index),
   ]
   ```

3. Django 2.0 版本(兼容1.8以上)

   ```python
   from django.contrib import admin
   from django.urls import path
   from views import home
    
   urlpatterns = [
       path(正则表达式, view函数名,参数,别名), 
       path('admin/', admin.site.urls),
       path(r'^index/', home.index),
   ]
   ```


### 2、url详解

1. 语法格式

   ```
   url(正则表达式, view函数名,参数,别名), 
   ```

2. 参数说明

   - regex:是正则表达式的通用缩写
   - view：
     当正则表达式匹配到某个条目时，自动将封装的HttpRequest对象作为第一个参数，正则表达式“捕获”到的值作为第二个参数，传递给该条目指定的视图。如果是简单捕获，那么捕获值将作为一个位置参数进行传递，如果是命名捕获，那么将作为关键字参数进行传递
   - kwargs：
     任意数量的关键字参数可以作为一个字典传递给目标视图。
   - name：
     对你的URL进行命名，可以让你能够在Django的任意处，尤其是模板内显式地引用它。相当于给URL取了个全局变量名，你只需要修改这个全局变量的值，在整个Django中引用它的地方也将同样获得改变。

3. 示例代码

   1、基本的配置

   ```python
   from django.conf.urls import url, include
   # 正则表达式的最前面的r表示raw_string 原生字符串。
   urlpatterns = [
       url(r'^test/$', views.test),
   ]
   ```
   2、动态路由

   ```python
   urlpatterns = [
       url(r'^list/(\d+)/(\d+)/$', views.list),
   ]
   
   # views
   def list(req, page, size):
       return HttpResponse('当前第%s页,默认%s条数' % (page, size))
   # 访问路径
   http://127.0.0.1:8000/route/list/1/10/    
   
   ```

   3、传参形式的动态路由

   ```python
   # (?p<分组名>正则语法)
   urlpatterns = [
      url(r'^param_list/(?P<uid>\d+)/$', views.param_list),
   ]
   #，相当于一个字典， key=uid, value=\d+。 {"uid":"\d+"}
   
   # views.py
   
   def param_list(req, uid):
       return HttpResponse('用户名id%s' % uid)
   
   #访问路径
   http://127.0.0.1:8000/route/param_list/1/
   ```

   4、那如果映射 url 太多怎么办，全写一个在 urlpatterns 显得繁琐 在每个app下新建urls文件

   ```python
   urlpatterns = [
       url(r'^test/$', views.test),
       url(r'^test1/$', views.test1),
       url('upload/$', include('app_name.urls'),
   ]
   ```
   5、url中还支持name参数的配置，如果配置了name属性，在模板的文件中就可以使用name值来代替相应的url值
   ```python
      urlpatterns = [
       	url(r'^index',views.index,name='bieming')
      ]
      <form action="{% url 'bieming' %}" method="post">
      </form>
   ```

## 三、FBV与CBV

   ### 1、FBV

   1. 说明

      function base views 就是在视图里使用函数处理请求

   2. urls

      ```python
      url(r'^login/$', account.login),
      ```

   3. views

      ```python
      def login(request):
          message = ""
          if request.method == "POST":
              user = request.POST.get('username')
              pwd = request.POST.get('password')
              c = User.objects.filter(username=user, password=pwd).count()
              if c:
                  request.session['is_login'] = True
                  request.session['username'] = user
                  return redirect('/index.html')
              else:
                  message = "用户名或密码错误"
          return render(request, 'login.html', {'msg': message})
      ```

### 2、CBV

1. 说明

   class base views  就是在视图里使用类处理请求

2.  urls

   ```python
   url(r'^login/$', account.Login.as_view()),
   ```

3. views

   ```python
   class Login(views.View):
       def get(self, request, *args, **kwagrs):
           return render(request, 'login.html')
            
       def post(self, request, *args, **kwagrs):
           user = request.POST.get('username')
           pwd = request.POST.get('password')
           c = Administrator.objects.filter(username=user, password=pwd).count()
           if c:
               request.session['is_login'] = True
               request.session['username'] = user
               return redirect('/index.html')
           else:
               message = "用户名或密码错误"
          	 return render(request, 'login.html', {'msg': message})
   ```

4. 注意

   当我们使用CBV方式时，首先要注意urls.py文件中要写成“类名.as_view()”方式映射，其次在类中我们定义的get/post方法这些方法的名字不是我们自己定义的，而是按照固定样式，View类中支持以下方法

   ```
   'get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace'
   ```

