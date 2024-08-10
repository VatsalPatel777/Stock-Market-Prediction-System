# jinja2_filters.py
from django.urls import reverse

def url_for(name, *args, **kwargs):
    return reverse(name, args=args, kwargs=kwargs)