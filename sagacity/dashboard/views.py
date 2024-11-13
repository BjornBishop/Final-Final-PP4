# dashboard/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from .forms import SignUpForm, AssignmentForm, PasswordResetRequestForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import Assignment, ContactMessage

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
        # Create contact message directly from POST data
        contact = ContactMessage(
            from_user=request.user,
            to_user=assignment.created_by,
            assignment=assignment,
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            message=request.POST.get('message')
        )
        contact.save()

        # Send email notification
        subject = f'New interest in your assignment: {assignment.title}'
        html_message = render_to_string('dashboard/email/contact_notification.html', {
            'name': contact.name,
            'email': contact.email,
            'assignment': assignment,
            'message': contact.message,
        })
        
        try:
            send_mail(
                subject=subject,
                message=strip_tags(html_message),
                html_message=html_message,
                from_email=None,
                recipient_list=[assignment.created_by.email],
            )
            messages.success(request, 'Your message has been sent successfully!')
        except Exception as e:
            messages.error(request, 'There was an error sending your message. Please try again.')
            print(f"Email error: {e}")  # For debugging

        return redirect('assignment_detail', pk=assignment_id)

    # If not POST, redirect back to assignment detail
    return redirect('assignment_detail', pk=assignment_id)

@login_required
def assignment_detail(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    return render(request, 'dashboard/assignment_detail.html', {
        'assignment': assignment
    })