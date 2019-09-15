from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from portal.forms import LoginForm

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated '\
                                        'successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    context= {'form':form}
    return render(request, 'portal/login.html', context)

# authenticate() comprueba las credenciales del usuario y devuelve un usuario
# si estuvieran bien. En cambio, login() lo que hace es modificar la session.
