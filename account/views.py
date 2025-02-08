from django.shortcuts import render, get_object_or_404, redirect

from .forms import CreateUserForm, LoginForm
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
from django.http import HttpResponse

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


def register(request):
    form = CreateUserForm()
    if request.method=="POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list.html')
    context = {'form': form}
    return render(request, 'blog/TD/create_user.html', context)