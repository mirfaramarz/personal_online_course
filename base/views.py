from django.shortcuts import render
from courses.models import Category, Course

def base(request):
    category = Category.objects.all().order_by('id')[0:5]
    course = Course.objects.filter(status='PUBLISH').order_by('-id')
    context = {
        'category':category,
        'course':course,
    }
    return render(request, 'base/home.html', context)

def about_us(request):
    return render(request, 'base/pages/about_us.html')

def contact_us(request):
    return render(request, 'base/pages/contact_us.html')