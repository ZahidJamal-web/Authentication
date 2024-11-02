from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .tokens import generate_token, send_verification_email
from django.http import HttpResponse  # Import for testing

def home(request):
    return render(request, 'authentication/index.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password = request.POST['password']
        c_password = request.POST['c_password']

        if password != c_password:
            messages.error(request, "Passwords do not match")
            return redirect("home")

        # Check for existing user
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect("home")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already in use.")
            return redirect("home")

        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.first_name = fname
            user.last_name = lname
            user.save()

            token = generate_token()
            send_verification_email(user.email, user.first_name, token)
            messages.success(request, 'Signup successful! An email has been sent to you.')
            return redirect('signin')
        except Exception as e:
            messages.error(request, f'Error creating user or sending email: {str(e)}')
            return redirect("home")

    return render(request, 'authentication/signup.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('home')

    return render(request, 'authentication/signin.html')

def signout(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('home')

def confirm_email(request, token):
    # Here you would verify the token (you'll need to implement this logic)
    # For now, just simulate a successful confirmation.
    messages.success(request, "Email confirmed successfully!")
    return redirect('home')

# Test sending email
def test_send_email(request):
    try:
        send_verification_email('zahidjamal2005@gmail.com', 'Zahid Jamal', 'ZhifAjkl123')  # Change recipient
        return HttpResponse("Test email sent!")
    except Exception as e:
        return HttpResponse(f"Error sending email: {str(e)}")
