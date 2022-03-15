import wikipedia as wiki
wiki.set_lang("en")

def wiki_search( name):
    content = wiki.summary(name, sentences=6)
    return content

# print(wiki_search("Ukrainian Levkoy"))