from django.shortcuts import render,get_object_or_404
from .models import allchaps,Novelas,Generos
from django.urls import reverse
import re
from django.db.models import Q
from django.http import Http404,HttpResponseRedirect



def home_view(request):

    chapter_list = allchaps.objects.all().order_by('-id')[:15]
    nc_slider = Novelas.objects.filter(generos__genre = 'Action').order_by('-id')[:4]
    nj_slider = Novelas.objects.filter(generos__genre = 'Fantasy').order_by('-id')[4:8]
    generos = Generos.objects.all()
    context = {
        'chapter_list': chapter_list,
        'nc_novels':nc_slider,
        'nj_novels':nj_slider,
        'generos':generos,
    }
    return render(request,"home.html",context)

def chapter_view(request,novelname,num):

    
    
    chapter = get_object_or_404(allchaps,novel_info__slug_titulo__iexact = novelname, num = num)
    
    context={
        'chapter':chapter
    }
    return render(request,"chapter.html",context)


def novel_view(request , novelname , amount):

    search_name = novelname
    novel = get_object_or_404(Novelas,slug_titulo__iexact = search_name)

    novel_chapter_num = allchaps.objects.filter(novel_info__slug_titulo__iexact = search_name).count() 
    novel_chapter_num = novel_chapter_num // 50
    lower_bound = amount * 50
    upper_bound = lower_bound + 50
    

    if 0 < amount <= novel_chapter_num:
        chapters = allchaps.objects.filter(novel_info__slug_titulo__iexact = search_name)[lower_bound:upper_bound]
        context={
        'novel':novel,
        'slug_novel':novelname,
        'tabs':range(novel_chapter_num + 1),
        'chapters': chapters,
        'chapter_page':amount,
        'from':lower_bound,
        'to':upper_bound,
        }
        
    else:
        chapters = allchaps.objects.filter(novel_info__slug_titulo__iexact = search_name)[:50]
        context={
        'novel':novel,
        'slug_novel':novelname,
        'tabs':range(novel_chapter_num + 1),
        'chapters': chapters,
        'chapter_page':amount,
        }
        
    return render(request,"novelpage.html",context)


def genero_view (request, genero, pagina):
    lower_bound = pagina * 12
    upper_bound = lower_bound + 12

    
    cantidad_novelas = Novelas.objects.filter(generos__genero_slug = genero).count()
    novelas = Novelas.objects.filter(generos__genero_slug = genero)[lower_bound:upper_bound]
    nombre = "Novelas " + Generos.objects.get(genero_slug = genero).genero
        
    if not cantidad_novelas % 12 == 0:
        cantidad_paginas = (cantidad_novelas // 12)+1
    else:
        cantidad_paginas = (cantidad_novelas // 12)
    if  pagina >= cantidad_paginas or pagina < 0:
        return HttpResponseRedirect(reverse('genero-view',kwargs={'genero':genero,'pagina':0}))
    
    
    context={
        'novelas':novelas,
        'nombre':nombre,
        'paginator':range(cantidad_paginas),
        'pagina':pagina,
        'max_pag':(cantidad_paginas-1),
        'genero':genero,
    }
    
    return render(request,"generos.html",context)

def search_view(request):
    if request.GET.get('page'):
        pagina = int(request.GET.get('page'))
    else:
        pagina = 0

    lower_bound = pagina * 8
    upper_bound = lower_bound + 8

    if request.GET.get('page'):
        busqueda = request.GET.get('busqueda')
    else:
        raise Http404

    novelas_startswith = Novelas.objects.filter(titulo__istartswith=busqueda)
    novelas_contains = Novelas.objects.filter(titulo__icontains=busqueda)
    novelas = novelas_startswith.union(novelas_contains)
    cantidad_novelas = novelas.all().count()
    
    novelas = novelas.all()[lower_bound:upper_bound]
        
    if not cantidad_novelas % 8 == 0:
        cantidad_paginas = (cantidad_novelas // 8)+1
    else:
        cantidad_paginas = (cantidad_novelas // 8)
    
    if  pagina >= cantidad_paginas or pagina < 0:
        return HttpResponseRedirect(reverse('search-view'))
    
    
    context={
        'novelas':novelas,
        'paginator':range(cantidad_paginas),
        'pagina':pagina,
        'max_pag':(cantidad_paginas-1),
        'busqueda':busqueda,
    }
    
    return render(request,"busqueda.html",context)
    