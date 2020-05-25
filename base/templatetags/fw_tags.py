import decimal
from datetime import timedelta
from django import template
from django.utils import timezone
from django.utils.datetime_safe import datetime
from django.utils.http import urlencode
from num2words import num2words
from django.utils.timesince import timesince

register = template.Library()


@register.filter
def time_until(value):
    now = datetime.now()
    try:
        difference = value - now
    except:
        return value

    if difference <= timedelta(minutes=1):
        return 'just now'
    return '%(time)s ago' % {'time': timesince(value).split(', ')[0]}

@register.filter
def days_until(value):
    now = datetime.now(timezone.utc)
    try:
        difference = now - value
    except:
        return value

    if difference <= timedelta(days=1):
        return ''
    return ' (дни: {:d})'.format(difference.days)

@register.inclusion_tag('paged_nav.html', takes_context=True)
def paging_navigation(context, page, params, *args, **kwargs):
    max_page_btn = 10
    if 'max_page_btn' in kwargs:
        max_page_btn = kwargs['max_page_btn']
    rng = page.paginator.page_range
    if rng.stop > max_page_btn:
        step = int(rng.stop // max_page_btn)+1
        new_range = range(rng.start, rng.stop, step)
    else:
        new_range = rng
    return {
        'page': page,
        'param': params,
        'max_page_btn': max_page_btn,
        'page_range':new_range
    }

@register.simple_tag()
def multiply(qty, unit_price, *args, **kwargs):
    # you would need to do any localization of the result here
    if qty and unit_price:
        sum = qty * unit_price
    else:
        sum=0
    return sum


@register.simple_tag(takes_context=True)
def numworder(context, text, **kwargs):
    try:
        return num2words(text, **kwargs)
    except decimal.InvalidOperation:
        return text

@register.simple_tag
def text_currency(number, before='', curency_text='грн.', **kwargs):
    if number:
        try:
            if 'lang' not in kwargs:
                kwargs['lang'] = 'uk'
            if 'to' not in kwargs:
                kwargs['to'] = 'currency'
            if 'currency' not in kwargs:
                kwargs['currency'] = 'UAH'
            text = num2words(number, **kwargs)

            return '{:s} {:s} ({:.2f} {:s})'.format(before, text, number, curency_text)
        except decimal.InvalidOperation:
            return number
    return ''



@register.simple_tag
def url_replace(request, field, value):
    d = request.GET.copy()
    d[field] = value
    return urlencode(d)


@register.simple_tag
def url_delete(request, field):
    d = request.GET.copy()
    del d[field]
    return urlencode(d)


@register.simple_tag(takes_context=True)
def param_replace(context, param, **kwargs):
    """
    Return encoded URL parameters that are the same as the current
    request's parameters, only with the specified GET parameters added or changed.

    It also removes any empty parameters to keep things neat,
    so you can remove a parm by setting it to ``""``.

    For example, if you're on the page ``/things/?with_frosting=true&page=5``,
    then

    <a href="/things/?{% param_replace page=3 %}">Page 3</a>

    would expand to

    <a href="/things/?with_frosting=true&page=3">Page 3</a>

    Based on
    https://stackoverflow.com/questions/22734695/next-and-before-links-for-a-django-paginated-query/22735278#22735278
    """
    #print(context)
    if 'request' in context and context['request'].GET:
        d = context['request'].GET.copy()
    else:
        d={}
    #print(d)
    for k, v in kwargs.items():
        d[k] = v
    for k in [k for k, v in d.items() if not v]:
        del d[k]

    for pk, pv in param.items():
        d[pk] = pv

    #print(d)
    return urlencode(d)