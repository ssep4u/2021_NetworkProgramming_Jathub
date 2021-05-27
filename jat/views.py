from django.shortcuts import render
from django.views import generic

from jat.models import Repository, Introduction


class RepositoryListView(generic.ListView):
    model = Repository


class RepositoryDetailView(generic.DetailView):
    model = Repository


class IntroductionDetailView(generic.DetailView):
    model = Introduction
