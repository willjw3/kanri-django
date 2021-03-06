from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Board(models.Model):
    STATUSES = [('ACTIVE', "active"), ('INACTIVE', "inactive"), ('CLOSED', "closed")]

    name = models.CharField(max_length=100)
    about = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUSES, default='ACTIVE')
    created_on = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['created_on']
    
    def __str__(self):
        return self.name

class Task(models.Model):
    STATUSES = [('TODO', "todo"), ('IN PROGRESS', "in progress"), ('CLOSED', "closed")]
    
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='tasks', default=1)
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default='admin')
    assigned_to = models.CharField(max_length=50, default='admin')
    status = models.CharField(max_length=20, choices=STATUSES, default='OPEN')
    label = models.CharField(max_length=30, default='')
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


    def get_absolute_url(self):
        print(self.kwargs)
        return reverse('board-detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments', default='Test Task - Ignore')
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    content = models.TextField()
    posted_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-posted_on']

    def __str__(self):
        return self.content
    
    def get_absolute_url(self):
        return reverse('issues-home')