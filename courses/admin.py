from django.contrib import admin
from .models import Category, Author, Course, Level

admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Course)
admin.site.register(Level)