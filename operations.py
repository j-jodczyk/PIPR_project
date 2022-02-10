from random import choice
from errors import (
    SynonymError,
    RhymeNotFoudError
)
import re
from classes import Paraphraze
import spacy


def split_sentence(sentence):
    '''
    Gets a sentence and returns an array of strings
    made by splitting given sentece into words and
    punctuation marks.
    '''
    return re.findall(r'''[\w']+|[,?."!;]''', sentence)


def join_sentence(words):
    '''
    Gets an array of strings and returns a string made
    by joining strings in the array.
    '''
    sentence = ' '.join(words)
    sentence = re.sub(r'\s+([,?.!;])', r'\1', sentence)
    return sentence.strip()


def get_last_word(words):
    '''
    Gets an array of strings and returns the first
    from last string that is a word, not an punctuation
    mark.
    '''
    i = -1
    while words[i] in '([?.!,])"':
        i -= 1
    index = len(words) + i
    return (Paraphraze(words[i]), index)


def lower_first_letter(sentence):
    '''
    Gets a string and returns it with lowercase first letter.

    '''
    try:
        result = sentence[0].lower() + sentence[1:]
    except IndexError:
        result = sentence
    return result


def upper_first_letter(sentence):
    '''
    Gets a string and returns it with capital first letter.
    '''
    try:
        result = sentence[0].upper() + sentence[1:]
    except IndexError:
        result = sentence
    return result


def parts_of_speech(sentence):
    '''
    Gets a sentence and returns dictionary with every word as
    key and simplyfied parts of speech as values.
    '''
    sp = spacy.load('en_core_web_sm')
    spacy_sent = sp(sentence)
    pos_dict = {
            "ADJ": 'adj',
            "ADP": 'adv',
            "ADV": 'adv',
            "AUX": 'verb',
            "CONJ": 'other',
            "CCONJ": 'other',
            "DET": 'other',
            "INTJ": 'noun',
            "NOUN": 'noun',
            "NUM": 'noun',
            "PART": 'other',
            "PRON": 'noun',
            "PROPN": 'noun',
            "PUNCT": 'punct',
            "SCONJ": 'other',
            "SYM": 'punct',
            "VERB": 'verb',
            "X": 'other',
            "SPACE": 'space'
            }
    sent_dict = {}
    for word in spacy_sent:
        try:
            word_pos = pos_dict[word.pos_]
        except KeyError:
            word_pos = 'other'
        sent_dict[str(word)] = word_pos
    return sent_dict


def create_synonym(sentence):
    '''
    Gets a string and returns the same string with one word changed
    to a synonym.
    '''
    sentence = lower_first_letter(sentence)
    words = split_sentence(sentence)
    pos_dict = parts_of_speech(sentence)
    synonyms = []
    no_synonyms = []
    while synonyms == []:
        try:
            word = Paraphraze(choice(words))
            synonyms = word.synonym()
            chosen_synonym = Paraphraze(choice(synonyms))
            while chosen_synonym.pos() != pos_dict[word.name()]:
                synonyms.remove(chosen_synonym.name())
                chosen_synonym = Paraphraze(choice(synonyms))
        except Exception:
            no_synonyms.append(word)
        if len(no_synonyms) == len(words):
            raise SynonymError()
    replaced = [w.replace(word.name(), chosen_synonym.name()) for w in words]
    return upper_first_letter(join_sentence(replaced))


def expand_with_adj(sentence):
    '''
    Gets a string and returns the same string with added adjectives
    that are often used to describe nouns in given string.
    '''
    sentence = lower_first_letter(sentence)
    words = split_sentence(sentence)
    sp = spacy.load('en_core_web_sm')
    spacy_sent = sp(sentence)
    adj_dict = {}
    for word in spacy_sent:
        if word.pos_ == 'NOUN':
            word_obj = Paraphraze(word.text)
            if word_obj.expand():
                adj_dict[word_obj.name()] = word_obj.expand()
    new_sentence = []
    for i in words:
        if i in adj_dict.keys():
            new_sentence += [choice(adj_dict[i]), i]
        else:
            new_sentence.append(i)
    return upper_first_letter(join_sentence(new_sentence))


def change_to_rhyme(sentence):
    '''
    Gets a string and returns the same string with last word
    changed to a rhyme.
    '''
    words = split_sentence(sentence)
    word, index = get_last_word(words)
    try:
        rhyme = choice(word.rhyme())
    except IndexError:
        raise RhymeNotFoudError("Your sentence doesn't rhyme with anything")
    replaced = []
    for i in range(len(words)):
        if i != index:
            replaced.append(words[i])
        else:
            replaced.append(rhyme)
    return join_sentence(replaced)


def make_rhyme(sentence1, sentence2):
    '''
    Gets two strings and returns a two line string made from
    given strings and with one word changed so that the lines
    rhyme.
    '''
    first_line = split_sentence(sentence1)
    second_line = split_sentence(sentence2)
    last_word_first_line, index1 = get_last_word(first_line)
    last_word_second_line, index2 = get_last_word(second_line)
    last_words = [last_word_first_line, last_word_second_line]
    try:
        word = (choice(last_words))
        rhyme = choice(word.rhyme())
    except IndexError:
        try:
            last_words.remove(word)
            rhyme = choice(last_words[0].rhyme())
        except IndexError:
            message = 'Sorry! None of the sentences rhyme with anything'
            raise RhymeNotFoudError(message)
    replaced = []
    if word.name() in first_line:
        for i in range(len(second_line)):
            if i == index2:
                replaced.append(rhyme)
            else:
                replaced.append(second_line[i])
        poem = join_sentence(first_line) + '\n' + join_sentence(replaced)
    else:
        for i in range(len(first_line)):
            if i == index1:
                replaced.append(rhyme)
            else:
                replaced.append(first_line[i])
        poem = join_sentence(replaced) + '\n' + join_sentence(second_line)
    return poem
