import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wuxi.settings')
django.setup()


from bs4 import BeautifulSoup
from urllib.request import urlopen,Request
import requests
from slugify import slugify
from novelas.models import Novelas,Generos


page_url = "https://novelfull.com"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}



for index in range(1,32):

    base_url= f"https://novelfull.com/index.php/latest-release-novel?page={index}"
    

    req = Request(url=base_url, headers=headers) 
    page = urlopen(req)
    content = page.read()
    page.close()

    parsed_content = BeautifulSoup(content,'html.parser')

    novels_in_page = parsed_content.find_all("h3", class_="truyen-title")
    for link in novels_in_page:

        synopsis = ""
        generos_novela = []

        novel = (link.a.attrs['href'])

        req = Request(url=(page_url + novel), headers=headers) 
        page = urlopen(req)
        content = page.read()
        page.close()

        parsed_content = BeautifulSoup(content,'html.parser')

        title = parsed_content.find("h3", class_="title").text

        slug_title = slugify(title)

        author = parsed_content.find("div", class_="info").div.a.text

        genres = parsed_content.find("div", class_="info").div.next_sibling
        genres = genres.find_all('a')

        for genre in genres:
            novel_genre = Generos.objects.get(genre=genre.text)
            generos_novela.append(novel_genre.id)

        translator = "Desconocido"

        state = parsed_content.find("div", class_="info").div.next_sibling.next_sibling.next_sibling.a.text
        if state == "Completed":
            state = "Completada"
        else:
            state = "En curso"
        
        category = "NC"

        synopsis_div = parsed_content.find("div", class_="desc-text")

        for parap in synopsis_div.find_all('p'):
            synopsis += parap.text + "\n\n"

        synopsis = synopsis.lstrip()

        image = page_url + parsed_content.find("div", class_="book").img['src']
        image_url = slugify(parsed_content.find("div", class_="book").img['alt']) + ".jpg"

        alt = "media/portadas_novelas/" + image_url
        r = requests.get(image)

        with open(alt,"wb") as novel_image:
            novel_image.write(r.content)

        img_dir = "portadas_novelas/" + image_url

        first_chap = page_url + parsed_content.find("ul", class_="list-chapter").li.a['href']

        novel_instance = Novelas(titulo=title, autor=author, traductor=translator,
                                 categoria=category, sinopsis=synopsis, estado=state, 
                                 img=img_dir, first_chapter=first_chap, slug_titulo=slug_title)
        novel_instance.save()

        novel_instance.generos.add(*generos_novela)

        















