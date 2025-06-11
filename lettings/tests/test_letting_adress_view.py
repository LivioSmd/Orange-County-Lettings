import pytest
from django.test import RequestFactory
from lettings import views
from lettings.models import Letting


class DummyLetting:
    """
    Letting factice sans accès à la DB.
    """
    def __init__(self, title="dummy", address="addr"):
        self.title = title
        self.address = address


def test_index_view_returns_correct_template_and_context(monkeypatch):
    """
    La vue index doit appeler render avec 'lettings/index.html'
    et le contexte contenant 'lettings_list'.
    """
    dummy_list = [DummyLetting("L1", "A1"), DummyLetting("L2", "A2")]
    monkeypatch.setattr(Letting.objects, 'all', lambda: dummy_list)

    def fake_render(request, template, context):
        return {'template': template, 'context': context}
    monkeypatch.setattr(views, 'render', fake_render)

    rf = RequestFactory()
    request = rf.get('/lettings/')

    result = views.index(request)

    assert result['template'] == 'lettings/index.html'
    assert 'lettings_list' in result['context']
    assert result['context']['lettings_list'] is dummy_list


def test_letting_view_returns_correct_template_and_context(monkeypatch):
    """
    La vue letting doit appeler render avec 'lettings/letting.html'
    et le contexte contenant 'title' et 'address'.
    """
    dummy = DummyLetting("Test Title", "Test Address")
    # get attend un id, on ignore l'argument
    monkeypatch.setattr(Letting.objects, 'get', lambda **kwargs: dummy)

    def fake_render(request, template, context):
        return {'template': template, 'context': context}
    monkeypatch.setattr(views, 'render', fake_render)

    rf = RequestFactory()
    request = rf.get('/lettings/1/')

    result = views.letting(request, letting_id=1)

    assert result['template'] == 'lettings/letting.html'
    assert result['context']['title'] == 'Test Title'
    assert result['context']['address'] == 'Test Address'


def test_letting_view_raises_when_not_found(monkeypatch):
    """
    Si Letting.objects.get() n'existe pas, la vue doit propager l'exception.
    """
    def fake_get(**kwargs):
        raise Letting.DoesNotExist
    monkeypatch.setattr(Letting.objects, 'get', fake_get)

    rf = RequestFactory()
    request = rf.get('/lettings/999/')

    with pytest.raises(Letting.DoesNotExist):
        views.letting(request, letting_id=999)
