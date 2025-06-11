import pytest
from django.core.exceptions import ValidationError
from lettings.models import Address


def test_address_instance_creation_with_valid_data():
    """
    Instanciation d'une adresse avec des données valides ne doit pas lever d'erreur de validation.
    """
    valid_data = {
        "number": 123,
        "street": "Test Street",
        "city": "Test City",
        "state": "TS",
        "zip_code": 54321,
        "country_iso_code": "TST"
    }
    address = Address(**valid_data)
    address.full_clean()
    assert isinstance(address, Address)
    assert address.number == 123
    assert address.street == "Test Street"


def test_str_method_returns_number_and_street():
    """
    La méthode __str__ doit renvoyer "<number> <street>".
    """
    data = {
        "number": 456,
        "street": "Another Ave",
        "city": "City",
        "state": "ST",
        "zip_code": 12345,
        "country_iso_code": "CTA"
    }
    address = Address(**data)
    assert str(address) == "456 Another Ave"


@pytest.mark.parametrize("field,value", [
    ("number", 10000),  # dépasse MaxValueValidator(9999)
    ("zip_code", 100000),  # dépasse MaxValueValidator(99999)
])
def test_max_value_validators_raise(field, value):
    """
    Les champs number et zip_code ne doivent pas dépasser leur valeur maximale.
    """
    data = {"number": 1, "street": "S", "city": "C", "state": "ST",
            "zip_code": 1, "country_iso_code": "ABC", field: value}
    address = Address(**data)
    with pytest.raises(ValidationError):
        address.full_clean()


@pytest.mark.parametrize("field,value", [
    ("state", "T"),  # moins de 2 caractères
    ("country_iso_code", "TS"),  # moins de 3 caractères
])
def test_min_length_validators_raise(field, value):
    """
    Les champs state et country_iso_code doivent respecter leur longueur minimale.
    """
    data = {"number": 1, "street": "S", "city": "C", "state": "ST",
            "zip_code": 1, "country_iso_code": "ABC", field: value}
    address = Address(**data)
    with pytest.raises(ValidationError):
        address.full_clean()


@pytest.mark.parametrize("field,invalid", [
    ("street", "S" * 65),  # plus de 64 caractères
    ("city", "C" * 65),  # plus de 64 caractères
])
def test_max_length_validators_raise(field, invalid):
    """
    Les champs street et city doivent respecter leur longueur maximale.
    """
    data = {"number": 1, "street": "S", "city": "C", "state": "ST",
            "zip_code": 1, "country_iso_code": "ABC", field: invalid}
    address = Address(**data)
    with pytest.raises(ValidationError):
        address.full_clean()


@pytest.mark.parametrize("field", ["street", "city"])
def test_required_string_fields_cannot_be_blank(field):
    """
    Les champs street et city sont obligatoires et ne peuvent pas être vides.
    """
    data = {"number": 1, "street": "Street", "city": "City", "state": "ST",
            "zip_code": 1, "country_iso_code": "ABC", field: ""}
    address = Address(**data)
    with pytest.raises(ValidationError) as excinfo:
        address.full_clean()
    assert field in excinfo.value.message_dict
