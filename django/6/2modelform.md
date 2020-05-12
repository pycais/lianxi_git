ModelForm

```
ModelForm
    a.  class Meta:
            model,                           # 对应Model的
            fields=None,                     # 字段
            exclude=None,                    # 排除字段
            labels=None,                     # 提示信息
            help_texts=None,                 # 帮助提示信息
            widgets=None,                    # 自定义插件
            error_messages=None,             # 自定义错误信息（整体错误信息from django.core.exceptions import NON_FIELD_ERRORS）
            field_classes=None               # 自定义字段类 （也可以自定义字段）
            localized_fields=('birth_date',) # 本地化，如：根据不同时区显示数据
            如：
                数据库中
                    2016-12-27 05:11:51
                setting中的配置
                    TIME_ZONE = 'Asia/Shanghai'
                    USE_TZ = True
                则显示：
                    2016-12-27 13:11:51
    b. 验证执行过程
        is_valid -> full_clean -> 钩子 -> 整体错误
 
    c. 字典字段验证
        def clean_字段名(self):
            # 可以抛出异常
            # from django.core.exceptions import ValidationError
            return "新值"
    d. 用于验证
        model_form_obj = XXOOModelForm()
        model_form_obj.is_valid()
        model_form_obj.errors.as_json()
        model_form_obj.clean()
        model_form_obj.cleaned_data
    e. 用于创建
        model_form_obj = XXOOModelForm(request.POST)
        #### 页面显示，并提交 #####
        # 默认保存多对多
            obj = form.save(commit=True)
        # 不做任何操作，内部定义 save_m2m（用于保存多对多）
            obj = form.save(commit=False)
            obj.save()      # 保存单表信息
            obj.save_m2m()  # 保存关联多对多信息
 
    f. 用于更新和初始化
        obj = model.tb.objects.get(id=1)
        model_form_obj = XXOOModelForm(request.POST,instance=obj)
        ...
 
        PS: 单纯初始化
            model_form_obj = XXOOModelForm(initial={...})

```

