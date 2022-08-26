from django.shortcuts import render
from elasticsearch import Elasticsearch
from pprint import pprint
from datetime import datetime

client = Elasticsearch('127.0.0.1', port='9200')


# Create your views here.
def index(request):
    return render(request, 'index.html')


def search(request):
    key_words = request.GET.get('q', '')
    page_size = 10
    page = request.GET.get('p', '1')  # 获取访问页码
    try:
        page = int(page)
    except:
        page = 1

    start_time = datetime.now()
    response = client.search(  # 原生的elasticsearch接口的search()方法，就是搜索，可以支持原生elasticsearch语句查询
        index="cnblogs",  # 设置索引名称
        doc_type="doc",  # 设置表名称
        body={  # 书写elasticsearch语句
            "query": {
                "multi_match": {  # multi_match查询
                    "query": key_words,  # 查询关键词
                    "fields": ["title", "description"]  # 查询字段
                }
            },
            "from": (page-1)*page_size,  # 从第几条开始获取
            "size": page_size,  # 获取多少条数据
            "highlight": {  # 查询关键词高亮处理
                "pre_tags": ['<span class="keyWord">'],  # 高亮开始标签
                "post_tags": ['</span>'],  # 高亮结束标签
                "fields": {  # 高亮设置
                    "title": {},  # 高亮字段
                    "description": {}  # 高亮字段
                }
            }
        }
    )
    end_time = datetime.now()
    search_time = (end_time - start_time).total_seconds()
    total = response["hits"]["total"]
    if (page % page_size) > 0:  # 计算页数
        page_num = int(total / page_size) + 1
    else:
        page_num = int(total / page_size)

    response_hits = response["hits"]["hits"]
    hit_list = []
    for hit in response_hits:
        hit_dict = {}
        if "title" in hit["highlight"]:
            hit_dict["title"] = "".join(hit["highlight"]["title"])
        else:
            hit_dict["title"] = hit["_source"]["title"]

        if "description" in hit["highlight"]:
            hit_dict["description"] = "".join(hit["highlight"]["description"])[:500]
        else:
            hit_dict["description"] = hit["_source"]["description"]

        hit_dict["url"] = hit["_source"]["url"]                         # 获取返回url
        hit_dict["create_date"] = hit["_source"]["riqi"]
        hit_dict["score"] = hit["_score"]
        hit_dict["source_site"] = "博客园"
        hit_list.append(hit_dict)

    # return_dict =
    return render(request, 'result.html', {
        "page": page,
        'page_num': page_num,
        "total": total,
        "all_hits": hit_list,
        "key_words": key_words,
        "search_time": search_time
    })
