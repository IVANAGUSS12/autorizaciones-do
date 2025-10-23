
from django.shortcuts import render

def panel_index(request):
    return render(request, "panel.html")

def qr_index(request):
    return render(request, "qr.html")

def qr_gracias(request):
    return render(request, "gracias.html")
