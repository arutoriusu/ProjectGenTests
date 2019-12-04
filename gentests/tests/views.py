from django.shortcuts import render

# Create your views here.

def index(request):
	return render(request, "tests/wrapper.html")

def start(request):
	return render(request, "tests/start.html")
