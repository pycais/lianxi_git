# 一、什么是主从复制?

主从复制，是用来建立一个和主数据库完全一样的数据库环境，称为从数据库；主数据库一般是准实时的业务数据库。

# 二、主从复制的作用（好处，或者说为什么要做主从）重点!

1、做数据的热备，作为后备数据库，主数据库服务器故障后，可切换到从数据库继续工作，避免数据丢失。
2、架构的扩展。业务量越来越大，I/O访问频率过高，单机无法满足，此时做多库的存储，降低磁盘I/O访问的频率，提高单个机器的I/O性能。
3、读写分离，使数据库能支撑更大的并发。

# 三、主从复制的原理（重中之重，面试必问）：

1.数据库有个bin-log二进制文件，记录了所有sql语句。
2.我们的目标就是把主数据库的bin-log文件的sql语句复制过来。
3.让其在从数据的relay-log重做日志文件中再执行一次这些sql语句即可。
4.下面的主从配置就是围绕这个原理配置
5.具体需要三个线程来操作：
1.binlog输出线程:每当有从库连接到主库的时候，主库都会创建一个线程然后发送binlog内容到从库。在从库里，当复制开始的时候，从库就会创建两个线程进行处理：
2.从库I/O线程:当START SLAVE语句在从库开始执行之后，从库创建一个I/O线程，该线程连接到主库并请求主库发送binlog里面的更新记录到从库上。从库I/O线程读取主库的binlog输出线程发送的更新并拷贝这些更新到本地文件，其中包括relay log文件。

3.从库的SQL线程:从库创建一个SQL线程，这个线程读取从库I/O线程写到relay log的更新事件并执行。

可以知道，对于每一个主从复制的连接，都有三个线程。拥有多个从库的主库为每一个连接到主库的从库创建一个binlog输出线程，每一个从库都有它自己的I/O线程和SQL线程。
主从复制如图：

![](./zhucong.png)![zhucong](D:\刘达1\hzpython1807\项目阶段\day02\文档\zhucong.png)





阅读网址：

https://blog.csdn.net/darkangel1228/article/details/80003967

原理介绍：master将改变记录到二进制日志中，slave将日志拷贝到中继日志，slave通过中继日志同步master的操作。

# 实现

环境：master  ip  192.168.1.128

​            slave    ip  192.168.1.129

注意：主从机数据库安装版本最好一致

配置过程

1.master

1）修改配置文件

 vim /etc/mysql/mysql.conf.d/mysqld.cnf

~~~
#[mysqld]
~~~



server-id       = 1   //数字随意设置，只要主从id不重复即可

log-bin  = master-bin    //开启二进制日志

log-bin-index   = master-bin.index

skip-name-resolve   

binlog-do-db    = flask_python   //需要备份的数据库名

binlog-ignore-db= mysql,information_schema   //需要忽略的数据库名

2）重启服务

 sudo  /etc/init.d/mysql restart

3）授权一个实现复制数据的用户

~~~~
mysql> CREATE USER 'dada'@'47.100.251.79' IDENTIFIED BY 'root'; 

mysql> GRANT REPLICATION SLAVE ON . TO 'dada'@'47.100.251.79'; 

mysql> flush privileges; 

~~~~



//此处的IP为从服务器的IP

2.slave

1）修改配置文件

 vim /etc/mysql/mysql.conf.d/mysqld.cnf

[mysqld]

server-id       = 2

relay_log   = slave-relay-bin   //开启中继日志

relay_log_index = slave-relay-bin.index   //一定要保证和master不一致

2）重启服务

 sudo   /etc/init.d/mysql restart

3.master上查看

注意数据master-bin.000024和Position  658  这两个数据

![img](http://upload-images.jianshu.io/upload_images/5750843-acbed2626a0fa976.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/777/format/webp)

4.在slave上同步数据

change master to master_host='47.102.197.236',

master_port=3306,

master_user='root',

master_password='root',

master_log_file='master-bin.000001',

master_log_pos=1020;

![img](http://upload-images.jianshu.io/upload_images/5750843-eea6070c4d257385.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/522/format/webp)

5.开启从服务，并查看从的状态

当Slave_IO_Running: Yes  Slave_SQL_Running: Yes主从数据库即同步

![img](http://upload-images.jianshu.io/upload_images/5750843-1ce6481123ee9871.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/612/format/webp)

 

 

 django 实现读写分离的操作

方案一：在做ORM的时候 使用using来指定使用的数据库

eg：Stu.objects.using("db1").get(id=1)

方案二： 在工程目录下 新建一个py文件 用来说明每个APP 用哪个库 读 写

~~~

class DbRouter(object):

    def db_for_read(self, models, **hints):
        return "db2"

    def db_for_write(self, models, **hints):
        return "db1"

    def allow_relation(self, obj1, obj2, **hints):
        """Allow any relation between apps that use the same database."""
        if obj1._meta.app_label == obj2._meta.app_label:
            return True
        else:
            return False

    # Django 1.7 - Django 1.11
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # if db in DATABASE_MAPPING.values():
        #     return DATABASE_MAPPING.get(app_label) == db
        # elif app_label in DATABASE_MAPPING:
        #     return False
        return True
~~~

在settings.py里加入配置

~~~
DATABASE_ROUTERS = [
    "工程名.文件名db_routers.类名DbRouter"
]
数据库配置
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': "qf_test",
        "HOST": "127.0.0.1",
        "USER": os.environ.get("DBUSER"),
        "PASSWORD": os.environ.get("DBPWD")
    },
    'db1': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': "flask_python",
        "HOST": "47.102.197.236",
        "USER": os.environ.get("DBUSER"),
        "PASSWORD": "123"
    },
    'db2': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': "flask_python",
        "HOST": "47.100.251.79",
        "USER": os.environ.get("DBUSER"),
        "PASSWORD": os.environ.get("DBUSER")
    },

}
~~~



DATE_FORMAT(date,format) 
根据format字符串格式化date值。下列修饰符可以被用在format字符串中： 
%M 月名字(January……December) 
%W 星期名字(Sunday……Saturday) 
%D 有英语前缀的月份的日期(1st, 2nd, 3rd, 等等。） 
%Y 年, 数字, 4 位 
%y 年, 数字, 2 位 
%a 缩写的星期名字(Sun……Sat) 
%d 月份中的天数, 数字(00……31) 
%e 月份中的天数, 数字(0……31) 
%m 月, 数字(01……12) 
%c 月, 数字(1……12) 
%b 缩写的月份名字(Jan……Dec) 
%j 一年中的天数(001……366) 
%H 小时(00……23) 
%k 小时(0……23) 
%h 小时(01……12) 
%I 小时(01……12) 
%l 小时(1……12) 
%i 分钟, 数字(00……59) 
%r 时间,12 小时(hh:mm:ss [AP]M) 
%T 时间,24 小时(hh:mm:ss) 
%S 秒(00……59) 
%s 秒(00……59) 
%p AM或PM 
%w 一个星期中的天数(0=Sunday ……6=Saturday ） 
%U 星期(0……52), 这里星期天是星期的第一天 
%u 星期(0……52), 这里星期一是星期的第一天 
%% 一个文字“%”。