from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def add_one(item):
    return item+1

@register.filter
def sub_one(item):
    return item-1
