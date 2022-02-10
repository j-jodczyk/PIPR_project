from operations import (
    create_synonym,
    expand_with_adj,
    change_to_rhyme,
    make_rhyme,
    split_sentence,
    join_sentence,
    get_last_word,
    lower_first_letter,
    upper_first_letter,
    parts_of_speech
)
from errors import (
    SynonymError,
    RhymeNotFoudError
)
from random import seed
import requests
import pytest


def test_split_sentence():
    assert split_sentence("What's up?") == ["What's", "up", "?"]
    split = ['Did', 'you', 'mean', '"', 'fish', '"', '?']
    assert split_sentence('Did you mean "fish"?') == split
    split2 = ['Hello', ',', 'how', 'are', 'you', '?']
    assert split_sentence('Hello, how are you?') == split2


def test_join_sentence():
    words = ["Oh", "yeah", ",", "I'll", "tell", "you", "somethin'", "!"]
    assert join_sentence(words) == "Oh yeah, I'll tell you somethin'!"


def test_get_last_word():
    words = ["I", "normally", "don’t", "enjoy",
             "making", "people", "laugh", "."]
    laugh, index = get_last_word(words)
    assert index == 6
    assert laugh.name() == 'laugh'


def test_lower_first_letter():
    assert lower_first_letter('Hello there') == 'hello there'
    assert lower_first_letter('HEllo there') == 'hEllo there'
    assert lower_first_letter("It's Monday") == "it's Monday"


def test_upper_first_letter():
    assert upper_first_letter('Hello there') == 'Hello there'
    assert upper_first_letter('hEllo there') == 'HEllo there'
    assert upper_first_letter("it's Monday") == "It's Monday"


def test_parts_of_speech():
    sentence = "I have learned to tune myself out"
    pos_dict = {
        'I': 'noun',
        'have': 'verb',
        'learned': 'verb',
        'to': 'other',
        'tune': 'verb',
        'myself': 'noun',
        'out': 'adv'
    }
    assert parts_of_speech(sentence) == pos_dict


def test_create_synonym():
    seed(3)
    sentence = 'He often goes fishing'
    assert create_synonym(sentence) == 'He frequently goes fishing'


def test_create_synonym_double_meanining():
    seed(27)
    sentence = 'I take a look at the paper'
    assert create_synonym(sentence) == 'I take a search at the paper'


def test_create_synonym_not_found(monkeypatch):
    sentence = 'I like trains'

    class MockResponse:
        def json(a):
            return []

    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr(requests, 'get', mock_get)
    with pytest.raises(SynonymError):
        create_synonym(sentence)


def test_expand_with_adj():
    seed(20)
    sentence = 'I look at the floor.'

    result = 'I look at the cold floor.'
    assert expand_with_adj(sentence) == result


def test_expand_with_adj_with_interpunction():
    seed(10)
    sentence = 'Boy, have you lost your mind?!'
    r = 'Boy, have you lost your troubled mind?!'
    assert expand_with_adj(sentence) == r


def test_expand_with_adj_adjective_already_exists():
    seed(10)
    sentence = 'Beautiful flower'
    r = 'Beautiful single flower'
    assert expand_with_adj(sentence) == r


def test_change_to_rhyme():
    seed(30)
    sentence = "If I don't have some cake soon I might die"
    result = "If I don't have some cake soon I might underlie"
    assert change_to_rhyme(sentence) == result


def test_change_to_rhyme_interpunction_at_the_end():
    seed(30)
    sentence = 'Would I rather be feared or loved...?'
    result = 'Would I rather be feared or unloved...?'
    assert change_to_rhyme(sentence) == result


def test_change_to_rhyme_repeted_words():
    seed(30)
    sentence = 'Would I rather be feared or feared...?'
    result = 'Would I rather be feared or beaird...?'
    assert change_to_rhyme(sentence) == result


def test_change_to_rhyme_interpunction_second_to_last():
    seed(20)
    sentence = 'I just hope I find it along the, way'
    result = 'I just hope I find it along the, today'
    assert change_to_rhyme(sentence) == result


def test_change_to_rhyme_not_found():
    seed(10)
    sentence = 'Nothing rhymes with "month"'
    with pytest.raises(RhymeNotFoudError):
        change_to_rhyme(sentence)


def test_make_rhyme():
    seed(20)
    sentence1 = "I don't hate it."
    sentence2 = "I just don't like it at all and it's terrible."
    res = "I don't hate it.\nI just don't like it at all and it's chit."
    assert make_rhyme(sentence1, sentence2) == res


def test_make_rhyme_not_found():
    seed(20)
    sentece1 = 'Nothing rhymes with "month"'
    sentece2 = 'Nothing rhymes with "ninth"'
    with pytest.raises(RhymeNotFoudError):
        make_rhyme(sentece1, sentece2)
