from django.db import models

class Category(models.Model):
    icon = models.CharField(max_length=200, null=True)
    name = models.CharField(max_length=200)
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name
class Author(models.Model):
    author_profile = models.ImageField(upload_to="course_author/")
    name = models.CharField(max_length=100, null=True)
    expertise = models.CharField(max_length=200)
    about_author = models.TextField()

    def __str__(self) -> str:
        return self.name
class Course(models.Model):
    STATUS = (
        ('PUBLISH','PUBLISH'),
        ('DRAFT', 'DRAFT'),
    )
    featured_image = models.ImageField(upload_to="featured_img/",null=True)
    featured_video = models.CharField(max_length=300,null=True)
    title = models.CharField(max_length=500)
    created_at = models.DateField(auto_now_add=True)
    author = models.ForeignKey(Author,on_delete=models.CASCADE,null=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    #level = models.ForeignKey(Level, on_delete=models.CASCADE, null=True)
    description = models.TextField()
    price = models.IntegerField(null=True,default=0)
    discount = models.IntegerField(null=True, blank=True)
    slug = models.SlugField(default='', max_length=500, null=True, blank=True)
    status = models.CharField(choices=STATUS,max_length=100,null=True)
    course_language =  models.CharField(max_length=100)
    deadline = models.DateField(null=True, blank=True)
    certificate = models.CharField(null=True, max_length=5)

    def __str__(self):
        return self.title
    
    # def get_absolute_url(self):
    #     from django.urls import reverse
    #     return reverse("course_details", kwargs={'slug': self.slug})