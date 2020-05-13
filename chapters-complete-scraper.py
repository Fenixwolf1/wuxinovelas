import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wuxi.settings')
django.setup()


from bs4 import BeautifulSoup
from urllib.request import urlopen,Request
from datetime import datetime, timezone
from novelas.models import Novelas,allchaps
from time import sleep

def get_current_chapter(last_chapter):

    if last_chapter:
        current_chapter = last_chapter.url
        #Getting new chapters from  existing novel chapters in the database
        reg_url = current_chapter
        req = Request(url=reg_url, headers=headers) 
        page = urlopen(req)
        urlindex = page.read()
        page.close()

        parsed_page = BeautifulSoup(urlindex,'html.parser')

        #Checking if we are in the last chapter
        next_chap = parsed_page.find_all(id="next_chap")[0]
        if "disabled" in next_chap.attrs:
            next_chap = "last"
            return current_chapter,0,next_chap

        next_chap = base_url + next_chap.get('href')

        #Getting next chapter url and it's chapter number
        current_chapter = next_chap
        numero = last_chapter.num + 1
        return current_chapter, numero,next_chap
    else:
        #Getting first chapter for a novel in the database
        current_chapter = current_novel.first_chapter
        numero= 1
        next_chap = ""
        return current_chapter,numero,next_chap









scraped_chapters = 0
base_url= "https://novelfull.com"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

ongoing_novels = Novelas.objects.filter(estado="Completada")
    
for current_novel in ongoing_novels:

    last_chapter = allchaps.objects.filter(novel_info = current_novel).order_by('-id').first()
    instance = get_current_chapter(last_chapter)
    current_chapter = instance[0]
    numero = instance[1]
    next_chap=instance[2]

    while next_chap != "last":
        
        # Downloading and opening the novel chapter
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
        reg_url = current_chapter
        req = Request(url=reg_url, headers=headers) 
        page = urlopen(req)
        chapter = page.read()
        page.close()


        # Parsing the chapter
        parsed_chapter = BeautifulSoup(chapter,'html.parser')


        #Checking if we are in the last chapter
        next_chap = parsed_chapter.find_all(id="next_chap")[0]
        if "disabled" in next_chap.attrs:
            next_chap = "last"
        else:
            next_chap = base_url + next_chap.get('href')


        # Extracting the data
        chapter_content =  parsed_chapter.find(id='chapter-content')
        chapter_text = ""
        
        
        for chapter_body in chapter_content.find_all('p'):
            if chapter_body.text != "":
                chapter_text +=  chapter_body.text + "\n\n"
        
        chapter_name = chapter_text.split("\n",1)[0]
        # Saving to the database
        
        fecha = datetime.now(timezone.utc)

        chapter_instance = allchaps(nombre=chapter_name, contenido=chapter_text, num=numero,
                                 fecha=fecha, novel_info_id=current_novel.id, url=current_chapter)
        chapter_instance.save()

        current_chapter = next_chap
        numero += 1
        scraped_chapters += 1
        if scraped_chapters > 4000:
            import sys
            sys.exit()
        sleep(0.20)
    





