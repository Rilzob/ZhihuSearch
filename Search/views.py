import json

from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse

from Search.models import ZhihuAnswerType, ZhihuQuestionType, ZhihuZhuanlanType

# Create your views here.


class SearchSuggest(View):
    def get(self, request):
        key_words = request.GET.get('s', '')
        re_datas = []
        if key_words:
            s = ZhihuAnswerType.search()
            s = s.suggest('my_suggest', key_words, completion={
                "field": "suggest", "fuzzy": {
                    "fuzziness": 2
                },
                "size": 2  # 数据量太小，所以只能设成很小的值，不然都不够返回的并会产生KeyError
            })
            suggestions = s.execute_suggest()
            for match in suggestions.my_suggest[0].options:
                source = match._source
                re_datas.append(source['question_title'])
        return HttpResponse(json.dumps(re_datas), content_type='application/json')
