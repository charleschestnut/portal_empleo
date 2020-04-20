from django import template

register = template.Library()


@register.simple_tag(name='url_transform_pagination')
def url_transform_pagination(url, page):
    idx = str(url).find("&page=")
    if idx == -1:
        url = str(url) + "&page="+str(page)
    else:
        idx = idx + 6
        # Le añadimos el +6 debido a que en el método find te devuelve el índice del primer caracter, no del último.
        substring = "&page="+str(url[idx])
        url = url.replace(substring, "&page="+str(page))
    return url
