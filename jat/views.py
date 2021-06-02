from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from jat.models import Repository, Introduction


class RepositoryListView(generic.ListView):
    model = Repository


class RepositoryDetailView(generic.DetailView):
    model = Repository


class RepositoryCreateView(generic.CreateView):
    model = Repository
    fields = ['name', 'description', 'deadline']    #'__all__'
    template_name_suffix = '_create'
    success_url = reverse_lazy('jat:repository_list')


class IntroductionDetailView(generic.DetailView):
    model = Introduction
