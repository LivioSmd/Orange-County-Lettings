# profiles/migrations/0002_copy_data.py

from django.db import migrations


def copy_profile_data(apps, schema_editor):
    OldProfile = apps.get_model('oc_lettings_site', 'Profile')
    NewProfile = apps.get_model('profiles', 'Profile')
    for old in OldProfile.objects.all():
        NewProfile.objects.create(
            id=old.id,
            user=old.user,
            favorite_city=old.favorite_city,
        )


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
        ('oc_lettings_site', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(copy_profile_data),
    ]
