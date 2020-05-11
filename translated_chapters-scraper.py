from bs4 import BeautifulSoup
from urllib.request import urlopen,Request
import sqlite3
from datetime import datetime, timezone
from yandex_translate import YandexTranslate


#Yandex translator
translator = YandexTranslate('trnsl.1.1.20200316T025958Z.ce545067c6d33a3b.55a842089b907006cb47ccd4ea74a1bbebbdb8e5')



# Database connection
connection = sqlite3.connect('db.sqlite3')
cur = connection.cursor()

base_url= "https://novelfull.com"
char_count = 0
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

cur.execute("SELECT url FROM novelas_allchaps ORDER BY id DESC LIMIT 1" )
current_chapter = cur.fetchone()
if current_chapter:
    current_chapter = current_chapter[0]

if current_chapter:
    #Getting new chapters from an existing novel in the database
    reg_url = current_chapter
    req = Request(url=reg_url, headers=headers) 
    page = urlopen(req)
    urlindex = page.read()
    page.close()

    parsed_page = BeautifulSoup(urlindex,'html.parser')

    next_chap = parsed_page.find_all(id="next_chap")[0]
    if "disabled" in next_chap.attrs:
        import sys
        sys.exit()
    else:
        next_chap = base_url + next_chap.get('href')

    #Getting next chapter url and it's chapter number
    current_chapter = next_chap
    cur.execute("SELECT num FROM novelas_allchaps ORDER BY id DESC LIMIT 1")
    numero = cur.fetchone()[0] + 1

else:
    #Getting chapters from a not existing novel in the database
    current_chapter = "https://novelfull.com/city-of-sin/prologue.html"
    numero= 1
    next_chap = ""
    
while next_chap != "last":
    
    # Downloading and opening the novel chapter
    split_index = 1
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
    translated_text = ""
    
    
    for chapter_body in chapter_content.find_all('p'):
        if chapter_body.text != "":
            chapter_text +=  chapter_body.text + "\n\n"
        if (len(chapter_text) > (split_index * 8000)):
            chapter_text += "###"
            split_index += 1

    splitted_chapter = chapter_text.split("###")
    splitted_chapter = [notempty for notempty in splitted_chapter if notempty != ""]
    for part in splitted_chapter:
        translated_text += translator.translate(part,'en-es')['text'][0]
    chapter_name = translated_text.split("\n",1)[0]
    # Saving to the database
    char_count += len(translated_text)
    fecha = datetime.now(timezone.utc)
    cur.execute("INSERT INTO novelas_allchaps VALUES (?,?,?,?,?,?,?,?)",(None,chapter_name,translated_text,numero,None,fecha,1,current_chapter,))
    connection.commit()
    current_chapter = next_chap
    numero += 1

connection.close()





