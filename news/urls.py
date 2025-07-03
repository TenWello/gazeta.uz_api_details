from django.urls import path
from .views import GazetaNewsBatchDetailApi

urlpatterns = [
    path('gazeta-news-detail-batch/', GazetaNewsBatchDetailApi.as_view()),
]
