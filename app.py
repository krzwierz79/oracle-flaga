from flask import Flask, render_template, url_for
import random
import os
import wikipedia
import requests
from lxml import html
# local scripts imports
from programs.wiki_search import wiki_search
from programs.wiki_hero_search import heroes_sorted
from programs.ffriends import read_ffriend
from programs.guten_gaps import build_exercise


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static' # not used right now (possibly automate some uploads later)

# main visible routes
@app.route('/')
def index():
    text = open('dane/xd.txt').read()
    return render_template("index.html", text=text)


@app.route('/flaga-dla-ukrainy')
def ukr():
    """
    Return data for Ukraine-themed page
    
        ua_heroes - wiki search by local script, sorted by length of descr
    to_page/from_wiki - simple wiki-search for random element from 'ukraininan' list
    pl/ua_word/mean - random choice od pl/ua true/false-friend words from csv
    """
    ukrainian = random.choice(
        ['Ukrainian Falcons', 'Ukrainian Levkoy', 'Ukrainian alphabet'])
    from_wiki = wiki_search(ukrainian).encode('utf-8').decode()
    ua_heroes = heroes_sorted()
    pl_word, ua_word, pl_mean, ua_mean = read_ffriend(
        '/var/www/flaga/dane/ffriends_pl_ua.csv')
    return render_template("ukraine.html",
                           ua_heroes=ua_heroes,
                           to_page=from_wiki,
                           pl_word=pl_word,
                           ua_word=ua_word,
                           pl_mean=pl_mean,
                           ua_mean=ua_mean)


@app.route('/gaps')
def gaps():
    """
    Return a passage of text with words removed and given in a box
    (fill in the gaps exercise)
    TODO: add a form to select some words for removal (other gaps are randomized)
    TODO: add a possibility to select more texts
    """
    box, passage = build_exercise()
    return render_template("gaps.html",
                           box=box,
                           passage=passage)


@app.route('/xd')
def xd():
    """Basic template render"""
    return render_template("xd.html")

@app.route('/pyscript')
def pyscript():
    """Pyscript template render"""
    return render_template("pyscript.html")

# 029 intro to storing data (in plain text) 

@app.route('/flaga', methods=["GET", "POST"])
def flaga():
    """Uses internal list/s of names, stores wiki-search on them, returns stored data"""
    create_folders() # Set up folder structure for data

      # Flag count number of flag images
    flag_count = len(os.listdir('static/flag_image')) 
      # pick a random flag
      # xd = random.choice(range(1, flag_count))
      # if flag_count < 2:
      #     xd = 1
    xd = random.randint(1, flag_count) # seems simpler than above
    
      # hard-code a flag (testing)
      # ta_flaga = os.path.join(app.config['UPLOAD_FOLDER'], 'flag_image/Flaga__2.jpg')
      # use a rangom flag
    ta_flaga = os.path.join(app.config['UPLOAD_FOLDER'], 'flag_image/Flaga__{}.jpg'.format(xd))
    
      # scrape/store/read heroes data 
    heroes = gather_heroes(xd)
    random.shuffle(heroes)

    return render_template("flaga.html", xd=xd, flaga=ta_flaga, heroes=heroes)

def gather_heroes(xd):

    patriots = [
         'Mikołaj Kopernik', 
         'Rotmistrz Pilecki',
         'Maria Skłodowska',
         'Fryderyk Chopin',
        
         #'Józef Piłsudski'
         #'Tadeusz Kościuszko',
         #'Adam Mickiewicz',
         
        #'Jan Henryk Dąbrowski',
         'Józef Haller',
         # 'Władysław Sikorski',
        # 'Wojciech Korfanty',
         # 'Mieczysław Paluch',
    ]

    pirates = [
         'Anne Bonny', 
         'Czarnobrody',
         'Sir Francis Drake',
         'Henry Morgan',
        "Mary Read",
    ]

    # pick side (flag file and heroes)
    if (xd % 2) == 0:
        heroes = pirates # even num in static/flga_image/Flaga__
        hero_tag = 'pirate'
    else:
        heroes = patriots # odd
        hero_tag = 'patriot'

    # TODO: not used on the web
    greetings = [
        'pozdrawia',
        '/wave',
        '/wink',
        'wita',
    ]

      # pull new data from wikipedia
    wikipedia.set_lang("pl")

    saved_heroes = os.listdir('dane/heroes/saved_heroes')
    saved_heroes = [h.split('.')[0] for h in saved_heroes]

    for hero in heroes:
        if hero not in saved_heroes:

        # Get some info and link.
            some_info = wikipedia.page(hero)
            info_intro = some_info.content.split('\n\n')[0]
            url = f"<a href={some_info.url}>Czytaj dalej na wikipedii</a>"
            images = some_info.images
            # Get what hero thinks. (query wikiquotes)
            hero_think(hero)
            
            # Get & save images. TODO: not used
            # images = some_info.images
            # n_photos = 0
            # for i, image_url in enumerate(images):
            #     if i < 3:
            #         hero_str = '11'.join(hero.split())
            #         image_name = '{}_{}.legend'.format(hero_str, i)
            #         save_image(image_url, image_name)
            #         n_photos += 1

            # Save all data into file with patriot or pirate ext (side/hero_tag)
            with open('dane/heroes/saved_heroes/'+hero+"."+hero_tag, "w+") as f:
                f.write(hero + '\n')
                f.write('\n') #str(n_photos) + '\n')
                f.write(info_intro + '\n')
                f.write(url)
                for img_url in images:
                    if img_url[len(img_url) - 3 :] == "jpg":
                        f.write("\n" + img_url)
                        break

        # else:
        #     # TODO: not used on the web - display info here already exists? 
        #     greeting = random.choice(greetings)
        #     print(hero, greeting)

        heroes = []
        # read all heroes
        for hero_file in os.listdir('dane/heroes/saved_heroes'):
            # select files for chosen side
            if hero_file.endswith(hero_tag):
            # build dict with data to display
                hero = {}
                some_info = open('dane/heroes/saved_heroes/'+hero_file).readlines()
                hero['name'] = some_info[0]
                #photo_nr = random.choice(range(int(some_info[1])))
                #hero_str = '11'.join(hero['name'][:-1].split())
                #hero['image'] = '{}_{}.legend'.format(hero_str, photo_nr)
                hero_quotes = open('dane/heroes/hero_think/' + hero['name'][:-1] + ".hero").readlines()
                hero['quote'] = random.choice(hero_quotes)
                hero['description'] = '\n'.join(some_info[2:-2])
                hero['description'] = bold(hero['description'])
                hero['url'] = some_info[-2]
                hero["image"] = some_info[-1]
                heroes.append(hero)
    return heroes

# def save_image(image_url, image_name):
#     image = requests.get(image_url).content
#     save_as = 'static/hero_image/{}'.format(image_name)
#     with open(save_as, 'wb') as ap:
#         ap.write(image)
#     return save_as

def bold(hero_info):
    nice = [
        "nauk",
        "gen",
        "zwy",
        "odk",
        "zał",
        "rod",
        "organiza",
        "astronom",
        "inż",
        "herb",
        "wojsk",
        "uczon",
        "pira",
        "kors",
        "angiel",
        "por",
        "kapita" "nobl",
        "wybitn",
        "romanty",
        "fizy",
        "filozof",
        "kocha",
        "woli",
        "kawaler",
        "skazan",
        "chem",
    ]

    right_desc = []
    words = [w for w in hero_info.split()]
    for w in words:
        for woah in nice:
            if w.lower().startswith(woah):
                w = '<b>'+w+'</b>'
        right_desc.append(w)
    right_desc = " ".join(right_desc)
    return right_desc

def hero_think(name):
    url_name = name.replace(' ', '_')
    url = 'https://pl.wikiquote.org/wiki/{}'.format(url_name)
    hero_wikiquotes = requests.get(url)
    with open('dane/heroes/hero_think/'+name+".hero", "w+") as f:
        # selects lines to drop or process 
        for line in hero_wikiquotes.text.split('\n'):
            if line.startswith('<h2>O'):
                continue
            if line.startswith('<ul><li>'):
                # save clean text strings
                tree = html.fromstring(line)
                quote = tree.text_content().strip()
                if quote.startswith('Utworzyć'):
                    f.write('Nie chce mi się z tobą gadać...\n')
                    # or format with name
                    # f.write(name + ' nie chce z tobą gadać...\n')
                # more strings to drop
                elif not quote.startswith(('Opis', 'Autor', 'Żródło', 'Zobacz też')):
                    f.write(quote + '\n')
                    print('-', quote)

def create_folders():
    os.system("mkdir static/hero_image")
    os.system("mkdir static/flag_image")
    os.system("mkdir dane/heroes/saved_heroes")
    os.system("mkdir dane/heroes/hero_think")

# end 029

if __name__ == "__main__":
    app.run()
