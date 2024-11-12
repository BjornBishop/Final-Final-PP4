# dashboard/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from .forms import SignUpForm, AssignmentForm, PasswordResetRequestForm
from .models import Assignment

# Create your views here

# home request

def home(request):
    # Add a print statement for debugging
    print("Home view is being called")
    active_assignments = Assignment.objects.filter(is_active=True)
    inactive_assignments = Assignment.objects.filter(is_active=False)
    context = {
        'active_assignments': active_assignments,
        'inactive_assignments': inactive_assignments,
        'user': request.user
    }
    print("Context:", context)  # Debug print
    return render(request, 'dashboard/home.html', context)

# sign up

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'dashboard/signup.html', {'form': form})

# Everything below required to be logged in

#assignment details

@login_required
def assignment_detail(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    return render(request, 'dashboard/assignment_detail.html', {'assignment': assignment})

# my assignments

@login_required
def my_assignments(request):
    assignments = Assignment.objects.filter(created_by=request.user)
    return render(request, 'dashboard/my_assignments.html', {'assignments': assignments})

# create assignment 

@login_required
def create_assignment(request):
    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.created_by = request.user
            assignment.save()
            return redirect('my_assignments')
    else:
        form = AssignmentForm()
    return render(request, 'dashboard/create_assignment.html', {'form': form})

# edit assignment 

@login_required
def edit_assignment(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk, created_by=request.user)
    if request.method == 'POST':
        form = AssignmentForm(request.POST, instance=assignment)
        if form.is_valid():
            form.save()
            return redirect('my_assignments')
    else:
        form = AssignmentForm(instance=assignment)
    return render(request, 'dashboard/edit_assignment.html', {'form': form})

# delete assignment 

@login_required
def delete_assignment(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk, created_by=request.user)
    assignment.delete()
    return redirect('my_assignments')

# toggle assignment 

@login_required
def toggle_assignment(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk, created_by=request.user)
    assignment.is_active = not assignment.is_active
    assignment.save()
    return redirect('my_assignments')