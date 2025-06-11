import pytest
from django.test import RequestFactory
from profiles import views
from profiles.models import Profile


class DummyProfile:
    """
    Profile factice sans accès base de données.
    """
    def __init__(self, username="dummy"):
        self.user = type("U", (), {"username": username})
        self.favorite_city = ""


def test_index_view_returns_correct_template_and_context(monkeypatch):
    """
    La vue index doit appeler render avec le template 'profiles/index.html'
    et le contexte contenant 'profiles_list'.
    """
    dummy_profiles = [DummyProfile("u1"), DummyProfile("u2")]
    monkeypatch.setattr(Profile.objects, 'all', lambda: dummy_profiles)

    def fake_render(request, template, context):
        return {'template': template, 'context': context}
    monkeypatch.setattr(views, 'render', fake_render)

    rf = RequestFactory()
    request = rf.get('/profiles/')

    result = views.index(request)

    assert result['template'] == 'profiles/index.html'
    assert 'profiles_list' in result['context']
    assert result['context']['profiles_list'] is dummy_profiles


def test_profile_view_returns_correct_template_and_context(monkeypatch):
    """
    La vue profile doit appeler render avec 'profiles/profile.html'
    et le contexte contenant 'profile'.
    """
    dummy = DummyProfile("alice")
    monkeypatch.setattr(Profile.objects, 'get', lambda id: dummy)

    def fake_render(request, template, context):
        return {'template': template, 'context': context}
    monkeypatch.setattr(views, 'render', fake_render)

    rf = RequestFactory()
    request = rf.get('/profiles/1/')

    result = views.profile(request, profile_id=1)

    assert result['template'] == 'profiles/profile.html'
    assert 'profile' in result['context']
    assert result['context']['profile'] is dummy


def test_profile_view_raises_when_not_found(monkeypatch):
    """
    Si Profile.objects.get() n'existe pas, la vue doit propager l'exception.
    """
    # Simuler get() qui lève DoesNotExist
    def fake_get(**kwargs):
        raise Profile.DoesNotExist
    monkeypatch.setattr(Profile.objects, 'get', fake_get)

    rf = RequestFactory()
    request = rf.get('/profiles/999/')

    with pytest.raises(Profile.DoesNotExist):
        views.profile(request, profile_id=999)
