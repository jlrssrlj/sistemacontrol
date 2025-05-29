from django.shortcuts import render,redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login, logout


@require_http_methods(["GET","POST"])
def principal(request):
    return render(request,'index.html')

@require_http_methods(["GET","POST"])
def login_view(request):
    error = None
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user= authenticate(request, username=username, password= password)
        if user is not None:
            login(request, user)
            return redirect('ventas')
        else:
            error = "usuairo o contraseña incorrecto"
    return render(request, 'login.html',{'error':error})

@require_http_methods(["GET"])
def logout_view(request):
    logout(request)
    return redirect('login')

@require_http_methods(["GET","POST"])
def ventas(request):
    return render(request, 'ventas.html')