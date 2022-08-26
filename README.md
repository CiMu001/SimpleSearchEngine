s
### 简介
<未命名搜索引擎>是一款基于ElasticSearc实现的搜索引擎。


### 功能
+ 检索使用elasticsearch
  + 倒排索引
  + 关键词高亮
+ 页面分页显示



### 主要技术栈
+ Scrapy
+ ElasticSearch    6.8.0
+ elasticsearch-dsl    6.4.0
+ Django


### 环境安装
+ elasticsearch-6.4.3<br>启动地址 http://127.0.0.1:9200/

+ elasticsearch-head ( 用于方便查看数据信息 )<br>启动地址 http://localhost:9100/
+ kibana-6.4.3 ( 用于方便对数据信息操作 )
+ 以上的安装版本要相符合

### 使用说明

1. 爬取数据

   ```shell
   启动elasticsearch
   
   # 初始化es数据库
   进入spider_to_es/cnblog/cnblog/es_orm.py 执行cnblogsType.init()
   
   运行spider_to_es/cnblog/main 执行爬虫
   ```

2. 运行django

   ```shell
   cd ./django_search_engine
   
   # 运行
   python manage.py runserver
   ```
   
