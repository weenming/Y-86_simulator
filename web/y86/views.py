from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views import generic

# Create your views here.

cpu =   {
            "PC": 0,
            "REG": {
                "rax": 1,
                "rcx": -2,
                "rdx": 3,
            },
            "CC": {
                "ZF": 0,
                "SF": 0,
                "OF": 0
            },
            "STAT": 1,
            "MEM": {
                "64": 4294901760,
                "72": 65535,
            },
        }


def index(request):
    return render(request, 'y86/index.html')


def detail(request):
    return render(request, 'y86/detail.html', {"cpu": cpu})
