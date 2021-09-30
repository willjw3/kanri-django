from django.shortcuts import render, redirect
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
from .forms import BoardForm, TaskForm
from datetime import datetime, timedelta
from django.conf import settings
from django.utils.timezone import make_aware


def landing(request):
    return render(request, 'projects/landing.html', {'title': 'Kanri | Welcome'})

def dashboard(request):

    naive_datetime = datetime.now()
    aware_datetime = make_aware(naive_datetime)

    last_month = aware_datetime - timedelta(days=30)
    
    # issue_counts = {}
    # issue_statuses = [issue.status for issue in Issue.objects.filter(author=request.user, date_posted__gte=last_month)]
    # for issue in issue_statuses:
    #     if issue in issue_counts:
    #         issue_counts[issue] += 1
    #     if issue not in issue_counts:
    #         issue_counts[issue] = 1
    

    # assigned_issue_counts = {}
    # assigned_issue_statuses = [issue.status for issue in Issue.objects.filter(assigned_to=request.user, date_posted__gte=last_month)]
    # for issue in assigned_issue_statuses:
    #     if issue in assigned_issue_counts:
    #         assigned_issue_counts[issue] += 1
    #     if issue not in assigned_issue_counts:
    #         assigned_issue_counts[issue] = 1


    # context = {
    #     'issues': Issue.objects.filter(author=request.user),
    #     'users': [user.username for user in User.objects.all()],
    #     'issue_counts': issue_counts,
    #     'assigned_issue_counts': assigned_issue_counts
    # }
    
    return render(request, 'projects/dashboard.html')


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
        context['todo_tasks'] = Board.objects.filter(status='TODO')
        context['in_progress_boards'] = Board.objects.filter(status='IN PROGRESS')
        context['closed_boards'] = Board.objects.filter(status='CLOSED')
        context['form'] = TaskForm()
        return context

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'projects/task_form.html'

    def form_valid(self, form):
        issue = form.save(commit=False)
        form.instance.author = self.request.user
        if form.instance.author.email == "kanridemo@kanri.com":
            messages.warning(self.request, f'Issue not saved. You are using a demo account. Demo accounts do not have write permissions. Create an account to enjoy full app functionality.')
            return redirect('tasks')
        issue.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('tasks')

class AllTasksView(View):
    def get(self, request, *args, **kwargs):
        view = BoardListView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = BoardCreateView.as_view()
        return view(request, *args, **kwargs)