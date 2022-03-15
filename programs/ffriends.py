import random
import csv

def read_ffriend(path_to_file):
    with open(path_to_file, newline='\n') as csvfile:
    # with open('/var/www/flaga/dane/ffriends_pl_ua.csv', newline='\n') as csvfile:
        entries = list(csv.reader(csvfile, delimiter=',', quotechar='|'))
        return random.choice(entries)

# print(read_ffriend('/var/www/flaga/dane/ffriends_pl_ua.csv'))