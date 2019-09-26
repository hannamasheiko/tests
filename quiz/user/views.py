from django.contrib.auth import (
    authenticate,
    login,
    logout,
)
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomUserChangeForm, UserLoginForm
from .models import CustomUser


def register_view(request):
    title = "Register"
    form = CustomUserCreationForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password1')
        user.set_password(password)
        user.save()
        return redirect('/')

    context = {
        'form': form,
        'title': title
    }

    return render(request, 'user/forms.html', context)


def login_view(request):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username,
                            password=password)
        login(request, user)
        return redirect('/')
    return render(request, 'user/forms_login.html', {'form': form})


def account_view(request):
    title = "Account"

    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, request.FILES)
        if form.is_valid():
            user = request.user
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.birth_date = form.cleaned_data.get('birth_date')
            user.information = form.cleaned_data.get('information')
            user.profile_image = form.cleaned_data.get('profile_image')
            user.save()
            return redirect('/')
    form = CustomUserChangeForm()
    context = {
        'form': form,
        'title': title
    }

    return render(request, 'user/forms_account.html', context)


def index(request):
    return render(request, 'user/base.html', {})


def logout_view(request):
    logout(request)
    return redirect('/')


def user_info(request):
    query_results = CustomUser.objects.filter(username=request.user).first()

    return render(request, 'user/user_info.html', {'query_results': query_results})
