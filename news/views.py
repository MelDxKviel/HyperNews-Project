from collections import defaultdict
from datetime import datetime
import random

from django.shortcuts import render, redirect
from django.views import View
import json


class MainPage(View):
    def get(self, request):
        return redirect("/news/")


class PostView(View):

    def get(self, request, post_id):
        with open('hypernews/news.json', 'r') as json_news:
            news_list = json.load(json_news)
            for post in news_list:
                if post["link"] == post_id:
                    return render(request, 'news/post.html', post)


class NewsPage(View):

    def get(self, request):
        search_query = request.GET.get('q', '')

        with open('hypernews/news.json', 'r') as json_news:
            news_list = json.load(json_news)
            news_list_sorted = list()

            if search_query:
                for i in news_list:
                    if search_query in i['title']:
                        news_list_sorted.append(i)
            else:
                news_list_sorted = news_list

            news_per_datetime = {news['created']: news for news in news_list_sorted}
            news_per_datetime_sorted = sorted(news_per_datetime.items(),
                                              key=lambda x: datetime.fromisoformat(x[0]), reverse=True)
            news_per_day_sorted = defaultdict(list)
            [news_per_day_sorted[v['created'].split(" ")[0]].append(v) for k, v in news_per_datetime_sorted]
            context = {"news_per_day": dict(news_per_day_sorted)}

        return render(request, 'news/news.html', context=context)


class NewsCreate(View):

    def get(self, request):
        return render(request, 'news/create.html')

    def post(self, request):
        title = request.POST.get("title")
        text = request.POST.get("text")
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open('hypernews/news.json', 'r') as json_news:
            news_list = json.load(json_news)
            post_ids = []
            for post in news_list:
                post_ids.append(post["link"])

        while True:
            link = random.randint(1, 10000000)
            if link not in post_ids:
                break

        article = dict()
        article["created"] = date
        article["text"] = text
        article["title"] = title
        article["link"] = link

        with open('hypernews/news.json', 'w') as json_news:
            news_list.append(article)
            json.dump(news_list, json_news)

        return redirect("/news/")
