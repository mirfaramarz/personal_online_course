from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import Category, Level, Course



def single_course(request):
    category = Category.objects.all().order_by('id')
    level = Level.objects.all()
    course = Course.objects.all()
    freeCourse = Course.objects.filter(price=0).count()
    paidCourse = Course.objects.filter(price__gte=1).count()
    context = {
        'category':category,
        'level':level,
        'course':course,
        'freeCourse':freeCourse,
        'paidCourse':paidCourse,
    }
    return render(request, 'courses/course_list.html', context)


"""This view is for filtering the courses on the course view based on the 
price , category ... . i created a ajax template for that in the ajax folder and script on the course_list 
template on the top is part of this code"""
def filter_data(request):
    # Extract selected filters, removing empty strings
    category = [cat for cat in request.GET.getlist('category[]') if cat]
    level = [lvl for lvl in request.GET.getlist('level[]') if lvl]
    price = [pr for pr in request.GET.getlist('price[]') if pr]

    course = Course.objects.all()

    if price:
        if 'pricefree' in price:
            course = course.filter(price=0)
        elif 'pricepaid' in price:
            course = course.filter(price__gte=1)
    if category:
        course = course.filter(category__id__in=category)
    if level:
        course = course.filter(level__id__in=level)
    
    course = course.order_by('-id')
    
    t = render_to_string('ajax/course_filter_data.html', {'course': course})
    return JsonResponse({'data': t})

def course_details(request, slug):
    context = {

    }
    return render(request, 'courses/course_details.html', context)
