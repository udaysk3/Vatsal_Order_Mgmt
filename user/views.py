from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import User
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password

def signin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        # Check if the user exists
        if not User.objects.filter(email=email).exists():
            messages.error(request,"User doesn't exist.")
            return render(request, 'user/login.html', {'message': "User doesn't exist. Please sign up"})
        
        user = User.objects.get(email=email)
        
        authenticated_user = authenticate(email=email, password=password)
        if authenticated_user is not None:
                # Check the password using check_password
                if check_password(password, authenticated_user.password):
                    request.session['email'] = email
                    request.session.save()
                    login(request, authenticated_user)
                    messages.success(request, 'Login Successful')
                    return redirect('/orders')
                
        messages.error(request,'Incorrect email or password')
        return render(request, 'user/login.html', {'message': 'Incorrect email or password'})
    
    return render(request, 'user/login.html')

def logout_view(request):
    if request.session.get('email',''):
        del request.session['email']
    request.session.save()
    logout(request)
    messages.success(request,'Logout Successful')
    return redirect('user:login')

def add_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'User with this email already exists!')
            return redirect('app:admin') 
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password') 
        user_type = request.POST.get('user_type')
        hashed_password = make_password(password) 
        user = User.objects.create(
            username=email,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password= hashed_password,
            user_type = user_type
        )
        messages.success(request, 'User added successfully!')
        return redirect('app:admin')  # Redirect to the appropriate URL

    return render(request, 'your_template.html')

def edit_user(request, user_id):
    user = User.objects.get(pk=user_id)
    if request.method == 'POST':
        #print(request.POST)
        user.email = request.POST.get('email')
        if request.POST.get('password'):
            user.password = make_password(request.POST.get('password'))
        user.user_type =  request.POST.get('user_type') if request.POST.get('user_type') is not None else user.user_type 
        # user.set_password(user.password)
        user.save()

        messages.success(request, 'User updated successfully!')
        return redirect('app:admin')  # Redirect to the appropriate URL

    context = {'user': user}
    return redirect('app:adminview')

def remove_user(request, user_id):
    user = User.objects.get(pk=user_id)
    if user.is_superuser:
        messages.error(request, 'SuperUser cannot be deleted!')
        return redirect('app:admin')
    user.delete()

    messages.success(request, 'User deleted successfully!')
    return redirect('app:admin')