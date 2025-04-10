# Create a file named templatetags/custom_filters.py in your app directory

from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Gets an item from a dictionary using key"""
    return dictionary.get(key)

@register.filter
def get_attr(obj, attr):
    """Gets an attribute of an object"""
    return getattr(obj, attr, '')