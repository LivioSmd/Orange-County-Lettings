import os
import django

"""
conftest.py is read by pytest before importing your test modules.
Placing os.environ.setdefault(...) here forces Django to know its settings
(oc_lettings_site.settings) as soon as pytest starts loading tests.
"""

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oc_lettings_site.settings')
django.setup()
