from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView, 
    CreateView,  
    UpdateView, 
    DeleteView, 
    FormView
)
from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse
from .models import Board, Task, Comment
from django.contrib.auth.models import User
from .forms import BoardForm, TaskForm, CommentForm
from datetime import datetime, timedelta
from django.conf import settings
from django.utils.timezone import make_aware


def landing(request):
    return render(request, 'projects/landing.html', {'title': 'Kanri | Welcome'})

def dashboard(request):

    naive_datetime = datetime.now()
    aware_datetime = make_aware(naive_datetime)

    last_month = aware_datetime - timedelta(days=30)
    
    task_counts = {}
    task_statuses = [task.status for task in Task.objects.filter(author=request.user, date_posted__gte=last_month)]
    for task in task_statuses:
        if task in task_counts:
            task_counts[task] += 1
        if task not in task_counts:
            task_counts[task] = 1
    
    
    assigned_task_counts = {}
    assigned_task_statuses = [task.status for task in Task.objects.filter(assigned_to=request.user, date_posted__gte=last_month)]
    for task in assigned_task_statuses:
        if task in assigned_task_counts:
            assigned_task_counts[task] += 1
        if task not in assigned_task_counts:
            assigned_task_counts[task] = 1


    context = {
        'tasks': Task.objects.filter(author=request.user),
        'users': [user.username for user in User.objects.all()],
        'task_counts': task_counts,
        'assigned_task_counts': assigned_task_counts
    }

    
    return render(request, 'projects/dashboard.html', context)


def boards(request):
    return render(request, 'projects/boards.html', {'title': 'Kanri | Welcome'})


class BoardListView(LoginRequiredMixin, ListView):
    model = Board
    template_name = 'projects/boards.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_boards'] = Board.objects.filter(status='ACTIVE')
        context['inactive_boards'] = Board.objects.filter(status='INACTIVE')
        context['closed_boards'] = Board.objects.filter(status='CLOSED')
        context['form'] = BoardForm()
        return context

class BoardCreateView(LoginRequiredMixin, CreateView):
    model = Board
    form_class = BoardForm
    template_name = 'projects/board_form.html'

    def form_valid(self, form):
        issue = form.save(commit=False)
        form.instance.author = self.request.user
        if form.instance.author.email == "kanridemo@kanri.com":
            messages.warning(self.request, f'Issue not saved. You are using a demo account. Demo accounts do not have write permissions. Create an account to enjoy full app functionality.')
            return redirect('boards')
        issue.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('boards')

class AllBoardsView(View):
    def get(self, request, *args, **kwargs):
        view = BoardListView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = BoardCreateView.as_view()
        return view(request, *args, **kwargs)

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'projects/tasks.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        board_id = self.kwargs['board_id']
        context['board_id'] = board_id
        context['board_name'] = Board.objects.get(id=board_id)
        context['todo_tasks'] = Task.objects.filter(status='TODO')
        context['in_progress_tasks'] = Task.objects.filter(status='IN PROGRESS')
        context['closed_tasks'] = Task.objects.filter(status='CLOSED')
        context['form'] = TaskForm()
        return context

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'projects/task_form.html'

    def form_valid(self, form):
        task = form.save(commit=False)
        task.board_id = self.kwargs['board_id']
        form.instance.author = self.request.user
        if form.instance.author.email == "kanridemo@kanri.com":
            messages.warning(self.request, f'Issue not saved. You are using a demo account. Demo accounts do not have write permissions. Create an account to enjoy full app functionality.')
            return redirect(reverse('board-detail', kwargs={'board_id': self.kwargs['board_id']}))
        task.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('board-detail', kwargs={'board_id': self.kwargs['board_id']})
        # return reverse('boards')


class BoardDetailView(View):
    def get(self, request, *args, **kwargs):
        view = TaskListView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = TaskCreateView.as_view()
        return view(request, *args, **kwargs)

class CommentCreateView(SingleObjectMixin, FormView):
    model = Task
    form_class = CommentForm
    template_name = 'task_detail.html'


    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(CommentCreateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
    
    def form_valid(self, form):
        comment = form.save(commit=False)
        form.instance.author = self.request.user
        if not form.instance.author.email == "kanridemo@kanri.com":
            comment.task = self.object
            comment.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('board-detail', kwargs={'board_id': self.kwargs['board_id']})
        # return reverse('issues-home')

class TaskDisplayView(DetailView):
    model = Task
    context_object_name = 'task'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        board_id = self.kwargs['board_id']
        context['board_id'] = board_id
        context['form'] = CommentForm()
        return context

class TaskDetailView(View):

    def get(self, request, *args, **kwargs):
        view = TaskDisplayView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = CommentCreateView.as_view()
        return view(request, *args, **kwargs)

class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    form_class= TaskForm
    template_name = 'projects/task_form.html'


    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, f'Update saved.')
        return super().form_valid(form)


    def test_func(self):
        task = self.get_object() 
        if self.request.user == task.author:
            return True
        return False
    
    def get_success_url(self):
        return reverse('board-detail', kwargs={'board_id': self.kwargs['board_id']})

class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['board_id'] = self.kwargs['board_id']
        print(context)

    def test_func(self):
        task = self.get_object() 
        if self.request.user == task.author:
            return True
        return False

    def get_success_url(self):
        return reverse('board-detail', kwargs={'board_id': self.kwargs['board_id']})