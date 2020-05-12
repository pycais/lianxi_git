## 1 WSGI介绍

1. 概要

   **WSGI** (Python Web Server Gateway Interface, Python Web服务器网关接口)是一个Web服务器和Web应用程序之间的标准化接口，用于增进应用程序在不同的Web服务器和框架之间的可移植性。关于该标准的官方说明可以参考[PEP333](http://www.python.org/dev/peps/pep-0333)。

2. WSGI规范如下：

   服务器的请求处理程序中要调用符合**WSGI**规范的网关接口；

   网关接口调用应用程序，并且要定义**start_response(status, headers)**函数，用于返回响应；

   应用程序中实现一个函数或者一个可调用对象**webapp(environ, start_response)**。其中**environ**是环境设置的字典，由服务器和**WSGI网关接口**设置，**start_response**是由网关接口定义的函数。

## 2、uwsgi

1. 说明

   与**WSGI**一样是一种通信协议，是**uWSGI**服务器的独占协议，用于定义传输信息的类型(type of information)，每一个uwsgi packet前4byte为传输信息类型的描述，与**WSGI**协议是两种东西，据说该协议是**fcgi**协议的10倍快。

## 3、uWSGI

1. 说明

   是一个web服务器，实现了WSGI协议、uwsgi协议、http协议等	



## 4 实操

安装：pip install uwsgi

启动：uwsgi --http 0.0.0.0:12346 --chdir /home/liuda/axf --wsgi-file /home/liuda/axf/axf/wsgi.py --master --processes 4 --threads 2 



配置文件 axf.ini

~~~
[uwsgi]
#直接作为web服务器使用
http = 0.0.0.0:12346
#使用nginx连接时 使用
socket = 127.0.0.1:8000
# django项目绝对路径
chdir = /home/liuda/axf/
# 模块路径（项目名称.wsgi）可以理解为wsgi.py的位置
module = axf.wsgi
# 允许主进程
master = true
#最多进程数
processes  = 4
# 退出时候回收pid文件
vacuum = true
#日志大小配置500M
log-maxsize = 500000000
#记录日志配置
logto = uwsgi.log
pidfile = axf.pid
daemonize=uwsgi.log
# 指定静态文件
static-map=/static=/home/liuda/axf/static
#或者pidfile=%(chdir)/uwsgi/uwsgi.pid

~~~

uwsgi相关的命令 是在你装了uwsgi的环境里才能运行的

启动：uwsgi --ini /home/liuda/1807teach/axf/uwsgi.ini

重新加载 uwsgi --reload uwsgi/uwsgi.pid 

终止：uwsgi --stop uwsgi/uwsgi.pid 





NGINX配置1

~~~
server{
    listen 80;
    server_name axf.sharemsg.cn; #此处写你的域名或者ip

    location / {
      include uwsgi_params;
#      proxy_pass http://127.0.0.1:12346; #你Django服务跑的那个端口
     uwsgi_pass 127.0.0.1:8000; #转到的就是你在axf.ini文件里 写的socket对应的IP加端口
     proxy_set_header Host $host;
      #捕获客户端真实IP
      proxy_set_header X-Real-IP $remote_addr;         #$remote_addr 代表客户端IP
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
      proxy_set_header X-Forwarded-Proto $scheme;
      root /home/liuda/axf;
      index index.html;
    }

    location /static{
        alias  /home/liuda/axf/static/; #静态文件的配置 路径就是你Django的static目录的路径
    }

}
~~~

配置2

~~~
upstream axf{
    server 127.0.0.1:12346 weight=2;
	server sharemsg.cn:12346 weight=3;
}
server{
    listen 80;
    server_name axf.sharemsg.cn; #此处写你的域名或者ip

    location / {
      
#      proxy_pass http://127.0.0.1:12346; #axf.ini文件里 http 那个配置写的IP加端口
     proxy_set_header Host $host;
      #捕获客户端真实IP
      proxy_set_header X-Real-IP $remote_addr;         #$remote_addr 代表客户端IP
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
      proxy_set_header X-Forwarded-Proto $scheme;
      root /home/liuda/axf;
      index index.html;
    }

    location /static{
        alias  /home/liuda/axf/static/; #静态文件的配置 路径就是你Django的static目录的路径
    }

}
~~~

~~~


~~~

