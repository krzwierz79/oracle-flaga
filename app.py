from flask import Flask, render_template, url_for
import random
from programs.wiki_search import wiki_search
from programs.wiki_hero_search import heroes_sorted
from programs.ffriends import read_ffriend
from programs.guten_gaps import build_exercise


app = Flask(__name__)


@app.route('/')
def index():
    text = open('dane/xd.txt').read()
    return render_template("index.html", text=text)


@app.route('/flaga-dla-ukrainy')
def ukr():
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
    box, passage = build_exercise()
    return render_template("gaps.html",
                           box=box,
                           passage=passage)


@app.route('/xd')
def xd():
    return render_template("xd.html")


if __name__ == "__main__":
    app.run()
