
from django.contrib import admin
from django.urls import path
from django.conf import settings

from django.conf.urls.static import static
from novelas.views import home_view,chapter_view,novel_view,genero_view,search_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home_view, name="home-view"), 
    path('<slug:novelname>/capitulo-<int:num>/',chapter_view, name="chapter-view"),
    path('<slug:novelname>/capitulos/<int:amount>/',novel_view, name="novel-view"),
    path('genero/<slug:genero>/<int:pagina>/',genero_view, name="genero-view"),
    path('resultado_busqueda',search_view, name="search-view"),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
