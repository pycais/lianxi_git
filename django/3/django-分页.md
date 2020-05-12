# django-分页

## 一、概要

> 分页操作是web开发中比较常见的功能

## 二、实现方式

### 1、框架自带的

1. Pagination

2. # 分页（后端重点）

   就是将我们的数据分成N组，每一组有n个数据，能减轻用户的流量使用，减少不必要客户端内存浪费

   ```
   paginator = Paginator(data, PER_PAGE)
   page = paginator.page(页码数)
   paginator提供的：
   	count对象总数
   		num_pages：页面总数
   		page_range: 页码列表，从1开始

   方法:		page(整数): 获得一个page对象
   page提供的：
   	属性:
   	object_list：	当前页面上所有的数据对象
   	number：	当前页的页码值
   	paginator:	当前page关联的Paginator对象
   方法：
   	has_next()	:判断是否有下一页
   	has_previous():判断是否有上一页
   	has_other_pages():判断是否有上一页或下一页
   	next_page_number():返回下一页的页码
   	previous_page_number():返回上一页的页码	
   	len()：返回当前页的数据的个数

   ```

   实现步骤

   ```
    	# 查出所有数据
       
       # 实例化一个分页器
      
       # 通过传过来的页码 获得page对象
       
       # 把page对象里的数据 我们读取出来， 然后返回给前端，（前端也需要有个页面）
   ```

   代码：

   ```
   def get_data(req):
       # 解析参数
       page_num = req.GET.get("page")
       # 查出所有数据
       data = Engineer.objects.all()
       # 实例化一个分页器
       paginator = Paginator(data, PER_PAGE)
       # 通过传过来的页码 获得page对象
       try:
           page = paginator.page(page_num)
           # 把page对象里的数据 我们读取出来， 然后返回给前端，（前端也需要有个页面）
           result = page.object_list
       except:
           result = []
       return render(req, "data.html", {"data": result})
   ```

   前端分页

   ```
   <!DOCTYPE html>
   <html lang="en">
   <head>
       <meta charset="UTF-8">
       <title>Title</title>
       <link href="http://cdn.static.runoob.com/libs/bootstrap/3.3.7/css/bootstrap.min.css" rel="stylesheet">
   </head>
   <body>
   <ul>
       {% for i in data %}
           <li>{{ i.name }}的年纪是{{ i.age }}</li>
       {% empty %}
           <h1>没有数据啦</h1>
       {% endfor %}
   </ul>

   <nav aria-label="Page navigation">
       <ul class="pagination">
           <li>
               {#        判断是否有前一页的数据#}
               {% if page.has_previous %}
                   <a href="/t07/data?page={{ page.previous_page_number }}" aria-label="Previous">
                       <span aria-hidden="true">上一页</span>
                   </a>
               {% else %}
                   <a href="/t07/data?page=1" aria-label="Previous">
                       <span aria-hidden="true">上一页</span>
                   </a>
               {% endif %}
           </li>
           {#    <li><a href="#">1</a></li>#}
           {#    <li><a href="#">2</a></li>#}
           {#    <li><a href="#">3</a></li>#}
           {#    <li><a href="#">4</a></li>#}
           {#    <li><a href="#">5</a></li>#}
           {% for i in page_range %}
               <li><a href="/t07/data?page={{ i }}">{{ i }}</a></li>
           {% endfor %}


           <li>
               {% if page.has_next %}
                   <a href="/t07/data?page={{ page.next_page_number }}" aria-label="Next">
                       <span aria-hidden="true">下一页</span>
                   </a>
               {% else %}
                   <a href="/t07/data?page={{ page_count }}" aria-label="Next">
                       <span aria-hidden="true">下一页</span>
                   </a>
               {% endif %}
           </li>
       </ul>
   </nav>
   </body>
   </html>
   ```


  
   ```

   ​

### 2、第三方

1. dj-pagination

2. django-pure-pagination

## 三、dj-pagination的使

### 1、安装

> pip install dj-pagination

### 2、注册

1. settings.py文件中。在INSTALLED_APPS加入此应用

   ```
   INSTALLED_APPS = [
       'django.contrib.admin',
       'django.contrib.auth',
       'django.contrib.contenttypes',
       'django.contrib.sessions',
       'django.contrib.messages',
       'django.contrib.staticfiles',
       ...
       'dj_pagination',
   ]
   ```

2. MIDDLEWARE 安装分页中间件

   ```
   MIDDLEWARE = [
       ...
       'dj_pagination.middleware.PaginationMiddleware',
   ]
   ```

### 3、在模板中使用

1. 在需要添加模板的页面中加载标签pagination_tags

   ```
   {% extends 'base.html' %}
   {% load pagination_tags %}
   ```

2. 自动分页

   ```
   {% autopaginate QUERYSET [PAGINATE_BY] [ORPHANS] [as NAME] %}
   # 显示分页的内容
   {% paginate %}
   ```

3. 示例

   ```python
   # views.py
   def pg_list(request):
       films = Film.objects.all()
       return render(request, 'pagination_demo.html', locals())
   ```

   ```django
   # templates
       {% autopaginate films 10 %}
       <table>
           <tr>
               <th>ID</th>
               <th>电影名称</th>
           </tr>

           {% for film in films %}
               <tr>
                   <td>{{ film.id }}</td>
                   <td>{{ film.name }}</td>
               </tr>
           {% endfor %}
       </table>
       {% paginate %}
   ```

### 4、使用自定义模板

1. 说明

   dj-pagination的默认模板很简陋我们如果想美化一下界面可以指定自定义的模板

   默认模板在 dj_pagination\templates\pagination\pagination.html
