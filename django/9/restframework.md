### 重量级RESTful

官方网站：

~~~
https://www.django-rest-framework.org/
~~~

中文翻译网站:

~~~
https://q1mi.github.io/Django-REST-framework-documentation/
~~~



- django-rest-framework
- REST难点
  - 模型序列化
    - 正向序列化
      - 将模型转换成JSON
    - 反向序列化
      - 将JSON转换成模型
  - serialization
    - 在模块serializers
      - HyperLinkedModelSerializer
        - 序列化模型，并添加超链接
      - Serializer
        - 手动序列化
      - ModelSerializer
        - 模型序列化器
  - 双R
    - Request
      - rest_framework.request
      - 将Django中的Request作为了自己的一个属性 _request
      - 属性和方法
        - content_type
        - stream
        - query_params
        - data
          - 同时兼容  POST,PUT,PATCH
        - user
          - 可以直接在请求上获取用户
          - 相当于在请求上添加一个属性，用户对象
        - auth
          - 认证
          - 相当于请求上添加了一个属性，属性值是token
        - successful_authenticator
          - 认证成功
    - Response
      - 依然是HttpResponse的子类
      - 自己封装的
        - data 直接接受字典转换成JSON
        - status  状态码
      - 属性和方法
        - rendered_content
        - status_text
  - APIView
    - renderer_classes
      - 渲染的类
    - parser_classes
      - 解析转换的类
    - authentication_classes
      - 认证的类
    - throttle_classes
      - 节流的类
      - 控制请求频率的
    - permission_classes
      - 权限的类
    - content_negotiation_class
      - 内容过滤类
    - metadata_class
      - 元信息的类
    - versioning_class
      - 版本控制的类
    - as_view()
      - 调用父类中的as_view -> dispatch
        - dispatch被重写
        - **initialize_request**
          - 使用django的request构建了一个REST中的Request
        - initial
          - perform_authentication
            - 执行用户认证
            - 遍历我们的认证器
              - 如果认证成功会返回一个元组
              - 元组中的第一个元素就是 user
              - 第二个元素就是 auth，token
          - check_permissions
            - 检查权限
            - 遍历我们的权限检测器
              - 只要有一个权限检测没通过
              - 就直接显示权限被拒绝
              - 所有权限都满足，才算是拥有权限
          - check_throttles
            - 检测频率
            - 遍历频率限制器
              - 如果验证不通过，就需要等待
          - finalize_response
            - 封装了Response
        - csrf_exempt
          - 所有APIView的子类都是csrf豁免的
  - 错误码
    - 封装 status模块中
    - 实际上就是一个常量类
  - 针对视图函数的包装
    - CBV
      - APIView
    - FBV
      - 添加 @api_view装饰器
      - 必须手动指定允许的请求方法



### APIView

- 子类
  - generics包中
  - GenericAPIView
    - 增加的模型的获取操作
    - get_queryset
    - get_object
      - lookup_field 默认pk
    - get_serializer
    - get_serializer_class
    - get_serializer_context
    - filter_queryset
    - paginator
    - paginate_queryset
    - get_paginated_response
  - CreateAPIView
    - 创建的类视图
    - 继承自GenericAPIView
    - 继承自CreateModelMixin
    - 实现了post进行创建
  - ListAPIView
    - 列表的类视图
    - 继承自GenericAPIView
    - 继承自ListModelMixin
    - 实现了get
  - RetrieveAPIView
    - 查询单个数据的类视图
    - 继承自GenericAPIView
    - 继承自RetrieveModelMixin
    - 实现了get  
  - DestroyAPIView
    - 销毁数据的类视图，删除数据的类视图
    - 继承自GenericAPIView
    - 继承自DestroyModelMixin
    - 实现了delete
  - UpdateAPIView
    - 更新数据的类视图
    - 继承自GenericAPIView
    - 继承自UpdateModelMixin
    - 实现了 put,patch
  - ListCreateAPIView
    - 获取列表数据，创建数据的类视图
    - 继承自GenericAPIView
    - 继承自ListModelMixin
    - 继承自CreateModelMixin
    - 实现了  get,post
  - RetrieveUpdateAPIView
    - 获取单个数据，更新单个数据的类视图
    - 继承自GenericAPIView
    - 继承自RetrieveModelMixin
    - 继承自UpdateModelMixin
    - 实现了 get, put, patch
  - RetrieveDestroyAPIView
    - 获取单个数据，删除单个数据
    - 继承自GenericAPIView
    - 继承自RetrieveModelMixin
    - 继承自DestroyModelMixin
    - 实现了  get, delete
  - RetrieveUpdateDestroyAPIView
    - 获取单个数据，更新单个数据，删除单个数据的类视图
    - 继承自GenericAPIView
    - 继承自RetrieveModelMixin
    - 继承自UpdateModelMixin
    - 继承自DestroyModelMixin
    - 实现了 get, put, patch, delete
- mixins
  - CreateModelMixin
    - create
    - perform_create
    - get_success_headers
  - ListModelMixin
    - list
      - 查询结果集，添加分页，帮你序列化
  - RetrieveModelMixin
    - retrieve
      - 获取单个对象并进行序列化
  - DestroyModelMixin
    - destroy
      - 获取单个对象
      - 调用执行删除
      - 返回Respon  状态码204
    - perform_destroy
      - 默认是模型的delete
      - 如果说数据的逻辑删除
        - 重写进行保存
  - UpdateModelMixin
    - update
      - 获取对象，合法验证
      - 执行更新
    - perform_update
    - partial_update
      - 差量更新，对应的就是patch
- viewsets
  - ViewSetMixin
    - 重写as_view
  - GenericViewSet
    - 继承自GenericAPIView
    - 继承自ViewSetMixin
  - ViewSet
    - 继承自APIView
    - 继承自ViewSetMixin
    - 默认啥都不支持，需要自己手动实现
  - ReadOnlyModelViewSet
    - 只读的模型的视图集合
    - 继承自RetrieveModelMixin
    - 继承自ListModelMixin
    - 继承自GenericViewSet
  - ModelViewSet
    - 直接封装对象的所有操作
    - 继承自GenericViewSet
    - 继承自CreateModelMixin
    - 继承自RetrieveModelMixin
    - 继承自UpdateModelMixin
    - 继承自DestroyModelMixin
    - 继承自ListModelMixin

拓展

request对象的data默认是不可修改 如果非要修改 那么我们可以进行下面的设置

```
request.query_params._mutable = True
或者request.data._mutable = True
然后我们修改里面的一个数据
self.request.data["h"] = 1
```