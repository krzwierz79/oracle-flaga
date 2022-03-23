import random
import wikipedia as wiki

wiki.set_lang("en")

def character(name):
    content = wiki.summary(name, sentences=3)
    return content

def three_amigos():
    entry_list = [
        'Andriy Kuzmenko',         
        'Vasyl Hrytsak',           
        'Filaret (Denysenko)',     
        'Maksym Shapoval',     
        'Mikhail Zhyzneuski',  
        'Reşat Amet',          
        'Vasyl Slipak'        
    ]

    descriptions = []
    for i in range(3):
        entry = random.choice(entry_list)
        index = entry_list.index(entry)
        entry_list.pop(index)

        entry_desc = character(entry)
        info = [entry, entry_desc, wiki.page(entry).url]
        descriptions.append(info)
    return descriptions

def add_word_count(top_list):
  for nested_list in top_list:
    word_count = len(nested_list[1].split())
    nested_list.append(word_count)
  return top_list

def sort_by_word_count(top_list):
  top_list.sort(key = lambda nested_list: nested_list[3], reverse = True)
  return top_list

def heroes_sorted():
  return sort_by_word_count(add_word_count(three_amigos()))

# print(heroes_sorted())

print(wiki.page("Andriy Kuzmenko").categories)