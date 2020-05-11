from django.db import models
from django.conf import settings
from django.urls import reverse
from datetime import datetime, timezone
from django.utils.text import slugify




class Generos(models.Model):
    
    genero = models.CharField(max_length=300,blank=True,null=True)
    genre = models.CharField(max_length=300,blank=True,null=True)
    genero_slug = models.CharField(max_length=300,blank=True,null=True,default="accion")

    def get_genero_slug_url(self):
        return reverse("genero-view",kwargs={'pagina':0, 'genero':self.genero_slug})
    def __str__(self):
        return  self.genero

class Novelas(models.Model):
    
    categorias = [
    ('NC', 'Novela China'),
    ('NJ', 'Novela Japonesa'),
    ('NK', 'Novela Koreana'),
    ]
    titulo = models.CharField(max_length=50,null=False,blank=False)
    slug_titulo = models.CharField(max_length=50,null=False,blank=False)
    autor = models.CharField(max_length=50,null=False,blank=False)
    traductor = models.CharField(max_length=50,null=True,blank=True)
    estado = models.CharField(max_length=50,null=True,blank=True,default='En curso')
    categoria = models.CharField(max_length=50,null=False,blank=False,choices = categorias)
    sinopsis = models.TextField(null=False,blank=False)
    generos = models.ManyToManyField(Generos)
    img = models.ImageField(upload_to="portadas_novelas",blank=True)
    first_chapter = models.URLField(null=True,blank=True)

    def __str__(self):
        return self.titulo

    def get_novel_url(self):
        
        novelname = self.slug_titulo
        return reverse("novel-view",kwargs={'novelname':novelname , 'amount': 0 })

class allchaps(models.Model):
    nombre = models.CharField(max_length=50,null=False,blank=False)
    contenido = models.TextField(null=False,blank=False)
    num = models.IntegerField(null=False,blank=False)
    nota = models.CharField(max_length=50,null=True,blank=True)
    novel_info = models.ForeignKey('Novelas', on_delete=models.SET_NULL, null=True, blank=True)
    fecha = models.DateTimeField(null = True,blank = False)
    url = models.URLField(null = True , blank = True)
    

    def get_chapter_as_list(self):
        
        return self.contenido.split('\n\n')

    def get_chapter_url(self):
        
        novelname = self.novel_info.slug_titulo
        return reverse("chapter-view",kwargs={'num':self.num , 'novelname':novelname})

    def get_novel_url(self):
        
        novelname = self.novel_info.slug_titulo
        return reverse("novel-view",kwargs={'novelname':novelname , 'amount': 0 })


    def get_posted_time(self):
        
        time = datetime.now(timezone.utc)
        updated_for = (time - self.fecha)
        if updated_for.days == 0:
            if not updated_for.seconds // 3600 > 0:
                if not updated_for.seconds // 60 > 0:
                    updated_for = str(updated_for.seconds) + " segundos"
                else:
                    updated_for = str((updated_for.seconds // 60)) + " minutos"
            else:
                updated_for = str((updated_for.seconds // 3600)) + " horas"

        else:
            updated_for = str(updated_for.days) + " dias"
        return updated_for

    def get_next_chapter(self):

        novelname = slugify(self.novel_info.titulo)
        return reverse("chapter-view",kwargs={'num':(self.num + 1), 'novelname':novelname})

    def get_prev_chapter(self):

        novelname = slugify(self.novel_info.titulo)
        return reverse("chapter-view",kwargs={'num':(self.num - 1), 'novelname':novelname})

    

        

    

        


class Comentarios(models.Model):
    comentario = models.TextField(null=False,blank=False)
    chapter = models.ForeignKey('allchaps', on_delete=models.CASCADE, null=True, blank=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    fecha = models.DateTimeField(null = True,blank = False)


# Create your models here.
