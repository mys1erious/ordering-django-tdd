from django.shortcuts import render


def main_page(request):
    if request.method == 'GET':
        return render(request, 'home_page.html')
