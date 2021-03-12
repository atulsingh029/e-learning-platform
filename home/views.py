from django.shortcuts import render, redirect


def home(request):
    if request.user.is_authenticated:
        return redirect('/dashboard')
    return render(request, 'home/home.html')

# Version2.0
def home_2(request):
    if request.user.is_authenticated:
        return redirect('/dashboard')
    return render(request, 'version2.0/home/landingpage.html')