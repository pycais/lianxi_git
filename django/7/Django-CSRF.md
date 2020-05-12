# Django-CSRF

## 一、什么是CSRF

### 1、概要

> CSRF（Cross-site request forgery），中文名称：跨站请求伪造，也被称为：one click attack/session riding，缩写为：CSRF/XSRF。是一种网络的攻击方式，它在 2007 年曾被列为互联网 20 大安全隐患之一。其他安全隐患，比如 SQL 脚本注入，跨站域脚本攻击等在近年来已经逐渐为众人熟知，很多网站也都针对他们进行了防御

### 2、原理

1. 结构图

   ![](http://zhangwei-imgs.oss-cn-beijing.aliyuncs.com/18-11-24/42651115.jpg)

2. 说明

   - 登录受信任网站A，并在本地生成Cookie 。
   - 在不退出A的情况下，访问危险网站B。

## 二、django中csrf的实现机制

1. django第一次响应来自某个客户端的请求时,后端随机产生一个token值，把这个token保存在SESSION状态中;同时,后端把这个token放到cookie中交给前端页面；

2. 下次前端需要发起请求（比如登录,注册）的时候把这个token值加入到请求数据或者头信息中,一起传给后端；Cookies:{csrftoken:xxxxx}

3. 后端校验前端请求带过来的token和SESSION里的token是否一致；

## 三、操作步骤

> 默认情况下，CSRF防御机制就已经开启了。如果没有开启，请在MIDDLEWARE设置中添加'django.middleware.csrf.CsrfViewMiddleware'。
>
> **对于GET请求，一般来说没有这个问题，CSRF通常是针对POST方法的！**
>
> 在含有POST表单的模板中，需要在其`<form>`表单元素内部添加`csrf_token`标签，`
>
> ```django
> <form action="" method="post">
>     {% csrf_token %}
>     ....
> </form>
> ```
>
> 这样，当表单数据通过POST方法，发送到后台服务器的时候，除了正常的表单数据外，还会携带一个CSRF令牌随机字符串，用于进行csrf验证。其实没有多么麻烦和复杂，对么？如果表单中没有携带这个csrf令牌

## 四、 AJAX

### 1、 说明

> 我们知道，在前端的世界，有一种叫做AJAX的东西，也就是“Asynchronous Javascript And XML”（异步 JavaScript 和 XML），经常被用来在不刷新页面的情况下，提交和请求数据。如果我们的Django服务器接收的是一个通过AJAX发送过来的POST请求的话，那么将很麻烦。
>
> 为什么？因为AJAX中，没有办法像form表单中那样携带`{% csrf_token %}`令牌。
>
> 那怎么办呢？好办！在你的前端模版的JavaScript代码处，添加下面的代码：

### 2、 示例代码

1. 栗子

   ```javascript
   function getCookie(name) {
       var cookieValue = null;
       if (document.cookie && document.cookie !== '') {
           var cookies = document.cookie.split(';');
           for (var i = 0; i < cookies.length; i++) {
               var cookie = jQuery.trim(cookies[i]);
               // Does this cookie string begin with the name we want?
               if (cookie.substring(0, name.length + 1) === (name + '=')) {
                   cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                   break;
               }
           }
       }
       return cookieValue;
   }
   var csrftoken = getCookie('csrftoken');

   function csrfSafeMethod(method) {
       // 这些HTTP方法不要求CSRF包含
       return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
   }
   $.ajaxSetup({
       beforeSend: function(xhr, settings) {
           if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
               xhr.setRequestHeader("X-CSRFToken", csrftoken);
           }
       }
   });
   ```

2. 说明

   上面代码的作用就是让你的ajax的POST方法带上CSRF需要的令牌，它依赖Jquery库，必须提前加载Jquery。这是Django官方提供的解决方案哦。

## 五、装饰器

### 1、单独指定csrf验证需要

1. 说明

   有时候，我们在全站上关闭了CSRF功能，但是希望某些视图还有CSRF防御，那怎么办呢？

   Django为我们提供了一个`csrf_protect(view)`装饰器，使用起来非常方便，如下所示：

2. 示例代码

   ```python
   from django.views.decorators.csrf import csrf_protect
   from django.shortcuts import render

   @csrf_protect
   def xxx_view(request):
       # ...
       return render(request, "index.html")
   ```

### 2、单独指定忽略csrf验证

1. 说明

   有正就有反。在全站开启CSRF机制的时候，有些视图我们并不想开启这个功能。比如，有另外一台机器通过requests库，模拟HTTP通信，以POST请求向我们的Django主机服务器发送过来了一段保密数据。它无法携带CSRF令牌，必然会被403。这怎么办呢？在接收这个POST请求的视图上为CSRF开道口子，不进行验证。这就需要使用Django为我们提供的`csrf_exempt(view)`装饰器了

2. 举个栗子

   ```python
   from django.views.decorators.csrf import csrf_exempt
   from django.http import HttpResponse

   @csrf_exempt
   def xxxx_view(request):
       return HttpResponse('Hello world')
   ```

### 3、确保csrf令牌被设置

1. 说明

   Django还提供了一个装饰器，确保被装饰的视图在返回页面时同时将csrf令牌一起返回。

   这个装饰器是：ensure_csrf_cookie(view)，其使用方法和上面的一样：

2. 举个栗子

   ```python
   from django.views.decorators.csrf import ensure_csrf_cookie
   from django.http import HttpResponse

   @ensure_csrf_cookie
   def xxxx_view(request):
       return HttpResponse('Hello world')
   ```

### 4、 requires_csrf_token(view)

1. 说明

   这个装饰器类似csrf_protect，一样要进行csrf验证，但是它不会拒绝发送过来的请求。

2. 举个栗子

   ```python
   from django.views.decorators.csrf import requires_csrf_token
   from django.shortcuts import render

   @requires_csrf_token
   def xxxx_view(request):
       return render(request, "index.html")
   ```

## 六、面试回答********

面试回答：

​	1 什么是：跨站请求伪造Cross Site Request Forgery

​	2 举例子：什么是跨站请求攻击：用户a 访问可信站点1做业务处理，此时浏览器会保存该网站的cookie，当用户a 访问不可信站点2时，如果站点2有指向站点1的链接时候，那么攻击就用可能发生

​	3 Django怎么做的：使用了csrf的中间件，具体操作是这样的，当浏览器第一次和Django服务交互的时候，

​		后台会生成一个唯一标识码， 放入到前端，同时后台也保存，那么之后再提交数据 服务端就会做csrf的校验，如果通过那么就正常处理，否则返回403

​	4 使用： **后端**

全局使用（禁用）

​	使用中间件操作

局部使用或禁用

from django.views.decorators.csrf import csrf_exempt（不使用CSRF验证）, csrf_protect（使用CSRF校验）

**前端**

Form表单

{%csrf_token%}

Ajax  方式

