from django import template

register = template.Library()


@register.simple_tag(name='url_transform_pagination')
def url_transform_pagination(url, page):

    print('URL: '+str(url))
    print('PAGE: '+str(page))

    idx = str(url).find("&page=")
    print('INDEX: '+str(idx))
    if idx== -1:
        url = str(url) + "&page="+str(page)
    else:
        substring = "page="+str(url[idx])
        url.replace(substring, "&page="+str(page))

    return url