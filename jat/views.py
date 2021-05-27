from django.shortcuts import render
from django.views import generic

from jat.models import Repository


class RepositoryListView(generic.ListView):
    model = Repository
