from django.shortcuts import render, HttpResponse
from custom_user.models import Account
from rest_framework.response import Response
from .models import Book
from .serializers import BookSerializer
from rest_framework.decorators import api_view
from .forms import AddBook
from django.shortcuts import redirect


def add_book(request):
    if request.method == "POST":
        account = Account.objects.get(username=request.user)
        if account.is_teacher:
            library = account.teacher.from_organization.library
        else:
            library = account.organization.library
        data = request.POST
        title = data.get('title')
        description = data.get('description')
        type = data.get('type')
        author = data.get('author')
        edition = data.get('edition')
        publisher = data.get('publisher')
        files = request.FILES
        cover = files.get('cover_pic')
        file = files.get('file')
        book = Book(title=title, description=description, type=type, author=author, edition=edition, publisher=publisher, cover=cover, file=file, library=library)
        book.save()
        return redirect("/dashboard/?javascript:loadLibraryDashboard()")
    else:
        form = AddBook()
        context = {'form' : form, 'forname':'ADD BOOK'}
        return render(request, 'custom_user/forms.html', context=context)


@api_view(['GET'])
def showcase(request):
    if request.user.is_authenticated:
        username = request.user
        account = Account.objects.filter(username=username)
        if account[0].is_organization:
            library = account[0].organization.library
        elif account[0].is_teacher:
            library = account[0].teacher.from_organization.library
        else:
            library = account[0].student.from_organization.library
        books = Book.objects.filter(library=library)
        serial_data = BookSerializer(books, many=True)
        return Response(serial_data.data)


@api_view(['GET'])
def delete_book(request, id):
    if request.user.is_authenticated:
        username = request.user
        account = Account.objects.filter(username=username)
        book = Book.objects.filter(id=id)
        if account[0].is_teacher:
            tester = account[0].teacher.from_organization
        else:
            tester = account[0].organization


        if book[0].library.owner == tester:
            book[0].delete()
            return Response("success")
        else:
            return Response("invalid request")
    else:
        return Response("auth error : login")


def edit_book(request):
    pass