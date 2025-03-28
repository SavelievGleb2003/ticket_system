from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from .forms import LoginForm, UserEditForm, ProfileForm

from django.contrib import messages
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




def different_user_profile(request, profile_id):
    # Try to get the profile or create a new one
    profile = get_object_or_404(Profile, user_id=profile_id)

    return render(request, 'account/different_user_profile.html', {'profile': profile})




@login_required
def user_profile(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)

    if request.method == 'POST' and 'update_profile' in request.POST:

        profile.date_of_birthday = request.POST.get('date_of_birthday', profile.date_of_birthday)
        profile.number = request.POST.get('number', profile.number)

        # Обновляем отдел
        if user.department:
            user.department.description = request.POST.get('department_description', user.department.description)
            user.department.save()

        # Обновляем должность
        if user.position:
            user.position.description = request.POST.get('position_description', user.position.description)
            user.position.save()

        # Сохраняем профиль и пользователя
        profile.save()
        user.save()  # <-- Добавляем это, чтобы убедиться, что изменения сохраняются

        messages.success(request, "Профиль успешно обновлен.")
        return redirect('account:user_profile')

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

