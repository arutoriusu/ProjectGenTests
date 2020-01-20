from django.shortcuts import render, redirect, get_object_or_404
from .forms import TestForm, VariantForm, TaskForm, TagForm, UserRegistrationForm
from .models import Test, Task, Variant
from django.utils import timezone
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


# def index(request):
# 	return render(request, "base/main.html")
# def index(request, username=None):
	
#     tests = Test.objects
#     user = None
#     if username is not None:
#         user = get_object_or_404(User, username=username)
#         tests = tests.filter(user=user)
#     tests = tests.order_by("-added_date")
#     return render(request, "base/main.html", {"tests": tests, "user": user})
def index(request, username=None):
    display_user = ""
    if request.user.is_authenticated:
        display_user = request.user
    tests = Test.objects
    user = None
    if username is not None:
        user = get_object_or_404(User, username=username)
        tests = tests.filter(user=user)
    tests = tests.order_by("-added_date")
    return render(request, "base/main.html", {"tests": tests, "user": user, "display_user": display_user})

def start(request):
	return render(request, "tests/start.html")

def registration(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            user = User.objects.create(user=new_user)
           
            return redirect('/account/login/')
    else:
        user_form = UserRegistrationForm()
    return render(request, 'registration/registration.html', {'user_form': user_form})

@login_required
def test_new(request):
	display_user = ""
	if request.user.is_authenticated:
		display_user = request.user
	if request.method == "POST":
		form = TestForm(request.POST)
		if form.is_valid():
			test = form.save(commit=False)
			test.user = request.user
			test.added_date = timezone.now()
			test.save()
			return redirect('test_detail', pk=test.pk)
	else:
		form = TestForm
	return render(request, "tests/test_new.html", {"form": form})

def test_detail(request, pk):
	test = get_object_or_404(Test, pk=pk)
	tasks = test.variants.get().tasks
	#tasks = Task.objects.filter(variant=Variant.objects.filter(test=test.pk))
	return render(request, 'tests/test_detail.html', {'test': test, 'tasks': tasks})

@login_required
def task_new(request, pk):
	display_user = ""
	if request.user.is_authenticated:
		display_user = request.user
	test = get_object_or_404(Test, pk=pk)
	if request.method == "POST":
		form = TaskForm(request.POST)
		if form.is_valid():
			task = form.save(commit=False)
			task.user = request.user
			task.added_date = timezone.now()
			task.save()
			#return redirect('test_detail', pk=task.pk)
			return render(request, "tasks/task_new.html")
	else:
		form = TaskForm
	return render(request, "tasks/task_new.html", {"form": form})
