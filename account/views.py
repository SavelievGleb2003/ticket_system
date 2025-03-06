from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from .forms import LoginForm, ProfileEditForm, UserEditForm
from .models import Profile, Position, Department
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView, PasswordResetView, PasswordResetConfirmView

# Create your views here.
def user_login(request):

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('вы успешно вошли в систему')
                else:
                    return HttpResponse('пользователь больше не доступен')
            else:
                return HttpResponse('неверный пароль или логин')
    else:
        form = LoginForm()
    return render(request,'account/login.html',{'form':form})



@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(
            instance=request.user,
            data=request.POST
        )
        profile_form = ProfileEditForm(
            instance=request.user.profile,
            data=request.POST,
            files=request.FILES
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit.html',{'user_form': user_form,'profile_form': profile_form})




def user_profile(request):
    user = request.user

    # Try to get the profile or create a new one
    profile, created = Profile.objects.get_or_create(user=user)

    return render(request, 'account/user_profile.html', {'profile': profile})


@login_required
def dashboard(request):
    return render(request,
                  'tickets/ticket_list.html',
                  {'section': 'dashboard'})


class my_PasswordChangeView(PasswordChangeView):
    success_url = reverse_lazy("account:password_change_done")

class my_PasswordResetView(PasswordResetView):
    success_url = reverse_lazy("account:password_reset_done")

class my_PasswordResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy("account:password_reset_complete")

