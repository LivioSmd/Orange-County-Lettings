from django.db import models
from django.core.validators import MaxValueValidator, MinLengthValidator


class Address(models.Model):
    """
    Represents a postal address.
    """
    number = models.PositiveIntegerField(validators=[MaxValueValidator(9999)])
    street = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    state = models.CharField(max_length=2, validators=[MinLengthValidator(2)])
    zip_code = models.PositiveIntegerField(validators=[MaxValueValidator(99999)])
    country_iso_code = models.CharField(max_length=3, validators=[MinLengthValidator(3)])

    class Meta:  # add to manage singular and plural in the admin area of the site
        """
        Model metadata to define singular and plural names.
        """
        verbose_name = "adresse"
        verbose_name_plural = "adresses"

    def __str__(self):
        """
        Return a string representation of the address.
        """
        return f'{self.number} {self.street}'


class Letting(models.Model):
    """
    Represents a letting property linked to an address.
    """
    title = models.CharField(max_length=256)
    address = models.OneToOneField(Address, on_delete=models.CASCADE)

    def __str__(self):
        """
        Return the title of the letting.
        """
        return self.title
