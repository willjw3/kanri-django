from django.shortcuts import render, HttpResponse


def landing(request):
    return render(request, 'projects/landing.html', {'title': 'Kanri | Welcome'})
