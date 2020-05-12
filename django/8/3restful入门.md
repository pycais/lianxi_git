# 什么是restful api

可以总结为一句话：REST是所有Web应用都应该遵守的架构设计指导原则。 
Representational State Transfer，翻译是”表现层状态转化”。 
**面向资源是REST最明显的特征**，对于同一个资源的一组不同的操作。资源是服务器上一个可命名的抽象概念，资源是以名词为核心来组织的，首先关注的是名词。REST要求，必须通过统一的接口来对资源执行各种操作。对于每个资源只能执行一组有限的操作。（7个HTTP方法：GET/POST/PUT/DELETE/PATCH/HEAD/OPTIONS）

# Restful API设计规范

**1，资源**。首先是弄清楚资源的概念。资源就是网络上的一个实体，一段文本，一张图片或者一首歌曲。资源总是要通过一种载体来反应它的内容。文本可以用TXT，也可以用HTML或者XML、图片可以用JPG格式或者PNG格式，JSON是现在最常用的资源表现形式。


**2，统一接口**。RESTful风格的数据元操CRUD（create,read,update,delete）分别对应HTTP方法：GET用来获取资源，POST用来新建资源（也可以用于更新资源），PUT用来更新资源，DELETE用来删除资源，这样就统一了数据操作的接口。


**3，URI**。可以用一个URI（统一资源定位符）指向资源，即每个URI都对应一个特定的资源。要获取这个资源访问它的URI就可以，因此URI就成了每一个资源的地址或识别符。一般的，每个资源至少有一个URI与之对应，最典型的URI就是URL。

**4，无状态**。所谓无状态即所有的资源都可以URI定位，而且这个定位与其他资源无关，也不会因为其他资源的变化而变化。有状态和无状态的区别，举个例子说明一下，

例如要查询员工工资的步骤为第一步：登录系统。第二步：进入查询工资的页面。第三步：搜索该员工。第四步：点击姓名查看工资。这样的操作流程就是有状态的，查询工资的每一个步骤都依赖于前一个步骤，只要前置操作不成功，后续操作就无法执行。如果输入一个URL就可以得到指定员工的工资，则这种情况就是无状态的，因为获取工资不依赖于其他资源或状态，且这种情况下，员工工资是一个资源，由一个URL与之对应可以通过HTTP中的GET方法得到资源，这就是典型的RESTful风格。

**RESTful API还有其他一些规范**。

1：应该将API的版本号放入URL。GET:http://www.xxx.com/v1/friend/123。或者将版本号放在HTTP头信息中。我个人觉得要不要版本号取决于自己开发团队的习惯和业务的需要，不是强制的。

2：URL中只能有名词而不能有动词，操作的表达是使用HTTP的动词GET,POST,PUT,DELETEL。URL只标识资源的地址，既然是资源那就是名词了。

3：如果记录数量很多，服务器不可能都将它们返回给用户。API应该提供参数，过滤返回结果。?limit=10：指定返回记录的数量、?page=2&per_page=100：指定第几页，以及每页的记录数。

# 到底什么是RESTful架构

1. 每一个URI代表一种资源
2. 客户端和服务器之间，传递这种资源的某种表现层
3. 客户端通过四个HTTP动词，对服务端资源进行操作，实现”表现层状态转换“

# HTTP常用动词

- GET（SELECT）：从服务器取出资源
- POST（CREATE or UPDATE）：在服务器创建资源或更新资源
- PUT（UPDATE）：在服务器更新资源（客户端提供改变后的完整资源）
- PATCH（UPDATE）：在服务器更新资源（客户端提供改变的属性）
- DELETE（DELETE）：从服务器删除资源
- HEAD：获取资源的元数据
- OPTIONS：获取信息，关于资源的哪些属性是客户端可以改变的



## 示例

- GET /students：获取所有学生
- POST /students：新建学生
- GET /students/id：获取某一个学生
- PUT /students/id ：更新某个学生的信息（需要提供学生的全部信息）
- PATCH /students/id：更新某个学生的信息（需要提供学生变更部分信息）
- DELETE /students/id：删除某个学生

# restful相关的网络请求状态码

- 200 OK - [GET]：服务器成功返回用户请求的数据
- 201 CREATED -[POST/PUT/PATCH]：用户新建或修改数据成功
- 202 Accepted - [*] ：表示一个请求已经进入后台排队（异步任务）
- 204 NO CONTENT - [DELETE]：表示数据删除成功
- 400 INVALID REQUEST - [POST/PUT/PATCH]：用户发出的请求有错误
- 401 Unauthorized - [*] ：表示用户没有权限（令牌，用户名，密码错误）
- 403 Forbidden - [*]：表示用户得到授权，但是访问是被禁止的
- 404 NOT FOUND - [*]：用户发出的请求针对的是不存在的记录
- 406 Not Acceptable - [*]：用户请求格式不可得
- 410 Gone - [GET] ：用户请求的资源被永久移除，且不会再得到的
- 422 Unprocesable entity -[POST/PUT/PATCH]：当创建一个对象时，发生一个验证错误
- 500 INTERNAL SERVER EROR - [*] ：服务器内部发生错误

# 简单实现

​	方式一

~~~
def stu_apis(request):

    if request.method == "GET":
        # 获取数据
        id = request.GET.get("id")
        try:
            stu = Student.objects.get(pk=int(id))
            data = {
                "code": 0,
                "msg": "OK",
                "data": model_to_dict(stu)
            }
        except Student.DoesNotExist:
            data = {
                "code": 1,
                "msg": "暂无数据",
                "data": None
            }
        return JsonResponse(data)
    elif request.method == "POST":
        # 创建数据
        params = request.POST
        stu, is_created = Student.objects.get_or_create(
            name=params.get("name"),
            age=params.get("age"),
            number=params.get("number")
        )
        create_msg = "创建完毕" if is_created else "数据已存在"
        data = {
            "code": 0,
            "msg": create_msg,
            "data": model_to_dict(stu)
        }
        return JsonResponse(data, status=201)
    elif request.method == "PUT":
        # 修改数据
        params = QueryDict(request.body)
        id = params.get("id")
        obj = Student.objects.get(pk=int(id))

        obj.name = params.get("name", obj.name)
        obj.age = int(params.get("age", obj.age))
        obj.number = params.get("number", obj.number)
        obj.save()

        data = {
            "code": 0,
            "msg": "Updated",
            "data": model_to_dict(obj)
        }
        return JsonResponse(data, status=201)
    elif request.method == "DELETE":
#         删除数据
        params = QueryDict(request.body)
        id = int(params.get("id"))
        Student.objects.get(pk=id).delete()
        data = {
            "code": 0,
            "data": None,
            "msg": "deleted"
        }
        return JsonResponse(data, status=204)
~~~

方式二

~~~
class StuAPI(View):

    def get(self, request):
        # 获取数据
        id = request.GET.get("id")
        try:
            stu = Student.objects.get(pk=int(id))
            data = {
                "code": 0,
                "msg": "OK",
                "data": model_to_dict(stu)
            }
        except Student.DoesNotExist:
            data = {
                "code": 1,
                "msg": "暂无数据",
                "data": None
            }
        return JsonResponse(data)

    def post(self, request):
        # 创建数据
        params = request.POST
        stu, is_created = Student.objects.get_or_create(
            name=params.get("name"),
            age=params.get("age"),
            number=params.get("number")
        )
        create_msg = "创建完毕" if is_created else "数据已存在"
        data = {
            "code": 0,
            "msg": create_msg,
            "data": model_to_dict(stu)
        }
        return JsonResponse(data, status=201)

    def put(self, request):
        # 修改数据
        params = QueryDict(request.body)
        id = params.get("id")
        obj = Student.objects.get(pk=int(id))

        obj.name = params.get("name", obj.name)
        obj.age = int(params.get("age", obj.age))
        obj.number = params.get("number", obj.number)
        obj.save()

        data = {
            "code": 0,
            "msg": "Updated",
            "data": model_to_dict(obj)
        }
        return JsonResponse(data, status=201)

    def delete(self, request):
        #         删除数据
        params = QueryDict(request.body)
        id = int(params.get("id"))
        Student.objects.get(pk=id).delete()
        data = {
            "code": 0,
            "data": None,
            "msg": "deleted"
        }
        return JsonResponse(data, status=204)

~~~

### 视图函数

- FBV
  - function base view
- CBV
  - class base view

### 类视图

- CBV
- 继承自View
- 注册url的时候使用的as_view()
- 入口
  - 不能使用请求方法的名字作为参数的名字
  - 只能接受已经存在的属性对应的参数
  - 定义了一个view
    - 创建了一个类视图对象
    - 保留，拷贝传递进来的属性和参数
    - 调用dispatch方法
      - 分发
      - 如果请求方法在我们的允许的列表中
        - 从自己这个对象中获取请求方法名字小写对应的属性，如果没有找到，会给一个默认http_method_not_allowded
      - 如果请求方法不在我们允许的列表中，直接就是http_method_not_allowed
      - 之后将参数传递，调用函数
- 默认实现了options
  - 获取接口信息，可以获取接口都允许什么请求
- 简化版流程
  - as_view
  - dispath
  - 调用实现请求方法对应的函数名

### 类视图深入拓展

- View
  - 核心
  - dispatch
- TemplateView
  - 多继承的子类
  - View
    - 分发
    - 函数 dispatch
  - ContextMixin
    - 接收上下文
    - 从视图函数传递到模板的内容
    - 函数 get_context_data
  - TemplateResponseMixin
    - 将内容渲染到模板中
    - template_name
    - template_engine
    - response_class
    - content_type
    - 函数 render_to_response
- ListView
  - MultipleObjectTemplateResponseMixin
    - TemplateResponseMixin
    - 获取模板名字
      - 首先根据template_name 
      - 如果没找到
        - 自己根据 应用的名字，关联模型的名字， _list.html 去查找
        - App/book_list.html
  - BaseListView
    - MultipleObjectMixin
      - ContextMixin
      - get_queryset
      - model
    - View
    - 默认实现了get，渲染成了response
- DetailView
  - SingleObjectTemplateResponseMixin
    - TemplateResponseMixin
    - 重写了获取模板名字的方法
  - BaseDetailView
    - View
    - SingleObjectMixin