import pytest
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from profiles.models import Profile


def fake_user(username="testuser"):
    """
    Retourne une instance de User "sauvegardée" en simulant un id,
    pour bypasser la validation de la PK sans toucher à la DB.
    """
    user = User(username=username)
    user.id = 1  # simule qu'il est déjà en base
    return user


def test_profile_str_returns_username():
    """
    La méthode __str__ doit renvoyer le username de l'utilisateur associé.
    """
    user = fake_user(username="alice")
    profile = Profile(user=user)
    # pas besoin de full_clean pour __str__
    assert str(profile) == "alice"


def test_favorite_city_blank_allowed():
    """
    Le champ favorite_city peut être vide sans lever d'erreur de validation.
    """
    user = fake_user()
    profile = Profile(user=user, favorite_city="")
    # on exclut 'user' car on ne teste que favorite_city
    profile.full_clean(exclude=['user'])
    assert profile.favorite_city == ""


@pytest.mark.parametrize("city", [
    "Paris",
    "C" * 64,     # longueur maximale autorisée
])
def test_favorite_city_valid_lengths(city):
    """
    Les villes de longueur <= 64 passent la validation.
    """
    user = fake_user()
    profile = Profile(user=user, favorite_city=city)
    profile.full_clean(exclude=['user'])
    assert profile.favorite_city == city


@pytest.mark.parametrize("city", [
    "C" * 65,     # dépasse la longueur maximale
])
def test_favorite_city_max_length_validator(city):
    """
    Les villes de longueur > 64 doivent lever ValidationError.
    """
    user = fake_user()
    profile = Profile(user=user, favorite_city=city)
    with pytest.raises(ValidationError) as excinfo:
        # on exclut user pour ne tester que favorite_city
        profile.full_clean(exclude=['user'])
    assert 'favorite_city' in excinfo.value.message_dict
