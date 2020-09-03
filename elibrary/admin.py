from django.contrib import admin
from .models import *


admin.site.register(Library)
admin.site.register(Book)
admin.site.register(BookReview)
admin.site.register(BookAnalytics)
admin.site.register(BookAnalyticViewer)
admin.site.register(TextReviews)
