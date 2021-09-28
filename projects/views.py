from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse

from django.contrib.auth.models import User

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