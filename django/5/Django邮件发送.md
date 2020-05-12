# 配置

~~~
EMAIL_USE_SSL = True

EMAIL_HOST = 'smtp.qq.com'  # 如果是 163 改成 smtp.163.com

EMAIL_PORT = 465

EMAIL_HOST_USER = environ.get("EMAIL_SENDER") # 帐号

EMAIL_HOST_PASSWORD = environ.get("EMAIL_PWD")  # 授权码（****）

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

~~~

注意：邮箱要开启smtp服务 并且记录授权码

https://docs.djangoproject.com/zh-hans/2.0/topics/email/



# 笔记

## 	为什么用

​			及时通知，还有邮箱验证等等

## 	怎么用

~~~
修改setting.py 加入邮箱配置
EMAIL_USE_SSL = True

EMAIL_HOST = 'smtp.qq.com'  # 如果是 163 改成 smtp.163.com

EMAIL_PORT = 465

EMAIL_HOST_USER = "xxx@qq.com" # 帐号

EMAIL_HOST_PASSWORD = "xxxxx"  # 授权码（****）

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
~~~

views里使用

~~~
普通单封邮件
def send_my_mail(req):
    title = "阿里offer"
    message = "恭喜您 成为我们公司CEO"
    email_from = "1625211623@qq.com"
    recs = ["17694871425@163.com", "569677884@qq.com", "ichenyouzhi@163.com"]
    #发送邮件
    send_mail(title, message, email_from, recs)
    return HttpResponse("CEO开始嗨起来")
~~~

~~~
多封普通邮件的发送
def send_emailss(req):
    title1 = "腾讯offer"
    message1 = "恭喜您 被骗了"
    email_from = "1625211623@qq.com"
    title2 = "这是一封挑事的邮件"
    message2 = "大哥大哥别杀我"
    recs1 = ["17694871425@163.com",
            "569677884@qq.com",
            "ichenyouzhi@163.com"]
    recs2 = ["17694871425@163.com",
             "569677884@qq.com",
             "ichenyouzhi@163.com",
             "m18742863100@163.com"]
    senders1 = (title1, message1, email_from, recs1)
    senders2 = (title2, message2, email_from, recs2)
    send_mass_mail((senders1, senders2), fail_silently=False)
    return HttpResponse("OK")
~~~

send_mail和send_mass_mail的区别

​	send_mail每次都连接SMTP服务

​	send_mass_mail 连一次就可以发多个

发送html的邮件

~~~
def email_html(req):
    title = "阿里offer"
    message = "恭喜您 成为我们公司CEO"
    email_from = "493024318@qq.com"
    recs = [
            "liuda@1000phone.com",

            ]
    html_content = '<a href={url}>{url}</a>'.format(url=url)

    msg = EmailMultiAlternatives(title,message, email_from, recs)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    return HttpResponse("OK")
~~~





## 	邮箱验证码

​		1 生成验证码

​		2 准备邮件内容 拼接验证url

​		3 发送邮件

​		4 拿到url里的那个token

​		5 改变邮箱对应用户的状态

生成验证连接发送邮件

~~~
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render
from email_verfiry import myutil
from django.core.cache import cache
# Create your views here.
def get_verify_code(req):
    param = req.GET
    email = param.get('email')
    name = param.get('name')
    #验证邮箱书写规则合法性
    #验证这个邮箱是否在我们的系统注册过了

    #生成验证码
    token = myutil.get_token()
    #拼接验证连接
    verify_url = "http://sharemsg.cn:12348/verify/" + token
    # 保存验证码
    cache.set(token, email, 60)
    # 发送邮件
    title = "欢迎注册1806会员"
    message = "请将如下连接 复制到浏览器访问{url}".format(
        url=verify_url
    )
    email_from = "493024318@qq.com"
    send_mail(title, message, email_from, [email])
    return HttpResponse("注册成功，请查看激活邮件")

~~~

 验证url的正确性

~~~
def verify(req, token):
    email = cache.get(token)
    if email:
     	# 去数据库找Email对应人
        return HttpResponse("修改用户状态，可以使用"+email)
    else:
        return HttpResponse("验证链接不正确")
~~~

