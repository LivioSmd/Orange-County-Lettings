import pytest
from django.core.exceptions import ValidationError
from lettings.models import Address, Letting


def fake_address():
    """
    Retourne une instance d'Address non sauvegardée pour usage en tests sans DB.
    """
    data = {
        "number": 10,
        "street": "Fake Street",
        "city": "Fake City",
        "state": "FC",
        "zip_code": 11111,
        "country_iso_code": "FKE",
    }
    return Address(**data)


def test_str_method_returns_title():
    """
    La méthode __str__ de Letting doit renvoyer le titre.
    """
    address = fake_address()
    letting = Letting(title="Mon Super Logement", address=address)
    assert str(letting) == "Mon Super Logement"


@pytest.mark.parametrize("title", [None, ""])
def test_title_required_raises_validation_error(title):
    """
    Le champ title est obligatoire : full_clean() doit lever ValidationError.
    """
    address = fake_address()
    letting = Letting(title=title, address=address)
    with pytest.raises(ValidationError) as excinfo:
        # full_clean() pour valider les champs
        letting.full_clean()
    assert 'title' in excinfo.value.message_dict


@pytest.mark.parametrize("address_val", [None])
def test_address_required_raises_validation_error(address_val):
    """
    Le champ address est obligatoire : full_clean() doit lever ValidationError.
    """
    letting = Letting(title="Titre Exemple", address=address_val)
    with pytest.raises(ValidationError) as excinfo:
        letting.full_clean()
    assert 'address' in excinfo.value.message_dict
