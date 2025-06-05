# lettings/migrations/0002_copy_data.py

from django.db import migrations


def copy_address_data(apps, schema_editor):
    OldAddress = apps.get_model('oc_lettings_site', 'Address')
    NewAddress = apps.get_model('lettings', 'Address')
    for old in OldAddress.objects.all():
        NewAddress.objects.create(
            id=old.id,
            number=old.number,
            street=old.street,
            city=old.city,
            state=old.state,
            zip_code=old.zip_code,
            country_iso_code=old.country_iso_code,
        )


def copy_letting_data(apps, schema_editor):
    OldLetting = apps.get_model('oc_lettings_site', 'Letting')
    NewLetting = apps.get_model('lettings', 'Letting')
    for old in OldLetting.objects.all():
        NewLetting.objects.create(
            id=old.id,
            title=old.title,
            address_id=old.address_id,
        )


class Migration(migrations.Migration):
    dependencies = [
        ('lettings', '0001_initial'),
        ('oc_lettings_site', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(copy_address_data),
        migrations.RunPython(copy_letting_data),
    ]
