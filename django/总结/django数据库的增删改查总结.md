

# 各种参数获取方式

### 在url中获取参数

~~~python
例如：www.xumingr.cn:3389/index?id=1

id = request.GET.get("id")

此时id的值便是字符串1
~~~

### 从数据库中查找数据

~~~python
name = User.objects.get(id=id)
print(name)
# 输出结果为：User object 
# 返回的是User的对象，使用时还需要实例属性
~~~

## 数据库的增删改查

#### 增加：

#####1.实例化对象名.save()

~~~python
def add_movie_one(req):
    # 实例化
    data = small_movie()
    # 赋值
    data.name = "东京不太热"
    data.url = "http://www.83ys.com"
    data.look_num = 10
    # 将对象写入到我们的数据表
    data.save()
    print(data)
    return HttpResponse("ok")
~~~

##### 2.create()函数创建

~~~python

~~~

#### 更新：

##### 1.实例化对象名.save()

~~~python
def update_movie_one(request):
#     解析参数 id
    id = request.GET.get("id")
#     获取数据
    movie = small_movie.objects.get(pk=id)
#     更新 你想更新的字段
    movie.name = "王二小"
    movie.sb = "元宵节"
#       保存数据
    movie.save()
#      返回一个响应结果
    return HttpResponse("更新完毕")
~~~

##### 2.update()函数更新

~~~python
def update_movie_two(req):
    # 解析参数
    id = req.GET.get("id")
# 查询数据 以及更新更新
    small_movie.objects.filter(pk=id).update(
        name="呵呵哒",
        url="www.baidu.com"
    )
#     返回结果
    return HttpResponse("收工")
~~~

#### 删除：有物理删除和逻辑删除

##### 1.物理删除delete()函数删除

​	两种删除方式

~~~python
def delete_movie_one(req):
    # 解析参数
    id = req.GET.get("id")
    # 获取数据
    movie = small_movie.objects.get(id=id)
    # 删除数据
    movie.delete()
    # 返回结果
    return HttpResponse("KO")
~~~

##### 2.逻辑删除：

​	就是把数据库表中的is_delete修改一下，其本质上还是更新

~~~python

~~~

#### 查询

##### 基本查询语句

~~~python
def get_data(req):
    # 获取全部
    # data = small_movie.objects.all()
    # print(data)
    # print(type(data))

    # 获取单个对象
    # try:
    #     data = small_movie.objects.get(name="呵呵哒")
    #     print(data)
    # except small_movie.DoesNotExist:
    #     return HttpResponse("木有数据")
    # except small_movie.MultipleObjectsReturned:
    #     return HttpResponse("数据过多")

    # 查询出所有没被删除的数据
    # data = small_movie.objects.filter(is_delete=False)
    # print(data)
    # print(type(data))

    # 查询被删除的数据
    # data = small_movie.objects.exclude(is_delete=False)
    # print(data)

    # 查询以某个字符串开头的数据 比如以呵呵开头
    # data = small_movie.objects.filter(name__startswith="呵呵")
    # print(data)
    # print(type(data))
    # print(data.first().id)

    # 查询以某个字符串结尾的数据 比如以呵呵结尾
    # data = small_movie.objects.filter(name__endswith="啊实打实哒")
    # print(data)
    #
    # # 包含
    # data = small_movie.objects.filter(name__contains="不太")
    # print(data)

    # 按照日期搜索
    # 按照年份
    # data = small_movie.objects.filter(create_time__year=2018)
    # print(data)
    # # 按照月份查
    # data = small_movie.objects.filter(create_time__month=2)
    # print(data)

    # 大于小于的问题
    # data = small_movie.objects.filter(look_num__gt=10)
    # print(data)

    # in的使用
    # data = small_movie.objects.filter(look_num__in=[2, 10])
    # print(data)
    return HttpResponse("OK")
~~~

##### 原生SQL语句查询

~~~python

def fetch_to_dict(cursor):
    desc = [i[0] for i in cursor.description]
    return [dict(zip(desc, i)) for i in cursor.fetchall()]

def get_data_next(req):
    sql = """
        SELECT
          id,name, url 
        FROM 
            small_movie
        ORDER BY 
            create_time
    """
    con = db.connection
    cursor = con.cursor()
    cursor.execute(sql)
    data = fetch_to_dict(cursor)
    print(data)
    return HttpResponse("OK")
~~~

##### 分组和聚合：annotate和aggregate（重新查资料）

## 连表的查询操作

### 一对一查询

​	首先时model中的表

~~~python
class Idcard(models.Model):
    number = models.CharField(
        max_length=20,
        verbose_name="身份证编号"
    )
    origin = models.CharField(
        max_length=100,
        verbose_name="签发机关"
    )
    create_time = models.DateField(
        auto_now_add=True,
        verbose_name='签发时间'
    )

class Humen(models.Model):
    sex_tyeps = (
        ("1", "男"),
        ("2", "女"),
        ("3", "保密")
    )
    name = models.CharField(
        max_length=20
    )
    sex = models.CharField(
        max_length=2,
        choices=sex_tyeps
    )
    idcard = models.OneToOneField(
        Idcard,
        verbose_name="身份证",
        on_delete=models.SET_NULL, # 删除保护
        null=True
    )
~~~

#### 正向查询：

~~~python
# 查询（正向） 查出人名是 呵呵哒的身份证的签发单位
def get_idcard_by_humen(req):
    humen = Humen.objects.get(
        pk=1
    )
    # 获取签发机构
    return HttpResponse(humen.idcard.number)
~~~

#### 反向查询

##### 其中对带有元组性别选择的查询不是其平常那样去查询

```python
# 查询（反向） 查出来 签发机构 华山派出所的 人
def get_humens_by_idcard(req):
    idcard = Idcard.objects.get(origin="华山派出所")
    # 通过反向关系 拿到数据
    humen = idcard.humen
    # 性别查询  获取性别值对应的描述信息
    print(humen.get_sex_display())
    return HttpResponse(humen.name)
```

##### 删除必选先删除主表信息，然后才能删除副标的数据

```python
def delete_humen(req):
    Humen.objects.get(pk=1).delete()
    return HttpResponse("ok")
def delete_idcard(req):
    Idcard.objects.get(pk=4).delete()
    return HttpResponse("OK")
```

### 一对多查询

​	建表信息在一对一的下面

#### 正相查询

```python
def get_staff_by_company(req):
    com = Company.objects.get(pk=1)
    # 通过公司查询人的身份证号
    print(com.staff.idcard.number)
    return HttpResponse("OK")
```

#### 反向查询

```python
# 给出人的信息 查询出所有跟这个人有关公司
def get_company_by_humen(req):
    # 查询人
    humen = Humen.objects.get(pk=6)
    # 跟人有关系的公司
    # coms = humen.company_set.all()
    coms = humen.company_set.filter(
        name__endswith="达达"
    )
    for i in coms:
        print(i.name)

    return HttpResponse("OK")
```

### 多对多查询

建表信息

```python
class Book(models.Model):
    name = models.CharField(
        max_length=20,
        verbose_name="书名"
    )
    price = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="价格"
    )

class Author(models.Model):
    name = models.CharField(
        max_length=20
    )
    books = models.ManyToManyField(
        Book,
        verbose_name="书"
    )
    
# ManyToManyField 相当于下面的情况
# class BookAuthorMap(models.Model):
#     book = models.ForeignKey(
#         Book
#     )
#     author = models.ForeignKey(
#         Author
#     )
#     class Meta:
#           联合约束
#         unique_together = ["book", "author"]
```

#### 多对多的数据创建

```python
# 多对多数据的创建
def add_author(req):
    # 先创建book
    book = Book.objects.create(
        name="python进阶",
        price=18
    )
    # 先要有我们的作者数据
    author = Author.objects.create(
        name="达达",
    )
    # 然后再去添加对应的多对多的信息
    author.books.add(book)
    # author.books = [book]
    # 保存数据
    author.save()
    return HttpResponse("OK")
```

#### 多对多的数据删除

```python
# 删除 作者的书籍
def delete_book(req):
    # 获取数据
    book = Book.objects.get(pk=2)
    author = Author.objects.first()

    # 删除对应的书籍数据
    author.books.remove(book)
    author.save()

    return HttpResponse("OK")
```

#### 正向查找

```python
# 通过作者查书籍 正向的
def get_book_by_author(req):
    # 获取作者
    author = Author.objects.get(pk=2)
    # 获取作者相关的书籍信息
    books = author.books.all()

    print(author.books)
    print(type(author.books))
    print("--"*40)
    for i in books:
        print(i.name)

    return HttpResponse("OK")
```

#### 反向查找

```
# 反向的： 通过书籍找作者
def get_author_by_book(req):
    book = Book.objects.get(pk=3)
    # 通过作者的类名小写_set 来获取反向关系
    authors = book.author_set.all()
    for i in authors:
        print(i.name)
	
    return HttpResponse("OK")
```

## 还有一个优化查询另查资料