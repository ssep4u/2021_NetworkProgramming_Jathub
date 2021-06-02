from django.urls import path

from jat import views

app_name = 'jat'

urlpatterns = [
    path('', views.RepositoryListView.as_view(), name='repository_list'),    #jat:repository_list
    path('repository/<int:pk>/', views.RepositoryDetailView.as_view(), name='repository_detail'),    #jat:repository_detail
    path('repository/<int:repository_pk>/introduction/<int:pk>/', views.IntroductionDetailView.as_view(), name='introduction_detail'),    #jat:introduction_detail
]