import random
import re

passage = "The Python creator and Dropbox engineer reflects on his early days in programming. Guido van Rossum is the creator and benevolent dictator for life BDFL of the Python programming language. Here he reflects on his path and shares what he's been working on since joining Dropbox. Read on for this and a hint at what's next for Dropbox, for Python, and for the BDFL himself.\n You were an electronics hobbyist before becoming a programmer. How did you get started in electronics? \n Okay, we're going waaaay back. I don't know exactly why I got into electronics as a kid. I remember that from the last grade in elementary school and probably through my second year in university, electronics kits and my own designs were one of my big passions. \n It wasn't always an easy path.\n In elementary school, I took one of the first projects I built into class as a show and tell project. There was no one who understood what it was or why it was interesting or cared. It's a very vague memory. I just know that I took it in, and it fell flat."

words_to_check = ["creator", "benevolent", "vague",
                  "hobbyist", "kits", "path", "Voldemort"]

# removed_words = []


# using regex( findall() )
# to extract words from string
# words = re.findall(r'\w+', passage)

# printing result
# print("\nThe words of string are")
# for i in words:
#     print(i)


def splitting_sentences(text: str, split_by: str):
    text = [i.strip() for i in text.split(split_by) if i]
    return text


split_passage = splitting_sentences(passage, ".")


def replace_str(word_list: list, sentence_num: int):
    chosen_word = ''
    while len(chosen_word) < 2:
        chosen_word = word_list[random.randint(0, len(word_list)-1)]
    for word in words_to_check:
        if word in word_list:
            chosen_word = word
    char_count = len(chosen_word)
    replacement = f"({sentence_num}){' _' * char_count} "
    return [chosen_word, replacement]


def build_exercise():
    removed_words = []
    gapped_passage = []

    for count, sentence in enumerate(split_passage):
        # print(f"{count} zdanie: {sentence}")
        removed, replacement = replace_str(
            splitting_sentences(sentence, " "), count + 1)
        gapped_sentence = f"{sentence.replace(removed, replacement, 1)}."
        removed_words.append(removed)
        random.shuffle(removed_words)
        gapped_passage.append(gapped_sentence)

        # print(f"zdanie z luką: {gapped_sentence}")
    # print(f"usunięto {len(removed_words)} słów: {removed_words} z {len(gapped_passage)} zdań.")
    # random_words = list(set(removed_words) - set(words_to_check))
    # unchecked_words = list(set(words_to_check) - set(removed_words))
    # print(f"losowe słowa: {random_words}")
    # print(f"niesprawdzone słowa: {unchecked_words}")
    return [removed_words, gapped_passage]


build_exercise()
# print(build_exercise())

# todo - wyszukać niesprawdzone słowa w innych tekstach (wikipedia?) pobrać je i dołączyć do zdań
# todo2 - dodać obsługę zwrotów zamiast pojedynczych słów (np "used to" a nie tylko "used")
