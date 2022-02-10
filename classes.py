import requests
import spacy


class Paraphraze:
    '''
    A class used to represent a word to be modified.
    Contains attributes:
    :param name: word name
    :type name: str
    '''
    def __init__(self, name):
        self._name = name

    def name(self):
        return self._name

    def pos(self):
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
        sp = spacy.load('en_core_web_sm')
        doc = sp(self._name)
        return pos_dict[doc[0].pos_]

    def _return_json(self, url):
        '''
        Returns request in json form.
        '''
        action = requests.get(url)
        return action.json()

    def _change_to_array(self, action):
        '''
        Takes json dictionary and returns array
        with only 'word' values.
        '''
        words = []
        for dictionary in action:
            word = dictionary['word']
            words.append(word)
        return words

    def synonym(self):
        '''
        Returns an array of synonyms of the name.
        '''
        address = f'https://api.datamuse.com/words?rel_syn={self.name()}'
        synonyms = self._return_json(address)
        return self._change_to_array(synonyms)

    def expand(self):
        '''
        Returns an array of adjectives related the name.
        '''
        address = f'https://api.datamuse.com/words?rel_jjb={self.name()}'
        adjectives = self._return_json(address)
        return self._change_to_array(adjectives)

    def rhyme(self):
        '''
        Returns an array of rhymes of the name.
        '''
        address = f'https://api.datamuse.com/words?rel_rhy={self.name()}'
        rhymes = self._return_json(address)
        return self._change_to_array(rhymes)
