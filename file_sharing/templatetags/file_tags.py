from django.template import Library

register = Library()

@register.filter
def get_icon(mime):
    if mime.startswith('image'):
        return 'icon-picture'
    elif mime.startswith('text'):
        return 'icon-file'
    elif mime.startswith('video'):
        return 'icon-film'
    elif mime.startswith('audio'):
        return 'icon-music'   
