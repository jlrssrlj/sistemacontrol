from django.shortcuts import render
from django.views.decorators.http import require_http_methods


@require_http_methods(["GET","POST"])
def principal(request):
    return render(request,'index.html')
