from django.urls import reverse, resolve

from lettings import views as lettings_views
from profiles import views as profiles_views
import oc_lettings_site.views as main_views


def test_url_resolves_to_correct_view():
    """
    Vérifie que chaque nom de route résout vers la vue correcte.
    """
    url_patterns = [
        ("lettings:index", {}, lettings_views.index),
        ("lettings:letting", {"letting_id": 1}, lettings_views.letting),
        ("profiles:index", {}, profiles_views.index),
        ("profiles:profile", {"profile_id": 1}, profiles_views.profile),
        ("index", {}, main_views.index),
    ]
    for name, kwargs, view_fn in url_patterns:
        path = reverse(name, kwargs=kwargs)
        match = resolve(path)
        assert match.func == view_fn
