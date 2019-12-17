from django.shortcuts import render
from .forms import ProfileForm, TestForm, VariantForm, TaskForm, TagForm

# Create your views here.

def index(request):
	return render(request, "tests/wrapper.html")

def start(request):
	return render(request, "tests/start.html")

def test_new(request):
	form = TestForm
	return render(request, "tests/test_new.html", {"form": form})
