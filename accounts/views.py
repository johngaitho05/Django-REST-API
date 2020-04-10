from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect
from forms import LoginForm


def anonymous_required(function=None, redirect_url=None):
    if not redirect_url:
        redirect_url = settings.LOGIN_REDIRECT_URL

    actual_decorator = user_passes_test(
        lambda u: u.is_anonymous,
        login_url=redirect_url
    )

    if function:
        return actual_decorator(function)
    return actual_decorator


@anonymous_required
def login_view(request):
    form = LoginForm

    if request.method == 'POST':
        if form.is_valid(request.POST):
            uname = form.cleaned_data.get('username')
            passwrd = form.cleaned_data.get('password')
            user = authenticate(username=uname, password=passwrd)
            login(request, user)

        else:
            return render(request, 'accounts/login.html', {'error': 'Invalid username or password', 'form': form})

    return render(request, 'accounts/login.html', {'form': form})
