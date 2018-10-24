from django.db import models

# Create your models here.
# encoding:utf-8

# @Author: Rilzob
# @Time: 2018/10/16 下午8:59

from elasticsearch_dsl import DocType, Text, Keyword, Integer, Completion
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl.analysis import CustomAnalyzer as _CustomAnalyzer
connections.create_connection(hosts=["localhost"])


class CustomAnalyzer(_CustomAnalyzer):
    def get_analysis_definition(self):
        return {}


ik_analyzer = CustomAnalyzer("ik_max_word", filter=['lowercase'])


class ZhihuQuestionType(DocType):
    # 知乎问题类型
    suggest = Completion(analyzer=ik_analyzer)
    question_id = Integer()
    question_url = Keyword()
    question_title = Text(analyzer="ik_max_word")
    question_descr = Text(analyzer="ik_max_word")
    answer_num = Integer()
    followers = Integer()
    visitors = Integer()
    topics = Text(analyzer="ik_max_word")

    class Meta:
        index = "zhihu"
        doc_type = "question"


class ZhihuAnswerType(DocType):
    # 知乎回答类型
    suggest = Completion(analyzer=ik_analyzer)
    answer_id = Keyword()
    comments_num = Integer()
    praise_num = Integer()
    answer_article = Text(analyzer="ik_max_word")

    class Meta:
        index = "zhihu"
        doc_type = "answer"


class ZhihuZhuanlanType(DocType):
    # 知乎专栏类型
    suggest = Completion(analyzer=ik_analyzer)
    zhuanlan_id = Keyword()
    zhuanlan_title = Text()
    praise_num = Integer()
    zhuanlan_url = Keyword()
    zhuanlan_article = Text(analyzer="ik_max_word")
    comments_num = Integer()

    class Meta:
        index = "zhihu"
        doc_type = "zhuanlan"


if __name__ == '__main__':
    ZhihuQuestionType.init()
    ZhihuAnswerType.init()
    ZhihuZhuanlanType.init()
