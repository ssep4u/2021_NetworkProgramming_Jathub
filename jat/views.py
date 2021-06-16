from django.db.models import Max
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic

from jat.forms import IntroductionForm
from jat.models import Repository, Introduction, Comment


class RepositoryListView(generic.ListView):
    model = Repository


class RepositoryDetailView(generic.DetailView):
    model = Repository


class RepositoryCreateView(generic.CreateView):
    model = Repository
    fields = ['name', 'description', 'deadline']  # '__all__'
    template_name_suffix = '_create'
    success_url = reverse_lazy('jat:repository_list')


class RepositoryUpdateView(generic.UpdateView):
    model = Repository
    fields = ['name', 'description', 'deadline']  # '__all__'
    template_name_suffix = '_update'
    success_url = reverse_lazy('jat:repository_list')


class RepositoryDeleteView(generic.DeleteView):
    model = Repository
    success_url = reverse_lazy('jat:repository_list')


class IntroductionDetailView(generic.DetailView):
    model = Introduction


class IntroductionCreateView(generic.CreateView):
    model = Introduction
    fields = ['repository', 'version', 'contents', 'access']  # '__all__'
    template_name_suffix = '_create'

    # success_url = reverse_lazy('jat:repository_detail') #repository_detail은 pk가 필요함(ImproperlyConfigured at /repository/3/introduction/add/)
    def get_initial(self):
        repository = get_object_or_404(Repository, pk=self.kwargs['repository_pk'])
        introduction = repository.introduction_set.aggregate(
            Max('version'))  # 해당 repository의 introduction 중 version 최대값 구하자
        version = introduction['version__max']
        if version == None:  # introduction이 아예 없으면 version 기본값: 1
            version = 1
        else:  # introduction이 있으면 version 최대값에서 +1
            version += 1
        return {'repository': repository, 'version': version}

    def get_success_url(self):
        return reverse_lazy('jat:repository_detail', kwargs={'pk': self.kwargs['repository_pk']})


def add_introduction(request, repository_pk):  # return render(request, '템플릿 이름', 그템플릿에 넘겨주는 context)
    if request.method == 'POST':    #POST라면
        form = IntroductionForm(request.POST)   #  introduction 만드는 form에서 입력한 정보 가져오자
        if form.is_valid(): #  그 정보가 확인되면
            form.save()     #    DB에 저장
            return redirect('jat:repository_detail', pk=repository_pk)   #    repository_detail로 redirect
    else:   #POST가 아니면(요청한 것: introduction 만들기위한 form 보여주기)
        repository = get_object_or_404(Repository, pk=repository_pk)    #  repository를 DB에서 꺼내자
        introduction = repository.introduction_set.order_by('-version').first()
        #  version을 구하자
        #  contents(introduction 내용) 가져오자
        if introduction == None:
            version = 1     #    introduction이 없으면 version = 1
            contents = ''   #    introduction이 없으면 ''
            access = 1
        else:
            version = introduction.version + 1  #    repository에 있는 introduction 중 가장 큰 버전 + 1
            contents = introduction.contents    #    introduction 중 가장 큰 버전의 contents를 가져오자
            access = introduction.access
        initial = {'repository': repository, 'version': version, 'contents': contents, 'access': access}
        form = IntroductionForm(initial=initial)   #  form 가져오자
        context = {'form': form, 'repository': repository}    #  context = form, repository

    return render(request, 'jat/introduction_create.html', context)



class IntroductionUpdateView(generic.UpdateView):
    model = Introduction
    fields = ['repository', 'version', 'contents', 'access']  # '__all__'
    template_name_suffix = '_update'

    def get_success_url(self):
        return reverse_lazy('jat:repository_detail', kwargs={'pk': self.kwargs['repository_pk']})


class IntroductionDeleteView(generic.DeleteView):
    model = Introduction

    def get_success_url(self):
        return reverse_lazy('jat:repository_detail', kwargs={'pk': self.kwargs['repository_pk']})


class CommentCreateView(generic.CreateView):  # repository/<int:repository_pk>/introduction/<int:introduction_pk>/comment/add/
    model = Comment
    fields = '__all__'  # ['introduction', 'comment']
    template_name_suffix = '_create'  # comment_create.html

    def get_initial(self):
        introduction = get_object_or_404(Introduction, pk=self.kwargs['introduction_pk'])
        return {'introduction': introduction}

    def get_success_url(self):  # jat:introduction_detail repository_pk pk
        kwargs = {
            'repository_pk': self.kwargs['repository_pk'],
            'pk': self.kwargs['introduction_pk'],
        }
        return reverse_lazy('jat:introduction_detail', kwargs=kwargs)   #repository/<int:repository_pk>/introduction/<int:pk>/


class CommentUpdateView(generic.UpdateView):
    model = Comment
    fields = '__all__'  # ['introduction', 'comment']
    template_name_suffix = '_update'  # comment_update.html

    def get_success_url(self):  # jat:introduction_detail repository_pk pk
        kwargs = {
            'repository_pk': self.kwargs['repository_pk'],
            'pk': self.kwargs['introduction_pk'],
        }
        return reverse_lazy('jat:introduction_detail', kwargs=kwargs)  # repository/<int:repository_pk>/introduction/<int:pk>/


class CommentDeleteView(generic.DeleteView):
    model = Comment

    def get_success_url(self):  # jat:introduction_detail repository_pk pk
        kwargs = {
            'repository_pk': self.kwargs['repository_pk'],
            'pk': self.kwargs['introduction_pk'],
        }
        return reverse_lazy('jat:introduction_detail', kwargs=kwargs)  # repository/<int:repository_pk>/introduction/<int:pk>/

