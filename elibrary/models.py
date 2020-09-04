from django.db import models
from custom_user.models import Organization,Account


class Library(models.Model):
    owner = models.OneToOneField(Organization,on_delete=models.CASCADE)


class Book(models.Model):
    library = models.ForeignKey(Library,on_delete=models.CASCADE)
    title = models.CharField(max_length=1024)
    description = models.CharField(max_length=8000,null=True,blank=True)
    type = models.CharField(choices=[('academic', 'academic'), ('non-academic', 'non-academic')], max_length=100)
    edition = models.CharField(max_length=512)
    author = models.CharField(max_length=1024)
    publisher = models.CharField(max_length=1024)
    file = models.FileField(upload_to='books')
    cover = models.ImageField(upload_to='book_cover', default='bookdefault.png')


class BookAnalytics(models.Model):
    book = models.OneToOneField(Book, on_delete=models.CASCADE)
    total_views = models.IntegerField()


class BookAnalyticViewer(models.Model):
    viewer = models.ForeignKey(Account, on_delete=models.CASCADE)
    view_time = models.DateTimeField(auto_now=True)
    book_analytics = models.ForeignKey(BookAnalytics,on_delete=models.CASCADE)


class BookReview(models.Model):     # Max points 10, Min points 0
    book = models.OneToOneField(Book,on_delete=models.CASCADE)
    points = models.FloatField()
    reviews = models.IntegerField()


class Stars(models.Model):
    review = models.ForeignKey(BookReview, on_delete=models.CASCADE)
    stars = models.IntegerField()
    reviewer = models.ForeignKey(Account, on_delete=models.CASCADE)


class TextReviews(models.Model):    # Equivalent to comments
    review = models.ForeignKey(BookReview,on_delete=models.CASCADE)
    text = models.CharField(max_length=5000,null=True,blank=True)
    reviewer = models.ForeignKey(Account,on_delete=models.CASCADE)


