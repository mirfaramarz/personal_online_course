from django.shortcuts import render

def base(request):
    return render(request, 'base/home.html')

def about_us(request):
    return render(request, 'base/pages/about_us.html')

def contact_us(request):
    return render(request, 'base/pages/contact_us.html')