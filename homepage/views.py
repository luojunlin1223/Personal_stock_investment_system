from django.shortcuts import render

# Create your views here.
def showhomepage(request):
    return render(request,'homepage/homepage.html')
