from elasticsearch_dsl import Date, analyzer, Keyword, Text, Document
from elasticsearch_dsl.connections import connections                 # 导入连接elasticsearch(搜索引擎)服务器方法

connections.create_connection(hosts=['127.0.0.1'])
# 分词器
ik_analyzer = analyzer('ik_max_word')


class cnblogsType(Document):                               # 自定义一个类来继承DocType类
    # Text类型需要分词，所以需要知道中文分词器，ik_max_word为中文分词器
    title = Text(analyzer="ik_max_word")                   # 设置，字段名称=字段类型，Text为字符串类型并且可以分词建立倒排索引
    description = Text(analyzer="ik_max_word")
    url = Keyword()                                        # Keyword为普通字符串类型，不分词
    riqi = Date()                                          # Date日期类型

    class Index:
        name = 'cnblogs'
        settings = {
            "number_of_shards": 5,
        }


# 创建连接
es = connections.create_connection(cnblogsType)

if __name__ == "__main__":      # 判断在本代码文件执行才执行里面的方法，其他页面调用的则不执行里面的方法
    cnblogsType.init()
