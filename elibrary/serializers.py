from rest_framework import serializers
from elibrary.models import Book, BookReview, TextReviews


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'description', 'type', 'edition', 'author', 'publisher', 'file', 'cover', ]