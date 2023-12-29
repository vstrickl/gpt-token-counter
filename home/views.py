from django.shortcuts import render

# Create your views here.
def home(request):
    header = 'Welcome to your Personal AI App'
    sub_header = 'Use this app to test AI and LLM APIs.'

    context = {
        'header':header,
        'sub_header':sub_header,
    }

    return render(request, 'home.html', context)