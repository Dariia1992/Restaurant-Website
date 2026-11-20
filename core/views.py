from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,'core/home.html')

def privacy_policy(request):
    return render(request, 'core/privacy_policy.html')