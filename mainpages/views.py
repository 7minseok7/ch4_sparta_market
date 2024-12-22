from django.shortcuts import render

# Create your views here.
def mainpages(request):
    return render(request, 'mainpages/index.html')