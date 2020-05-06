# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect, get_object_or_404
from .forms import TestForm, TaskForm, TagForm, UserRegistrationForm
from .models import Test, Task, Variant
from django.utils import timezone
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.db.models import Q


def index(request, username=None):
    display_user = ""
    if request.user.is_authenticated:
        display_user = request.user
    tests = Test.objects.all()
    for test in tests:
        test.count_of_variants = test.variants.count()
        count_of_tasks = 0
        for variant in test.variants.all():
            count_of_tasks += variant.tasks.count()
        test.count_of_tasks = count_of_tasks
        test.save()
    user = None
    if username is not None:
        user = get_object_or_404(User, username=username)
        tests = tests.filter(user=user)
    tests = tests.order_by("-added_date")
    leftArray, rightArray = split_tests_on_arrays(tests)
    return render(request, "base/main.html", {"leftArray": leftArray, "rightArray": rightArray, "user": user, "display_user": display_user})

def test_list(request):
	tests = Test.objects.all().order_by('-added_date')
	leftArray, rightArray = split_tests_on_arrays(tests)
	return render(request, 'tests/test_list.html', {"leftArray": leftArray, "rightArray": rightArray})

def mytests_list(request):
	tests = Test.objects.filter(user=request.user).order_by("-added_date")
	leftArray, rightArray = split_tests_on_arrays(tests)
	return render(request, 'tests/mytests_list.html', {"leftArray": leftArray, "rightArray": rightArray})

def split_tests_on_arrays(tests):
	leftArray = []
	rightArray = []
	for i in range(0,len(tests)):
		if i % 2 == 0:
			rightArray.append(tests[i])
			continue
		leftArray.append(tests[i])
	return leftArray, rightArray

def start(request):
	return render(request, "tests/start.html")

class SearchResultsView(ListView):
	model = Test
	template_name = "base/search_results.html"

	def get_queryset(self):
		query = self.request.GET.get('q')
		object_list = Test.objects.filter(
			Q(theme_of_test__icontains=query)
		)
		return object_list

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
            # в чем разница между этими двумя способами?
            #user = User.objects.create(username=new_user)
           
            return redirect('/accounts/login/')
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

def tag_new(request, pk):
	return render(request, "tags/tag_new.html")

def test_detail(request, pk):
	test = get_object_or_404(Test, pk=pk)
	variants = test.variants
	return render(request, 'tests/test_detail.html', {'test': test, 'variants': variants})

def test_print(request, pk):
	test = get_object_or_404(Test, pk=pk)
	variants = test.variants
	return render(request, 'tests/test_print.html', {'test': test, 'variants': variants})

@login_required
def task_new(request, pk, pk2):
	test = get_object_or_404(Test, pk=pk)
	if request.user != test.user:
		return redirect('/')
	variant = get_object_or_404(Variant, pk=pk2)
	if request.method == "POST":
		form = TaskForm(request.POST)
		if form.is_valid():
			task = form.save(commit=False)
			task.user = request.user
			task.added_date = timezone.now()
			task.variant = variant
			task.save()
			return redirect('variant_detail', pk=test.pk, pk2=variant.pk)
	else:
		form = TaskForm
	return render(request, "tasks/task_new.html", {"form": form})

def task_list(request, category):
	tasks = Task.objects.filter(category=category).order_by("-added_date")
	print(tasks)
	return render(request, "tasks/task_list.html", {"tasks": tasks})

@login_required
def variant_new(request, pk):
	test = get_object_or_404(Test, pk=pk)
	if request.user != test.user:
		return redirect('/')
	variant = Variant(test=test)
	variant.number_of_variant = str(test.variants.count()+1)
	variant.save()
	tasks = variant.tasks
	return render(request, 'variants/variant_detail.html', {'test': test, 'variant': variant, 'tasks': tasks})

def variant_detail(request, pk, pk2):
	test = get_object_or_404(Test, pk=pk)
	variant = get_object_or_404(Variant, pk=pk2)
	tasks = variant.tasks
	return render(request, 'variants/variant_detail.html', {'test': test, 'variant': variant, 'tasks': tasks})

def variant_print(request, pk, pk2):
	test = get_object_or_404(Test, pk=pk)
	variant = get_object_or_404(Variant, pk=pk2)
	tasks = variant.tasks
	return render(request, 'variants/variant_print.html', {'test': test, 'variant': variant, 'tasks': tasks})

@login_required
def variant_delete(request, pk, pk2):
	test = get_object_or_404(Test, pk=pk)
	if request.user != test.user:
		return redirect('/')
	variant = get_object_or_404(Variant, pk=pk2)
	variant.delete()
	variants = test.variants
	return render(request, 'tests/test_detail.html', {'test': test, 'variants': variants})

@login_required
def test_delete(request, pk):
	test = get_object_or_404(Test, pk=pk)
	if request.user != test.user:
		return redirect('/')
	test.delete()
	return redirect('/test/list/')

@login_required
def test_edit(request, pk):
    test = get_object_or_404(Test, pk=pk)
    if request.user != test.user:
        return redirect('/')
    variants = test.variants
    if request.method == "POST":
        form = TestForm(request.POST, instance=test) # why instance
        if form.is_valid():
            test = form.save(commit=False)
            test.user = request.user
            test.date = timezone.now()
            test.save()
            return render(request, 'tests/test_detail.html', {'test': test, 'variants': variants})
    else:
        form = TestForm(instance=test)
    return render(request, 'tests/test_new.html', {'form': form})

@login_required
def task_delete(request, pk, pk2, pk3):
	task = get_object_or_404(Task, pk=pk3)
	if request.user != task.user:
		return redirect('/')
	task.delete()
	return variant_detail(request, pk, pk2)

@login_required
def task_edit(request, pk, pk2, pk3):
    test = get_object_or_404(Test, pk=pk)
    variant = get_object_or_404(Variant, pk=pk2)
    task = get_object_or_404(Task, pk=pk3)
    if request.user != task.user:
        return redirect('/')
    tasks = variant.tasks
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task) # why instance
        if form.is_valid():
            task = form.save(commit=False)
            task.date = timezone.now()
            task.save()
            return render(request, 'variants/variant_detail.html', {'test': test, 'variant': variant, 'tasks': tasks})
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_new.html', {'form': form})
