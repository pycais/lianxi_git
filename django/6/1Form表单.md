# Form表单

## 一、概要

> Django提供了一个丰富的框架来帮助创建表单和处理表单数据

## 二、Form表单的功能

- 自动生成HTML表单元素
- 检查表单数据的合法性
- 如果验证错误，重新显示表单（数据不会重置）
- 数据类型转换（字符类型的数据转换成相应的Python类型）

## 三、Form相关的对象包括

- Widget：用来渲染成HTML元素的工具，如：forms.Textarea对应HTML中的`<textarea>`标签
- Field：Form对象中的一个字段，如：EmailField表示email字段，如果这个字段不是有效的Email地址格式，就会产生错误。
- Form：一系列Field对象的集合，负责验证和显示HTML元素
- Form Media：用来渲染表单的CSS和JavaScript资源。

## 四、基本使用

### 1、说明

> Form对象封装了一系列Field和验证规则，Form类都必须直接或间接继承自django.forms.Form，定义Form有两种方式:
>
> 1. 直接继承Form
> 2. 结合Model，继承django.forms.ModelForm

### 2、语法格式

1. 直接继承

   ```python
   class XXXForm(forms.Form):
      pass
   ```

2. 继承ModelForm

   ```python
   class XXX(models.Model):
       字段 = models.CharField(max_length=30)
       字段 = models.CharField(max_length=20)

   class XXXForm(ModelForm):
       class Meta:
           model = XXX
           field = ('字段', '字段')  # 只显示model中指定的字段
   ```


### 3、示例代码

1. models

   ```python
   class Shop(models.Model):
       title = models.CharField('标题', max_length=30)
       content = models.CharField('内容', max_length=20)
       class Meta:
           db_table = 'T_SHOP'
   ```

2. ModelForm

   ```python
   class ShopForm(ModelForm):
       class Meta:
           model = models.Shop
           fields = ('title', 'content')  # 只显示model中指定的字段
   ```

3. views

   ```；python
   from django.shortcuts import render

   # Create your views here.
   from .forms import ShopForm

   def add_shop(request):
       if request.method == "POST":
           form = ShopForm(request.POST)
           if form.is_valid():  # 所有验证都通过
               # 处理表单数据
               title = form.cleaned_data['title']
               print(title)
               # content = form.cleaned_data['content']
               # 保存数据
               form.save()
               return render(request, 'shop/add_shop.html', {"shop_form": form})
       else:
           form = ShopForm()
       return render(request, 'shop/add_shop.html', {"shop_form": form}) 
   ```

4. 模板中使用

   ```django
   <form action="{% url 'add' %}" method="post">
       {% csrf_token %}
       {{ shop_form }}
       <input type="submit" value="提交"/>
   </form>
   ```

## 五、常用的Form属性

### 1、BooleanField

1. 类

   ```python
   class BooleanField(**kwargs)
   ```

2. 参数

   - 默认的Widget：CheckboxInput
   - 空值：False
   - 规范：Python 的True 或 False。
   - 如果字段带有required=True，验证值是否为True（例如复选框被勾上）。 
   - 错误信息的键：required

3. 举个栗子

   ```python
    sex = forms.BooleanField(label='接受协议', required=True,error_messages={'required', u'必选'})
   ```

### 2、CharField

1. 类

   ```python
   class CharField(**kwargs)
   ```

2. 参数

   - 默认的Widget：TextInput
   - 空值：''（一个空字符串）
   - 规范化为：一个Unicode 对象。
   - 如果提供，验证max_length 或min_length。 否则，所有的输入都是合法的。
   - 错误信息的键：required, max_length, min_length

3. 举个栗子

   ```python
    from django.core.validators import RegexValidator
    name = forms.CharField(label='名称', max_length=16, min_length=6,
                error_messages={'required': u'标题不能为空',
                                'min_length': u'标题最少为6个字符',
                                'max_length': u'标题最多为16个字符'}
                           validators=[RegexValidator('\d+','只能是数字') ]
                          )
   ```

### 3、ChoiceField

1. 类

   ```
    class ChoiceField(**kwargs)
   ```

2. 参数说明

   - 默认的Widget：Select
   - 空值：' '（一个空字符串）
   - 规范化为：一个Unicode 对象。
   - 验证给定的值在选项列表中存在。
   - 错误信息的键：required, invalid_choice
   - invalid_choice：错误消息可能包含%(value)s，它将被选择的选项替换掉。接收一个额外的必选参数：choices用来作为该字段选项的一个二元组组成的可迭代对象（例如，列表或元组）或者一个可调用对象。

3. 举个栗子

   ```
    city = forms.ChoiceField(choices=[(1, '上海'), (2, '北京',), (3, '广州')])
   ```

### 4、DateField

1. 类

   ```python
   class DateField(**kwargs)
   ```

2. 参数说明

   - 默认的Widget：DateInput
   - 空值：None
   - 规范化为：一个Python datetime.date 对象。
   - 验证给出的值是一个datetime.date、datetime.datetime 或指定日期格式的字符串。
   - 错误信息的键：required, invalid
   - input_formats：一个格式的列表，用于转换一个字符串为datetime.date 对象

3. 举个栗子

   ```python
   create_date = forms.DateField(label='选择时间', input_formats=['%Y-%m-%d'])
   ```

### 5、DateTimeField

1. 类

   ```python
   class DateTimeField(**kwargs)
   ```

2. 参数说明

   - 默认的Widget：DateInput
   - 空值：None
   - 规范化为：一个Python datetime.date 对象。
   - 验证给出的值是一个datetime.date、datetime.datetime 或指定日期格式的字符串。
   - 错误信息的键：required, invalid
   - input_formats：一个格式的列表，用于转换一个字符串为datetime.date 对象。

3. 举个栗子

   ```python
   create_date = forms.DateTimeField(label='选择时间', input_formats=[''%Y-%m-%d %H:%M:%S'])
   ```

### 6、DecimalField

1. 类

   ```python
   class DecimalField(**kwargs)
   ```

2. 参数说明

   - 默认控件：[`NumberInput`]当[`Field.localize`]为 `False`，否则[`TextInput`]。

   - 空值： `None`

   - 规范化为：Python `decimal`。

   - 验证给定的值是小数。前导和尾随空白被忽略。

   - 错误信息键：`required`，`invalid`，`max_value`， `min_value`，`max_digits`，`max_decimal_places`， `max_whole_digits`

   - max_value

     最大值

   - min_value

     最下至

   - max_digits

     允许在数值中允许的最大位数（小数点前的数字加上小数点后的数字，前面的零除去）


   - decimal_places

     允许的最大小数位数。


3. 举个栗子

   ```python
    price = forms.DecimalField(label='价格', max_digits=10, decimal_places=2)
   ```

### 7、FileField

1. 类

   ```python
   class FileField(**kwargs)
   ```

2. 参数说明

   - 默认小部件： ClearableFileInput
   - 空值： `None`
   - 规范化为：`UploadedFile`将文件内容和文件名称封装到单个对象中的对象。
   - 可以验证非空文件数据已被绑定到表单。
   - 错误信息键：`required`，`invalid`，`missing`，`empty`， `max_length`

3. 举个栗子

   ```
   file = forms.FileField(allow_empty_file=True)
   ```

### 8、ImageField

1. 类

   ```python
   class ImageField(**kwargs)
   ```

2. 参数说明

   - 默认小部件： ClearableFileInput
   - 空值： None
   - 规范化为：`UploadedFile`将文件内容和文件名称封装到单个对象中的对象。
   - 验证文件数据是否已绑定到表单，并且该文件是Pillow可以理解的图像格式。
   - 错误信息键：`required`，`invalid`，`missing`，`empty`， `invalid_image`

3. 举个栗子

   ```python
    img =  forms.ImageField(allow_empty_file=True)
   ```

### 9、EmailField

1. 类

   ```python
   class EmailField(**kwargs)
   ```

2. 参数说明

   - 默认的Widget：EmailInput
   - 空值：''（一个空字符串）
   - 规范化为：一个Unicode 对象。
   - 验证给出的值是一个合法的邮件地址，使用一个适度复杂的正则表达式。
   - 错误信息的键：required, invalid
   - 具有两个可选的参数用于验证，max_length 和min_length。如果提供，这两个参数确保字符串的最大和最小长度。

3. 举个栗子

   ```python
    img =  forms.EmailField(lable='邮箱')
   ```

### 10、ModelChoiceField

1. 类

   ```python
   class ModelChoiceField(**kwargs)
   ```

2. 参数说明

   - 默认的Widget：Select
   - 空值：None
   - 规范化为：一个模型实例。
   - 验证给定的id存在于查询集中。
   - 错误信息的键：required, invalid_choice
   - 可以选择一个单独的模型对像，适用于表示一个外键字段。 ModelChoiceField默认widet不适用选择数量很大的情况，在大于100项时应该避免使用它。


   - 可选参数

     queryset 将导出字段选择的模型对象的QuerySet，将用于验证用户的选择。

     ModelChoiceField也有两个可选参数：

     - empty_label

       默认情况下，ModelChoiceField使用的<select>小部件将在列表顶部有一个空选项。您可以使用empty_label属性更改此标签的文本（默认为"---------"），也可以禁用空白标签完全通过将empty_label设置为None：
     - to_field_name

       此可选参数用于指定要用作字段窗口小部件中选项的值的字段。确保它是模型的唯一字段，否则选定的值可以匹配多个对象。默认情况下，它设置为None，在这种情况下，将使用每个对象的主键


3. 举个栗子

   ```python
   address = forms.ModelChoiceField(queryset=models.Address.objects.filter(uid=2)
                                        , empty_label=None
                                        , to_field_name=None)
   ```

## 六、From常用方法

### 1、is_valid

1. 说明

   提交的数据验证通过

2. 方法

   ```
   form.is_valid()
   ```

3. 返回值

   bool

### 2、cleaned_data

1. 说明

   获取提交的form数据

2. 方法

   ```
   form.cleaned_data
   ```

3. 返回

   字典

4. 示例代码

   ```python
   form.cleaned_data['username']
   ```

### 3、fields

1. 说明

   获取form表达的所有属性

2. 方法

   ```
   form.fields
   ```

3. 返回值

   字典

4. 举个栗子

   ```python
   f.fields['username']
   ```

### 4、initial

1. 说明

   给html元素赋默认值

2. 举个栗子

   ```
   username = forms.CharField(initial='class')
   或者
   user = User(initial={'username','这个是默认值'})
   ```

### 5、has_changed

1. 说明

   检查表单数据是否已从初始数据更改

2. 方法

   ```
   froms.has_changed()
   ```

3. 返回值

   bool

## 七、重写验证

1. 说明

2. 举个栗子

3. 注意事项
   - 函数名就必须为clean_字段名
   - 必须有返回值
   - 只能拿自己当前字段值
   - raise ValidationError('xxx')

   ```python
    class UserFrom(forms.Form):
   	    # 自定义方法（局部钩子），密码必须包含字母和数字
       def clean_password(self):
           if self.cleaned_data.get('password').isdigit() or self.cleaned_data.get('password').isalpha():
               raise ValidationError('密码必须包含数字和字母')
           else:
               return self.cleaned_data['password']

       def clean_valid_code(self):  # 检验验证码正确；之前生成的验证码保存在了了session中
           if self.cleaned_data.get('valid_code').upper() == self.request.session.get('valid_code'):
               return self.cleaned_data['valid_code']
           else:
               raise ValidationError('验证码不正确')

       # 自定义方法（全局钩子, 检验两个字段），检验两次密码一致;
       def clean(self):
           if self.cleaned_data.get('password') != self.cleaned_data.get('password2'):
               raise ValidationError('密码不一致')
           else:
               return self.cleaned_data

       # 注意，上面的字典取值用get, 因为假如在clean_password中判断失败，那么没有返回值，最下面的clean方法直接取值就会失败
   ```

## 附:完整代码

1. 示例代码

   ```python
   class UserFrom(forms.Form):
       sex = forms.BooleanField(label='用户名', required=True, error_messages={'required': u'必选'})
       password = forms.CharField(label='密码', widget=forms.PasswordInput(attrs={'placeholder': '请输入密码'}))
       confirm_password = forms.CharField(label='密码', widget=forms.PasswordInput(attrs={'placeholder': '请再次输入密码'}))
       name = forms.CharField(label='名称', max_length=16, min_length=6,
                              error_messages={'required': u'标题不能为空',
                                              'min_length': u'标题最少为6个字符',
                                              'max_length': u'标题最多为16个字符'})
       # 下拉框
       city = forms.ChoiceField(choices=[(1, '上海'), (2, '北京',), (3, '广州')])
       create_date = forms.DateField(label='选择时间', input_formats=['%Y-%m-%d'])
       price = forms.DecimalField(label='价格', max_digits=10, decimal_places=2)
       head = forms.FileField(allow_empty_file=True)
       img = forms.ImageField(allow_empty_file=True)
       email = forms.EmailField(required=False,
                                error_messages={'required': u'邮箱不能为空',
                                                'invalid': u'邮箱格式错误'},
                                widget=forms.TextInput(
                                    attrs={'class': "form-control",
                                           'placeholder': u'邮箱'})
                                )
       address = forms.ModelChoiceField(queryset=models.Address.objects.filter(uid=2)
                                        , empty_label=None
                                        , to_field_name=None)
       def clean_password(self):
           if self.cleaned_data.get('password').isdigit() or self.cleaned_data.get('password').isalpha():
               raise ValidationError('密码必须包含数字和字母')
           else:
               return self.cleaned_data['password']

       def clean_valid_code(self): 
           if self.cleaned_data.get('valid_code').upper() == self.request.session.get('valid_code'):
               return self.cleaned_data['valid_code']
           else:
               raise ValidationError('验证码不正确')

       def clean(self):
           if self.cleaned_data.get('password') != self.cleaned_data.get('confirm_password'):
               raise ValidationError('密码不一致')
           else:
               return self.cleaned_data

   ```

## 八、表单渲染的选项

### 1、概要

> 对于`<label>/<input>` 对，还有几个输出选项：
>
> - `{{ form.as_table }}` 以表格的形式将它们渲染在`<tr>` 标签中
> - `{{ form.as_p }}` 将它们渲染在`<p>` 标签中
> - `{{ form.as_ul }}` 将它们渲染在`<li>` 标签中
>
> 注意，你必须自己提供`<table>` 或`<ul>` 元素。

### 2、举个栗子

1. form.as_p 

   ```django
   <form action="">
       <p>
           <label for="id_username">Username:</label>
           <input id="id_username" maxlength="100" name="username" type="text" required="">
       </p>
       <p>
           <label for="id_password">Password:</label>
           <input id="id_password" maxlength="100" name="password" placeholder="password" type="password" required="">
       </p>
       <p>
           <label for="id_telephone">Telephone:</label> <input id="id_telephone" name="telephone" type="number" required="">
       </p>
       <p>
           <label for="id_email">Email:</label> <input id="id_email" name="email" type="email" required="">
       </p>
       <p>
           <label for="id_is_married">Is married:</label> <input id="id_is_married" name="is_married" type="checkbox">
       </p>
       <input type="submit" value="注册">
   </form>
   ```

2. 综合

   ```django
   #-----------------------------------------models.py
   from django.db import models
   class Info(models.Model):
       name = models.CharField(max_length=64)
       sex = models.CharField(max_length=64)
       birthday = models.CharField(max_length=64)
       age=models.CharField(max_length=64)
       qualification=models.CharField(max_length=64)
       job=models.CharField(max_length=64)
       email=models.CharField(max_length=64,default='')
   class Hobby(models.Model):
       item=models.CharField(max_length=64)

   #-----------------------------------------form.py

   from django import forms
   from app01 import models
   from django.core.exceptions import ValidationError

   class InfoForm(forms.Form):
       def validate_name(value):
           try:
               models.Info.objects.get(name=value)
               raise ValidationError('%s 的信息已经存在!'%value)
           except models.Info.DoesNotExist:
               pass
       sex_choice=((0,'男'),
                   (1,'女'))#select的数据可以像这样写,也可以在另外一张表中动态去拿
       name = forms.CharField(validators=[validate_name],label='姓名',error_messages={'required':'必填'})

       age = forms.CharField(label='年龄',error_messages={'required':'必填'})

       # sex = forms.CharField(label='性别',error_messages={'required':'必填',},)
       sex=forms.IntegerField(widget=forms.widgets.Select(choices=sex_choice,
    attrs={'class':'setform2'} ))
       birthday = forms.CharField(label='生日',error_messages={'required':'必填'})

       qualification = forms.CharField(label='学历',error_messages={'required':'必填'},widget=forms.TextInput(attrs={'class':'formset','placeholder':'本科' }))
       email=forms.EmailField(max_length=100,min_length=10)
       job = forms.CharField(label='工作',error_messages={'required':'必填'})
       def  __init__(self,*args,**kwargs):
           super(Info_form,self).__init__(*args,**kwargs)      		self.fields['hobby']=forms.CharField(widget=forms.widgets.Select(choices=models.Hobby.objects.values_list('id','item')))

   #-----------views.py
   from django.shortcuts import render,HttpResponse

   def add_info(req):
       if req.method=='POST':
           Info_form_obj=Info_form(req.POST)
           if Info_form_obj.is_valid():
               Info.objects.create(name=Info_form_obj.cleaned_data['name'],
                                   age=Info_form_obj.cleaned_data['age'],
                                   sex=Info_form_obj.cleaned_data['sex'],
                                   birthday=Info_form_obj.cleaned_data['birthday'],
                                   qualification=Info_form_obj.cleaned_data['qualification'],
                                   job=Info_form_obj.cleaned_data['job']
                                )
               return HttpResponse('添加成功!')
           else:
               error_obj=Info_form_obj.errors
               print('***************')
               print(type(error_obj))#<class 'django.forms.utils.ErrorDict'>
               print(error_obj['name'][0])#必填
               print(error_obj.get('age'))#<ul class="errorlist"><li>必填</li></ul>
               return render(req,'add_info.html',{'form_obj':Info_form_obj,'error_obj':error_obj})
       Info_form_obj=Info_form()
       return render(req,'add_info.html',{'form_obj':Info_form_obj})

   #------add_info.html
   <!DOCTYPE html>
   <html lang="en">
   <head>
       <meta charset="UTF-8">
       <title>添加个人信息</title>
       <style>
           .formset{
               color: rebeccapurple;
               border: dashed cadetblue;
           }
       </style>
   </head>
   <body>
        <form action="{% url 'add_info' %}" method="post">
            <p>姓名{{ form_obj.name }}{{ error_obj.name.0 }}</p>
            <p>年龄{{ form_obj.age }}{{ error_obj.age.0 }}</p>
            <p>生日{{ form_obj.birthday }}{{ error_obj.birthday.0 }}</p>
            <p>工作{{ form_obj.job }}<span>{{ error_obj.job }}</span></p>
            <p>学历{{ form_obj.qualification }}<span>{{ error_obj.qualification }}</span></p>
            <p>性别{{ form_obj.sex }}<span>{{ error_obj.sex }}</span></p>
            <p>邮箱{{ form_obj.email }}<span>{{ error_obj.email }}</span></p>
            <p>爱好{{ form_obj.hobby }}<span>{{ error_obj.hobby }}</span></p>
            {{ form_obj.as_p }}
              <input type="submit" value="提交"><br>
             {% csrf_token %}
        </form>
   </body>
   </html>
   ```
