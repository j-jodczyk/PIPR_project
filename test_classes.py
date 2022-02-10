from classes import Paraphraze
import requests


def test_paraphraze_create():
    apple = Paraphraze('apple')
    assert apple.name() == 'apple'


def test_paraphraze_pos():
    apple = Paraphraze('apple')
    assert apple.pos() == 'noun'


def test_return_json(monkeypatch):
    fish = Paraphraze('fish')
    assert fish.name() == 'fish'

    class MockResponse:
        def json(a):
            return {"fish": "[{'word': 'mark', 'score': 4689}]"}

    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr(requests, 'get', mock_get)
    result = fish._return_json('https://fakeurl')
    assert result['fish'] == "[{'word': 'mark', 'score': 4689}]"


def test_change_to_array():
    fish = Paraphraze('fish')
    assert fish.name() == 'fish'
    action = [{'word': 'mark', 'score': 4689}]
    assert fish._change_to_array(action) == ['mark']


def test_change_to_array_empty():
    fish = Paraphraze('fish')
    assert fish.name() == 'fish'
    assert fish._change_to_array([]) == []


def test_paraphraze_synonym(monkeypatch):
    fish = Paraphraze('fish')
    assert fish.name() == 'fish'

    class MockResponse:
        def json(a):
            return [{'word': 'mark', 'score': 4689}]

    def mock_get(*args, **kwargs):
        return MockResponse()
    monkeypatch.setattr(requests, 'get', mock_get)
    assert fish.synonym() == ['mark']


def test_paraphraze_synonym_empty(monkeypatch):
    fish = Paraphraze('fish')
    assert fish.name() == 'fish'

    class MockResponse:
        def json(a):
            return []

    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr(requests, 'get', mock_get)
    assert fish.synonym() == []


def test_paraphraze_expand(monkeypatch):
    fish = Paraphraze('fish')
    assert fish.name() == 'fish'

    class MockResponse:
        def json(a):
            return [{"word": "small", "score": 1001}]

    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr(requests, 'get', mock_get)
    assert fish.expand() == ['small']


def test_paraphraze_rhyme(monkeypatch):
    fish = Paraphraze('fish')
    assert fish.name() == 'fish'

    class MockResponse:
        def json(a):
            return [{"word": "dish", "score": 1794, "numSyllables": 1}]

    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr(requests, 'get', mock_get)
    assert fish.expand() == ['dish']
