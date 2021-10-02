from django.urls import path, include

from .views import *

urlpatterns = [
    path('<int:post_id>/', PostView.as_view()),
    path('', NewsPage.as_view(), name="news_page"),
    path('create/', NewsCreate.as_view()),
]
