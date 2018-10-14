from django.shortcuts import render

# Create your views here.
from django.views import View


class Shop(View):
    def get(self, request):
        return render(request, 'shop/speed.html')

    def post(self, request):
        pass


class Store(View):
    def get(self, request):
        return render(request, 'shop/list.html')

    def post(self, request):
        pass
