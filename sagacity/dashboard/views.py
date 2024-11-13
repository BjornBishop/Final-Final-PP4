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

# Contact Creator 

@login_required
def contact_assignment_creator(request, assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id)
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.from_user = request.user
            contact.to_user = assignment.created_by
            contact.assignment = assignment
            contact.save()

            # Send email notification
            subject = f'New interest in your assignment: {assignment.title}'
            html_message = render_to_string('dashboard/email/contact_notification.html', {
                'from_user': request.user,
                'name': form.cleaned_data['name'],
                'email': form.cleaned_data['email'],
                'assignment': assignment,
                'message': contact.message,
            })
            
            send_mail(
                subject=subject,
                message=strip_tags(html_message),
                html_message=html_message,
                from_email=None,
                recipient_list=[assignment.created_by.email],
            )

            messages.success(request, 'Your message has been sent successfully!')
            return redirect('assignment_detail', pk=assignment_id)
    else:
        # Pre-fill the form with user's information
        initial_data = {
            'name': f"{request.user.first_name} {request.user.last_name}",
            'email': request.user.email
        }
        form = ContactForm(initial=initial_data)

    return render(request, 'dashboard/assignment_detail.html', {
        'form': form,
        'assignment': assignment
    })