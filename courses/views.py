from django.shortcuts import render

def single_course(request):
    return render(request, 'courses/course_list.html')